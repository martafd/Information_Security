import ast
from tempfile import mkstemp
from shutil import move
from user import User
import os


def read_from_file():
    file = open('data.txt', 'r')
    split_lines = []
    for line in file:
        split_lines.append(line.replace('\n', '').split(' ', -1))
    file.close()
    return split_lines


def write_to_file(cur_line, new_line):
    fd, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open('data.txt') as old_file:
            for line in old_file:
                new_file.write(line.replace(cur_line, new_line))
    os.close(fd)
    os.remove('data.txt')  # Remove original file
    move(abs_path, 'data.txt')  # Move new file


def writing_new_password(login_name, password, split_lines, item, first_try):
    fd, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open('data.txt') as old_file:
            if password == '':
                for line in old_file:
                    if login_name in line:
                        new_file.write(line[:-1] + ' ' + first_try + '\n')
                    else:
                        new_file.write(line)
            else:
                for line in old_file:
                    new_file.write(line.replace(login_name + ' ' + str(split_lines[item][1]) + ' ' +
                                                str(split_lines[item][2]) + ' ' +
                                                str(split_lines[item][3]) + ' ' +
                                                str(password), login_name + ' ' +
                                                str(split_lines[item][1]) + ' ' +
                                                str(split_lines[item][2]) + ' ' +
                                                str(split_lines[item][3]) + ' ' +
                                                str(first_try)))
    os.close(fd)
    os.remove('data.txt')  # Remove original file
    move(abs_path, 'data.txt')  # Move new file


def check_password(password):
    flag1 = False
    flag2 = False
    ar_operators = ['+', '-', '*', '/', '%', '//', '**']
    for letter in password:
        if letter.isalpha():
            if flag1:
                continue
            else:
                flag1 = True
    for letter in password:
        if letter in ar_operators:
            if flag2:
                continue
            else:
                flag2 = True
    return flag1 and flag2


def enter_new_password(login_name, password, split_lines, item):
    try:
        flag = False
        while not flag:
            first_try = raw_input('Enter new password: ')
            if ast.literal_eval(split_lines[item][2]):
                print 'flag ' + str(flag)
                flag = check_password(login_name, split_lines, first_try)
                if not flag:
                    print 'Look for password limits'
            else:
                flag = True
        second_try = raw_input('Enter new password once more: ')
        if first_try == second_try:
            writing_new_password(login_name, password, split_lines, item, first_try)
            print 'Password changed successfully\n'
            if login_name == split_lines[0][0]:
                show_admin_panel(login_name, first_try)
            else:
                show_user_panel(login_name, first_try)
        else:
            print 'Passwords are not equal'
    except ValueError:
        print 'Empty password'


def change_password(login_name, password):
    split_lines = read_from_file()
    second_password = raw_input('Current password: ')
    if (second_password == password) or (second_password == password and password == ''):
        for item in xrange(len(split_lines)):
            if login_name in split_lines[item][0]:
                if len(split_lines[item]) < 5:
                    enter_new_password(login_name, '', split_lines, item)
                # elif password != split_lines[item][4]:
                #     print 'Password is incorrect, to change password enter correct one'
                else:
                    enter_new_password(login_name, password, split_lines, item)
    else:
        print 'Password is incorrect, to change password enter correct one'


def list_of_users():
    split_lines = read_from_file()
    print 'user_name'.rjust(9), 'is_blocked'.rjust(9), 'limit_on'.rjust(9), \
        'is_admin'.rjust(9),  'password'.rjust(9)
    for i in xrange(len(split_lines)):
        try:
            print str(split_lines[i][0]).rjust(9), str(split_lines[i][1]).rjust(9),\
                str(split_lines[i][2]).rjust(9), str(split_lines[i][3]).rjust(9), str(split_lines[i][4]).rjust(9)
        except IndexError:
            continue


def add_to_file(line):
    file = open('data.txt', 'a')
    file.write(line)
    file.close()


def add_user():
    split_lines = read_from_file()
    new_user = User
    while True:
        new_user.name = raw_input('Enter user"s name: ')
        new_user.is_user_blocked = False
        new_user.limit_on_password = False
        new_user.is_admin = False
        if new_user.name not in [split_lines[item][0] for item in range(len(split_lines))]:
            new_user.password = ''
            line = new_user.name + ' ' + str(new_user.is_user_blocked) + ' ' + str(new_user.limit_on_password) + \
                   ' ' + str(new_user.is_admin) + ' ' + new_user.password + '\n'
            add_to_file(line)
            print 'User creates successfully'
            return
        else:
            print 'This user name exists. Choose another user name.'


def show_user_panel(login_name, password):
    while True:
        print 'Menu:'
        print '1. Change password\n2. Exit to main menu'
        choice = int(raw_input('Choice: '))
        if choice == 1:
            print '\n-----Changing password--------'
            change_password(login_name, password)
        elif choice == 2:
            show_menu()
        else:
            print 'incorrect choice'
            continue


