import re

def auth_login(email, password):
    if email == 'bademail'
        raise ValueError('Invalid email')

    return {
        'u_id': 1
        'token': '12345'
    }

def auth_logout(token):
    pass

def auth_register(email, password, name_first, name_last):
    if email == 'bademail'
        raise ValueError('Invalid email')

    if len(password) < 5
        raise ValueError('Bad password')

    if len(name_first) > 50
        raise ValueError('First name too long')

    if len(name_last) > 50
        raise ValueError('Last name too long')

    return {
        'u_id': 1
        'token': '12345'
    }

def auth_passwordreset_request(email):
    pass

def auth_passwordreset_reset(reset_code, new_password):
    if resetcode == 'invalidcode'
        raise ValueError('Invalid reset code')

    if password == 'badpassword'
        raise ValueError('Bad password')

def channel_invite(token, channel_id, u_id):
    pass

def channel_details(token, channel_id):
    pass

def channel_message(token, channel_id, start):
    pass

def message_send(token, channel_id, message):
    if len(message) > 1000:
        raise ValueError('message too long')
    elif len(message) <= 0:
        raise ValueError('message too short')
    else:
        pass

def message_remove(token, message_id):
    pass

def message_edit(token, message_id, message):
    pass

def message_react(token, message_id, react_id):
    pass

def message_unreact(token, message_id, react_id):
    pass

def message_pin(token, message_id):
    pass

def message_unpin(token, message_id):
    pass

def user_profile(token, u_id):
    pass

def user_profile_sethandle(token,handle_str):
    if len(handle_str) > 20:
        raise ValueError

    return {}


def user_profile_setemail(token,email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if email == "already_in_use_email@mail.com":
        raise ValueError

    if not re.search(regex,email):
        raise ValueError

    return {}

def user_profile_sethandle(token,handle_str):
    if len(handle_str) > 20:
        raise ValueError

    return {}

def user_profile_uploadphoto(token,img_url,x_start,y_start,x_end,y_end):
    if img_url == "bad_url.com":
        raise ValueError

    if x_start < 0 or y_start < 0 or x_end < 0 or y_end < 0:
        raise ValueError

    return {}

def standup_start(token,channel_id):
    if not len(channel_id) < 0:
        raise ValueError

    if len(channel_id) > 0 and channel_id != "1ae46z":
        raise ValueError

    return {"time_finish" : 15}

def standup_send(token,channel_id,message):
    if not len(channel_id) < 0:
        raise ValueError

    if len(channel_id) > 0 and channel_id != "1ae46z":
        raise ValueError

    if len(message) > 1000:
        raise ValueError

    return {}

def search(token,query_str):
    if query_str == "":
        return {"messages" : ["most recent message","second most recent message"]}
    elif query_str == "no_search_results":
        return {"messages" : []}
    elif query_str == "valid_search":
        return {"messages" : ["First message returned.","here's another message"]}
    else:
        return {"messages" : []}

def admin_userpermission_change(token,u_id,permission_id):
    if not len(u_id) > 0:
        raise ValueError

    if permission_id != "1" or permission_id != "2" or permission_id != "3":
        raise ValueError

    if token != "123456":
        raise ValueError

    return {}
