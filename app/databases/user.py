from .database import Database
from ..models import UserModel
import datetime
import mongoengine as me


class UserDatabase(Database):
    @staticmethod
    async def insert(first_name, last_name, username, email, password):
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        user_data = UserModel(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            created_at=created_at,
            updated_at=created_at,
        )
        await user_data.unique_field()
        user_data.save()
        return user_data

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        pass

    @staticmethod
    async def get(category, **kwargs):
        email = kwargs.get("email")
        username = kwargs.get("username")
        if category == "by_email_username":
            if user_data := UserModel.objects(
                me.Q(email=email) | me.Q(username=username)
            ):
                return user_data
        if category == "by_email":
            if user_data := UserModel.objects(email=email.lower()):
                return user_data
