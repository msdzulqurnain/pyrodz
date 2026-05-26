from framework.database import Schema


class CreateUsersTable:
    def up(self):
        Schema.create("users", [
            Schema.increments("id"),
            Schema.string("first_name", 100),
            Schema.string("last_name", 100),
            Schema.string("username"),
            Schema.integer("user_id").set_unique(),
            Schema.timestamps(),
        ])

    def down(self):
        Schema.drop("users")
