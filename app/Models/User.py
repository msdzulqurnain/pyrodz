from framework.database import Model


class User(Model):
    table = "users"
    fillable = ["first_name", "last_name", "username", "user_id"]
    guarded = ["id"]
    timestamps = True
