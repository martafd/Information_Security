import ast
from tempfile import mkstemp
from shutil import move
from user import User
import os


def write_to_file(cur_line, new_line):
    fd, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open('data.txt') as old_file:
            for line in old_file:
                new_file.write(line.replace(cur_line, new_line))
    os.close(fd)
    os.remove('data.txt')  # Remove original file
    move(abs_path, 'data.txt')  # Move new file


def writing_new_password(login_name, password, item, first_try):
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
                    new_file.write(line.replace(login_name + ' ' + str(person_list[item].is_blocked) + ' ' +
                                                str(person_list[item].is_limit_on) + ' ' +
                                                str(person_list[item].is_admin) + ' ' +
                                                str(password), login_name + ' ' +
                                                str(person_list[item].is_blocked) + ' ' +
                                                str(person_list[item].is_limit_on) + ' ' +
                                                str(person_list[item].is_admin) + ' ' +
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


def enter_new_password(login_name, password, item):
    try:
        flag = False
        while not flag:
            first_try = raw_input('Enter new password: ')
            if ast.literal_eval(person_list[item].is_limit_on):
                print 'flag ' + str(flag)
                flag = check_password(login_name, first_try)
                if not flag:
                    print 'Look for password limits'
            else:
                flag = True
        second_try = raw_input('Enter new password once more: ')
        if first_try == second_try:
            writing_new_password(login_name, password, item, first_try)
            print 'Password changed successfully\n'
            if login_name == person_list[0].name:
                show_admin_panel(login_name, first_try)
            else:
                show_user_panel(login_name, first_try)
        else:
            print 'Passwords are not equal'
    except ValueError:
        print 'Empty password'


def change_password(login_name, password):
    second_password = raw_input('Current password: ')
    if (second_password == password) or (second_password == password and password == ''):
        for item in xrange(person_list.__len__()):
            if login_name in person_list[item].name:
                if person_list[item].password == '':
                    enter_new_password(login_name, '', item)
                # elif password != split_lines[item][4]:
                #     print 'Password is incorrect, to change password enter correct one'
                else:
                    enter_new_password(login_name, password, item)
    else:
        print 'Password is incorrect, to change password enter correct one'


def list_of_users():
    file = open('data.txt', 'r')
    split_lines = []
    for line in file:
        split_lines.append(line.replace('\n', '').split(' ', -1))
    file.close()
    person_list = []
    for person_arr in split_lines:
        if len(person_arr) < 5:
            temp = User(person_arr[0], person_arr[1], person_arr[2], person_arr[3], '')
        else:
            temp = User(person_arr[0], person_arr[1], person_arr[2], person_arr[3], person_arr[4])
        person_list.append(temp)

    print 'user_name'.rjust(9), 'is_blocked'.rjust(9), 'limit_on'.rjust(9), \
        'is_admin'.rjust(9),  'password'.rjust(9)
    for i in xrange(len(split_lines)):
        try:
            print str(person_list[i].name).rjust(9), str(person_list[i].is_blocked).rjust(9),\
                str(person_list[i].is_limit_on).rjust(9), str(person_list[i].is_admin).rjust(9), \
                str(person_list[i].password).rjust(9)
        except IndexError:
            continue


def add_to_file(append_line):
    open_to_append = open('data.txt', 'a')
    open_to_append.write(append_line)
    open_to_append.close()


def add_user():
    new_user = User()
    while True:
        new_user.name = raw_input('Enter user"s name: ')
        if new_user.name not in [person_list[item].name for item in range(len(person_list))]:
            line = new_user.name + ' ' + str(new_user.is_blocked) + ' ' + str(new_user.is_limit_on) + \
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
    name = raw_input('Enter user name to block: ')
    name_in_file = False
    for item in xrange(person_list.__len__()):
        if name == person_list[item].name:
            name_in_file = True
            if not ast.literal_eval(person_list[item].is_blocked):   # if user is not blocked
                cur_line = str(person_list[item].name) + ' ' + str(person_list[item].is_blocked)
                new_line = str(person_list[item].name) + ' ' + str(not ast.literal_eval(person_list[item].is_blocked))
                write_to_file(cur_line, new_line)
                print 'User blocked successfully\n'
            else:
                print 'User is already blocked\n'
    if not name_in_file:
        print 'This user does not exist'


def limit_on_password():
    name = raw_input('Enter user name to know if the limit on password: ')
    if name not in [person_list[item].name for item in xrange(person_list.__len__())]:
        print 'This user name do not exist'
    for item in xrange(person_list.__len__()):
        if name == person_list[item].name:
            print 'Current password is limited. ' + person_list[item].is_limit_on
            print 'Do you want to change user"s limit on password?'
            print '1. Yes\n2. No'
            choice = raw_input('Choice: ')
            if choice == '1':
                cur_line = str(person_list[item].name) + ' ' + str(person_list[item].is_blocked) + ' ' + \
                           str(person_list[item].is_limit_on) + ' ' + str(split_lines[item].is_admin) + ' ' + \
                           str(split_lines[item].password)
                new_line = str(person_list[item].name) + ' ' + str(person_list[item].is_blocked) + ' ' + \
                           str(not ast.literal_eval(person_list[item].is_limit_on)) + ' ' + \
                           str(split_lines[item].is_admin) + ' ' + str(split_lines[item].password)
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
            change_password(login_name, password)
        elif choice == 2:
            print '\n-----List of users--------'
            list_of_users()
        elif choice == 3:
            print '\n-------Adding new user-------'
            add_user()
        elif choice == 4:
            print '\n-------Blocking user-------'
            is_blocked()
        elif choice == 5:
            print '\n-------Checking limit on password-------'
            limit_on_password()
        elif choice == 6:
            return
            # show_menu()
        else:
            print 'Incorrect choice'
            continue


def login():
    login_name = raw_input('Login: ')
    for i in xrange(3):
        if login_name == person_list[0].name and person_list[0].is_admin == 'True':   # check if admin
            # try:
            password = raw_input('Password: ')
            if person_list[0].password == '' and len(password) == 0:
                show_admin_panel(person_list[0].name, person_list[0].password)
                return
            elif password == person_list[0].password:
                show_admin_panel(person_list[0].name, person_list[0].password)
                return
            else:
                print 'Admin password is incorrect, try again'
                continue
        elif login_name in [person_list[item].name for item in xrange(person_list.__len__())]:
            if not (ast.literal_eval(str([person_list[item].is_blocked for item in xrange(person_list.__len__())
                                          if login_name == person_list[item].name][0]))):
                password = raw_input('Password: ')
                if person_list[4].password == '' and len(password) == 0:
                    show_user_panel(login_name, password)
                    return
                elif password == [person_list[item].password for item in range(person_list.__len__())
                                  if login_name == person_list[item].name][0]:
                    show_user_panel(login_name, password)
                    return
                else:
                    if i == 2:
                        print 'You entered wrong password tree times! \n'
                        exit()
                    else:
                        print 'User password is incorrect, try again'
                        continue
            else:
                if i == 2:
                    print 'You are blocked'
        else:
            print 'Incorrect login'
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
            return
        else:
            print 'Incorrect choice'
            continue


if __name__ == '__main__':
    file_name = 'data.txt'
    if not os.path.exists(file_name):
        f = open(file_name, 'w')
        f.write('ADMIN False False True ')  # admin login, is_blocked, limit_on, is_admin
        f.close()

    file = open(file_name, 'r')
    split_lines = []
    for line in file:
        split_lines.append(line.replace('\n', '').split(' ', -1))
    file.close()
    
    global person_list
    person_list = []
    for person_arr in split_lines:
        if len(person_arr) < 5:
            temp = User(person_arr[0], person_arr[1], person_arr[2], person_arr[3], '')
        else:
            temp = User(person_arr[0], person_arr[1], person_arr[2], person_arr[3], person_arr[4])
        person_list.append(temp)

    show_menu()
