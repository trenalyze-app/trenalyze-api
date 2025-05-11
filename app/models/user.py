import mongoengine as me


class UserModel(me.Document):
    first_name = me.StringField(required=True)
    last_name = me.StringField(required=True)
    username = me.StringField(required=True, unique=True)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    created_at = me.IntField(required=True)
    updated_at = me.IntField(required=True)
    is_active = me.BooleanField(required=False, default=False)
    bio = me.StringField(required=False)
    country = me.StringField(required=False)
    city = me.StringField(required=False)
    postal_code = me.StringField(required=False)

    meta = {"collection": "users"}

    async def unique_field(self):
        if self.username:
            self.username = self.username.lower()
        if self.email:
            self.email = self.email.lower()
