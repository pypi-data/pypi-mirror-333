from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, logout_user
from pymysql import IntegrityError

from splent_app.modules.auth import auth_bp
from splent_app.modules.auth.decorators import guest_required
from splent_app.modules.auth.forms import SignupForm, LoginForm
from splent_app.modules.auth.services import AuthenticationService
from splent_app.modules.confirmemail.services import ConfirmemailService
from splent_app.modules.profile.services import UserProfileService

from splent_app import db

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
confirmemail_service = ConfirmemailService()


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = SignupForm()
    if form.validate_on_submit():

        email = form.email.data
        if not authentication_service.is_email_available(email):
            flash(f"Email {email} is already in use", "danger")
            return render_template("auth/signup_form.html", form=form)

        try:
            # We try to create the user
            user = authentication_service.create_with_profile(**form.data)
            confirmemail_service.send_confirmation_email(user.email)
        except IntegrityError as exc:
            db.session.rollback()
            if "Duplicate entry" in str(exc):
                flash(f"Email {email} is already in use", "danger")
            else:
                flash(f"Error creating user: {exc}", "danger")
            return render_template("auth/signup_form.html", form=form)

        return redirect(url_for("public.index"))

    return render_template("auth/signup_form.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@guest_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():

        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for("public.index"))

        return render_template(
            "auth/login_form.html", form=form, error="Invalid credentials"
        )

    return render_template("auth/login_form.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.index"))
