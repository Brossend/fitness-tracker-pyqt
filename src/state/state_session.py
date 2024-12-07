class StateSession:
    def __init__(self):
        self.logged_in_user = None

    def set_user(self, user_data):
        self.logged_in_user = user_data

    def get_user(self):
        return self.logged_in_user

    def clear_user(self):
        self.logged_in_user = None

state_session = StateSession()