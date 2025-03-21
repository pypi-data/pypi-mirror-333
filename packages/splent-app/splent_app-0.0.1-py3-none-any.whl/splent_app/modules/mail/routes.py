from flask import render_template
from splent_app.modules.mail import mail_bp


@mail_bp.route("/mail", methods=["GET"])
def index():
    return render_template("mail/index.html")
