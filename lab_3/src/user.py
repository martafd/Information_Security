class User:

    def __init__(self, name='', is_blocked=False, is_limit_on=False, is_admin=False, password=''):
        self.name = name
        self.is_blocked = is_blocked
        self.is_limit_on = is_limit_on
        self.is_admin = is_admin
        self.password = password

# user = User()
# user.change_password('marta', 'mmm')