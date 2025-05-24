from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name='default'):
    app = Flask(__name__)

    # Load configuration
    from config.settings import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    from app.models import init_db
    init_db(app)

    login_manager.init_app(app)

    # Register blueprints
    from app.views.main import main as main_blueprint
    from app.views.medical_records import medical_records
    from app.views.auth import auth as auth_blueprint
    from app.models.employee import Employee
    from app.views.certificates import certificates
    from app.views.reports import reports as reports_bp

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(certificates)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(medical_records)
    app.register_blueprint(reports_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    return app