def is_blocked():
    split_lines = read_from_file()
    name = raw_input('Enter user name to block: ')
    name_in_file = False
    for item in xrange(len(split_lines)):
        if name == split_lines[item][0]:
            name_in_file = True
            if not ast.literal_eval(split_lines[item][1]):   # if user is not blocked
                cur_line = str(split_lines[item][0]) + ' ' + str(split_lines[item][1])
                new_line = str(split_lines[item][0]) + ' ' + str(not ast.literal_eval(split_lines[item][1]))
                write_to_file(cur_line, new_line)
                print 'User blocked successfully\n'
            else:
                print 'User is already blocked\n'
    if not name_in_file:
        print 'This user does not exist'


def limit_on_password():
    split_lines = read_from_file()
    name = raw_input('Enter user name to know if the limit on password: ')
    for item in xrange(len(split_lines)):
        if name == split_lines[item][0]:
            print 'Current password is limited. ' + split_lines[item][2]
            print 'Do you want to change user"s limit on password?'
            print '1. Yes\n2. No'
            choice = raw_input('Choice: ')
            if choice == '1':
                cur_line = str(split_lines[item][0]) + ' ' + str(split_lines[item][1]) + ' ' + \
                           str(split_lines[item][2]) + ' ' + str(split_lines[item][3]) + ' ' + \
                           str(split_lines[item][4])
                new_line = str(split_lines[item][0]) + ' ' + str(split_lines[item][1]) + ' ' + \
                           str(not ast.literal_eval(split_lines[item][2])) + ' ' + \
                           str(split_lines[item][3]) + ' ' + str(split_lines[item][4])
                write_to_file(cur_line, new_line)
                print 'You change user"s limit on password'
                return
            elif choice == '2':
                return
            else:
                print 'Incorrect choice'
                return


def show_admin_panel(login_name, password):
    while True:
        print '\n------- Admin Menu-------'
        print '1. Change admin password\n2. List of users\n3. Add new user'
        print '4. Block user\n5. Limits on password\n6. Exit to main menu\n'
        choice = int(raw_input('Choice: '))
        print '\n'
        if choice == 1:
            print '\n-----Changing password--------'
            change_password(login_name, password)                # don't works
        elif choice == 2:
            print '\n-----List of users--------'
            list_of_users()                                      # works
        elif choice == 3:
            print '\n-------Adding new user-------'
            add_user()                       # works
        elif choice == 4:
            print '\n-------Blocking user-------'
            is_blocked()                                         # works
        elif choice == 5:
            print '\n-------Checking limit on password-------'
            limit_on_password()                                  # works
        elif choice == 6:
            show_menu()                                          # works
        else:
            print 'Incorrect choice'
            continue


def login():
    split_lines = read_from_file()
    login_name = raw_input('Login: ')
    for i in xrange(3):
        if login_name == split_lines[0][0] and split_lines[0][3] == 'True':   # check if admin
            try:
                password = raw_input('Password: ')
                if len([split_lines[item] for item in xrange(len(split_lines)) if login_name ==
                        split_lines[0][0]][0]) < 5 and len(password) == 0:
                    show_admin_panel(login_name, password)

                elif password == split_lines[0][4]:
                    show_admin_panel(login_name, password)
                else:
                    print 'Admin password is incorrect, try again'
                    continue
            except IndexError:
                print 'Incorrect password'
                show_menu()
            except ValueError:
                print 'Incorrect password'
                show_menu()

        # user in file and not blocked
        elif login_name in [split_lines[item][0] for item in xrange(len(split_lines))]:
            if not (ast.literal_eval(str([split_lines[item][1] for item in xrange(len(split_lines))
                                          if login_name == split_lines[item][0]][0]))):
                try:
                    password = raw_input('Password: ')

                    if len([split_lines[item] for item in xrange(len(split_lines)) if login_name ==
                            split_lines[item][0]][0]) < 5 and len(password) == 0:
                        show_user_panel(login_name, password)
                    elif password == [split_lines[item][4] for item in range(len(split_lines))
                                      if login_name == split_lines[item][0]][0]:
                        show_user_panel(login_name, password)
                    else:
                        if i == 2:
                            print 'You entered wrong password tree times! \n'
                            exit()
                        else:
                            print 'User password is incorrect, try again'
                            continue
                except IndexError:
                    print 'Incorrect password'
                    show_menu()
                except ValueError:
                    print 'Incorrect password'
                    show_menu()
            else:
                if i == 2:
                    print 'You are blocked'
        else:
            return


def info():
    print '\n------- INFO -------'
    print 'Lab_1 by Marta Fedyshyn, IS-32'
    print 'Variant 2: Availability of letters and arithmetic operators.\n'
    return


def show_menu():
    while True:
        print '\n------- Main Menu -------'
        print '1. Login\n2. Info \n3. Exit\n'
        choice = raw_input('Choice: ')
        print '\n'
        if choice == '1':
            login()
        elif choice == '2':
            info()
        elif choice == '3':
            exit()
        else:
            print 'Incorrect choice'
            continue


if __name__ == '__main__':
    file_name = 'file.txt'
    if not os.path.exists(file_name):
        f = open(file_name, 'w')
        f.write('ADMIN False False True ')  # admin login, is_blocked, limit_on, is_admin
        f.close()
    show_menu()
