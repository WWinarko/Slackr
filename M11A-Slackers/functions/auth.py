''' Authorisation functions for Slackr webapp '''
# Disable anomalous-backslash-in-string check in pylint due to usage in regex
# pylint: disable=W1401
import hashlib
import re
import time
import jwt
from functions.error import ValueError

DATA = {
    'users': [],
    'curr_u_id': 1,
    'reset_codes': [],
    'channels' : [],
    'messages' : [],
    'secret': 'M11Aslackers',
}

def get_data():
    ''' Returns global data variable '''
    global DATA
    return DATA

def generate_token(u_id):
    ''' Generates a token using JWT '''
    data = get_data()
    payload = {
        'u_id': u_id,
        'timestamp': time.time(),
    }
    return jwt.encode(payload, data['secret'], algorithm='HS256').decode('utf-8')

def get_user_from_email(input_email):
    ''' Find user given email '''
    data = get_data()
    for user in data['users']:
        if user['email'] == input_email:
            return user
    return None

def get_user_from_uid(input_uid):
    ''' Find user given u_id (used for get_user_from_token) '''
    data = get_data()
    for user in data['users']:
        if user['u_id'] == int(input_uid):
            return user
    return None

def get_user_from_token(token):
    ''' Returns user dictionary given token '''
    data = get_data()
    decoded = jwt.decode(token, data['secret'], algorithms=['HS256'])
    return get_user_from_uid(decoded['u_id'])

def hash_password(password):
    ''' Function to hash a given password using SHA256 '''
    return hashlib.sha256(password.encode()).hexdigest()


def check_valid_email(email):
    ''' Function to check if name is below 50 characters '''
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if not re.search(regex, email):
        return False
    return True

def check_name_length(name):
    ''' Funtion to check if a given name is within the required length '''
    if len(name) < 1 or len(name) > 50:
        return False
    return True

def auth_register(email, password, first, last):
    ''' Registration function '''
    data = get_data()

    if not check_valid_email(email):
        raise ValueError(description="Invalid email")

    if get_user_from_email(email) is not None:
        raise ValueError(description="Email already in use")

    if len(password) < 6:
        raise ValueError(description="Password too short")
    if not check_name_length(first):
        raise ValueError(description="Invalid first name")
    if not check_name_length(last):
        raise ValueError(description="Invalid last name")

    # add new user details  to dictionary of all users
    curr_u_id = data['curr_u_id']

    handle = (first + last)[:20]
    handle = handle.lower()
    handle_index = 1

    # check if handle taken
    for user in data['users']:
        if handle == user['handle_str']:
            # check if handle + index taken
            for same_handle_user in data['users']:
                if handle + str(handle_index) == same_handle_user['handle_str']:
                    handle_index += 1
                    continue
            # append lowest non-taken index to handle
            # while keeping handle <= 20 chars
            handle = handle[:20-len(str(handle_index))]
            handle += str(handle_index)

    # set user permission to member (3) by default
    # assume first Slackr user to register will be the Slackr owner (u_id 1 -> permission_id 1)
    if curr_u_id == 1:
        permission_id = 1
    else:
        permission_id = 3

    # generate token
    token = generate_token(curr_u_id)

    data['users'].append({
        'email': email,
        'password': hash_password(password),    # store password hashed for security reasons
        'name_first': first,
        'name_last': last,
        'handle_str': handle,
        'profile_img_url': None,
        'u_id': curr_u_id,
        'permission_id': permission_id,
        'tokens': [token],
    })

    # increment lowest untaken u_id
    data['curr_u_id'] += 1

    return {
        'token': token,
        'u_id': curr_u_id,
    }

def auth_login(email, password):
    ''' Login function '''
    data = get_data()

    if not check_valid_email(email):
        raise ValueError(description="Invalid email")

    # compare the given username and password to all stored usernames and passwords
    for user in data['users']:
        if user['email'] == email and user['password'] == hash_password(password):
            u_id = user['u_id']
            token = generate_token(u_id)
            user['tokens'].append(token)

            return {
                'token': token,
                'u_id': u_id,
            }

    raise ValueError(description='Email or password incorrect')

def auth_logout(token):
    ''' Logout function '''
    user = get_user_from_token(token)

    if user is not None:
        user['tokens'].remove(token)
        return True

    return False

def auth_passwordreset_request(email):
    ''' Password reset code request function '''
    data = get_data()

    user = get_user_from_email(email)
    name = user['name_first']

    if user is not None:
        # generate unique reset code by hashing the current time and shortening for ease of entry
        new_reset_code = hashlib.sha256(str(time.time()).encode()).hexdigest()[-15:]

        reset_code_dict = {
            'code': new_reset_code,
            'timestamp': time.time(),
            'email': email,
            'first_name': name,
        }

        data['reset_codes'].append(reset_code_dict)

        return reset_code_dict

def auth_passwordreset_reset(given_reset_code, new_password):
    ''' Password reset function '''
    data = get_data()

    if len(new_password) < 6:
        raise ValueError(description='Password must be at least 6 characters')

    for reset_code in data['reset_codes']:
        if given_reset_code == reset_code['code']:
            # check if fewer than 900 seconds (15 mins) have passed
            if time.time() - reset_code['timestamp'] <= 900:
                user = get_user_from_email(reset_code['email'])
                user['password'] = hash_password(new_password)

                data['reset_codes'].remove(reset_code)
            else:
                data['reset_codes'].remove(reset_code)
                raise ValueError(description='Invalid reset code.')

            # if the given reset code is not found in data['reset_codes'],
            # throw a ValueError
            break
    else:
        raise ValueError(description='Invalid reset code.')
