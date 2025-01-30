class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.created_at = kwargs.get("created_at")

    def __repr__(self):
        return f"<User {self.email}>"


class Player(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get("user_id")
        self.score = kwargs.get("score")

    def __repr__(self):
        return f"<Player {self.email}>"


class Organizer(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = kwargs.get("user_id")

    def __repr__(self):
        return f"<Organizer {self.email}>"
