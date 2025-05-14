from flask import Flask, request
import os
from .config import (
    database_mongodb,
    database_mongodb_url,
    smtp_host,
    smtp_port,
    smtp_email,
    smtp_password,
    celery_broker_url,
    celery_result_backend,
)
from .database import db
from .celery_app import celery_init_app
from .mail import mail
import datetime
from .models import AccountActiveModel
from celery.schedules import crontab


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    private_key_path = os.path.join(BASE_DIR, "keys", "private.pem")
    public_key_path = os.path.join(BASE_DIR, "keys", "public.pem")

    global PRIVATE_KEY, PUBLIC_KEY
    with open(private_key_path, "rb") as f:
        PRIVATE_KEY = f.read()

    with open(public_key_path, "rb") as f:
        PUBLIC_KEY = f.read()

    app.config.from_prefixed_env()
    app.config.from_mapping(
        CELERY=dict(
            broker_url=celery_broker_url,
            result_backend=celery_result_backend,
            task_ignore_result=True,
        ),
    )
    app.config["MONGODB_SETTINGS"] = {
        "db": database_mongodb,
        "host": database_mongodb_url,
        "connect": False,
    }
    app.config["MAIL_SERVER"] = smtp_host
    app.config["MAIL_PORT"] = smtp_port
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = smtp_email
    app.config["MAIL_PASSWORD"] = smtp_password
    app.config["MAIL_DEFAULT_SENDER"] = smtp_email

    global celery_app
    celery_app = celery_init_app(app)
    db.init_app(app)
    mail.init_app(app)

    @celery_app.task(name="delete_token_task")
    def delete_token_task():
        expired_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        if data_account_active := AccountActiveModel.objects.all():
            for account_active_data in data_account_active:
                if account_active_data.expired_at <= expired_at:
                    account_active_data.delete()
        return f"delete token at {int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"

    celery_app.conf.beat_schedule = {
        "run-every-5-minutes": {
            "task": "delete_token_task",
            "schedule": crontab(minute="*/5"),
        },
    }

    with app.app_context():
        from .api.login import login_router
        from .api.register import register_router
        from .api.account_active import account_active_router
        from .api.business import business_router
        from .api.profile import profile_router

        app.register_blueprint(login_router)
        app.register_blueprint(register_router)
        app.register_blueprint(account_active_router)
        app.register_blueprint(business_router)
        app.register_blueprint(profile_router)

    @app.after_request
    async def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    @app.before_request
    def before_request():
        request.timestamp = datetime.datetime.now(datetime.timezone.utc)

    return app
