from .user import User


class Admin(User):
    login = 'ADMIN'
    is_admin = True
    password = 'admin'


# admin = Admin()
# admin.add_user('ADMIN', 'admin')