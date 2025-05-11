from .database import Database
from ..models import UserModel, AccountActiveModel
import datetime
import mongoengine as me


class AccountActiveDatabase(Database):
    @staticmethod
    async def insert(email, created_at, expired_at, token_email, token_web):
        if user_data := UserModel.objects(email=email).first():
            if account_active_data := AccountActiveModel.objects(
                user=user_data
            ).first():
                account_active_data.token_email = token_email
                account_active_data.token_web = token_web
                account_active_data.updated_at = created_at
                account_active_data.expired_at = expired_at
                account_active_data.save()
                return account_active_data
            account_active_data = AccountActiveModel(
                token_email=token_email,
                token_web=token_web,
                created_at=created_at,
                updated_at=created_at,
                expired_at=expired_at,
                user=user_data,
            )
            account_active_data.save()
            return account_active_data

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        created_at = kwargs.get("created_at")
        token = kwargs.get("token")
        user_id = kwargs.get("user_id")
        if category == "active_user_by_token_email":
            if user_data := UserModel.objects(id=user_id).first():
                if account_active_data := AccountActiveModel.objects(
                    user=user_data, token_email=token
                ).first():
                    user_data.is_active = True
                    user_data.updated_at = created_at
                    user_data.save()
                    account_active_data.delete()
                    return account_active_data

    @staticmethod
    async def get(category, **kwargs):
        token = kwargs.get("token")
        user_id = kwargs.get("user_id")
        if category == "by_token_email_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                if account_active_data := AccountActiveModel.objects(
                    user=user_data, token_email=token
                ).first():
                    return account_active_data
        if category == "by_token_web_user_id":
            if user_data := UserModel.objects(id=user_id).first():
                if account_active_data := AccountActiveModel.objects(
                    user=user_data, token_web=token
                ).first():
                    return account_active_data
