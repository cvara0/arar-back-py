from flask_login import LoginManager

lm = LoginManager()
lm.session_protection = "strong"