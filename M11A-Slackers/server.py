'''Flask server'''
# Disable pylint docstring check as docstrings are included in all derivative files
# pylint: disable=C0116
import sys
from json import dumps
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from functions.auth import (auth_login, auth_register, auth_logout, auth_passwordreset_request,
                            auth_passwordreset_reset)
from functions.channel import (channel_invite, channel_details, channel_messages,
                               channel_leave, channel_join, channel_addowner, channel_removeowner,
                               channel_list, channel_listall, channel_create)
from functions.standup import standup_start, standup_active, standup_send
from functions.messages import (message_send, message_sendlater, message_remove,
                                message_edit, message_react, message_unreact,
                                message_pin, message_unpin)
from functions.user import (user_profile, user_profile_setname, user_profile_setemail,
                            user_profile_sethandle, user_profiles_uploadphoto, users_all)
from functions.admin import admin_userpermission_change
from functions.search import search

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__, static_url_path='/functions/profile_imgs/') 
# email
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='m11a.slackers@gmail.com',
    MAIL_PASSWORD="M11A?slackers"
)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)

##################
# AUTH FUNCTIONS #
##################

@APP.route('/auth/register', methods=['POST'])
def create():
    ret_val = auth_register(request.form.get('email'), request.form.get('password'),
                            request.form.get('name_first'), request.form.get('name_last'))
    return dumps(ret_val)

@APP.route('/auth/login', methods=['POST'])
def connect():
    ret_val = auth_login(request.form.get('email'), request.form.get('password'))
    return dumps(ret_val)


@APP.route('/auth/logout', methods=['POST'])
def invalidate():
    is_success = auth_logout(request.form.get('token'))
    return dumps({
        'is_success': is_success,
    })

@APP.route('/auth/passwordreset/request', methods=['POST'])
def email():
    mail = Mail(APP)
    email = request.form.get('email')
    reset_dict = auth_passwordreset_request(email)

    name = reset_dict['first_name']
    new_reset_code = reset_dict['code']
    try:
        msg = Message("Slackr password reset",
                      sender="m11a.slackers@gmail.com",
                      recipients=[email])
        msg.body = f"Hi {name},\n\nYour reset code is {new_reset_code}\n \
                     Please use it within 15 minutes.\n\nRegards,\nSlackr support."
        mail.send(msg)

        return dumps({})
    except Exception as e:
        return str(e)

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def reset():
    auth_passwordreset_reset(request.form.get('reset_code'), request.form.get('new_password'))
    return dumps({})

#####################
# MESSAGE FUNCTIONS #
#####################

@APP.route('/message/send', methods=['POST'])
def send_message():
    message_send(request.form.get('token'), request.form.get('channel_id'),
                 request.form.get('message'))
    return dumps({})

@APP.route('/message/sendlater', methods=['POST'])
def send_messagelater():
    message_sendlater(request.form.get('token'), request.form.get('channel_id'),
                      request.form.get('message'), request.form.get('time_sent'))
    return dumps({})

@APP.route('/message/remove', methods=['DELETE'])
def remove_message():
    message_remove(request.form.get('token'), request.form.get('message_id'))
    return dumps({})

@APP.route('/message/edit', methods=['PUT'])
def edit_message():
    message_edit(request.form.get('token'), request.form.get('message_id'),
                 request.form.get('message'))
    return dumps({})

@APP.route('/message/react', methods=['POST'])
def react_message():
    message_react(request.form.get('token'), request.form.get('message_id'),
                  request.form.get('react_id'))
    return dumps({})

@APP.route('/message/unreact', methods=['POST'])
def unreact_message():
    message_unreact(request.form.get('token'), request.form.get('message_id'),
                    request.form.get('react_id'))
    return dumps({})

@APP.route('/message/pin', methods=['POST'])
def pin_message():
    message_pin(request.form.get('token'), request.form.get('message_id'))
    return dumps({})

@APP.route('/message/unpin', methods=['POST'])
def unpin_message():
    message_unpin(request.form.get('token'), request.form.get('message_id'))
    return dumps({})

##################
# USER FUNCTIONS #
##################

@APP.route('/user/profile', methods=['GET'])
def profile():
    ret_val = user_profile(request.args.get('token'), request.args.get('u_id'))
    return dumps(ret_val)

@APP.route('/user/profile/setname', methods=['PUT'])
def setname():
    user_profile_setname(request.form.get('token'), request.form.get('name_first'),
                         request.form.get('name_last'))
    return dumps({
    })

@APP.route('/user/profile/setemail', methods=['PUT'])
def setemail():
    user_profile_setemail(request.form.get('token'), request.form.get('email'))
    return dumps({
    })

@APP.route('/user/profile/sethandle', methods=['PUT'])
def sethandle():
    user_profile_sethandle(request.form.get('token'), request.form.get('handle_str'))
    return dumps({
    })
@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def uploadphoto():
    user_profiles_uploadphoto(request.form.get('token'), request.form.get('img_url'), request.form.get('x_start'), request.form.get('y_start'), request.form.get('x_end'), request.form.get ('y_end'))
    return dumps({      
    })
@APP.route('/profile_imgs/<path:path>')
def send_img(path):
    return send_from_directory(directory='profile_imgs',filename=path)

@APP.route('/users/all', methods=['GET'])
def get_all():
    ret_val = users_all(request.args.get('token'))
    return dumps(ret_val)

#####################
# STANDUP FUNCTIONS #
#####################

@APP.route('/standup/start', methods=['POST'])
def start():
    time_finish = standup_start(request.form.get('token'), request.form.get('channel_id'), request.form.get('length'))
    return dumps(time_finish)

@APP.route('/standup/active', methods=['GET'])
def check():
    ret_dict = standup_active(request.args.get('token'), request.args.get('channel_id'))
    return dumps(ret_dict)

@APP.route('/standup/send', methods=['POST'])
def send():
    standup_send(request.form.get('token'), request.form.get('channel_id'),
                 request.form.get('message'))
    return dumps({})

###################
# SEARCH FUNCTION #
###################

@APP.route('/search', methods=['GET'])
def get():
    ret_val = search(request.args.get('token'), request.args.get('query_str'))
    return dumps({
        'messages': ret_val,
    })

###################
# ADMIN FUNCTIONS #
###################

@APP.route('/admin/userpermission/change', methods=['POST'])
def change():
    admin_userpermission_change(request.form.get('token'), request.form.get('u_id'),
                                request.form.get('permission_id'))
    return dumps({})

#####################
# CHANNEL FUNCTIONS #
#####################

@APP.route('/channel/invite', methods=['POST'])
def invite():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_invite(token, channel_id, u_id))

@APP.route('/channel/details', methods=['GET'])
def details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel_details(token, channel_id))

@APP.route('/channel/messages', methods=['GET'])
def messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start_message = request.args.get('start')
    return dumps(channel_messages(token, channel_id, start_message))

@APP.route('/channel/leave', methods=['POST'])
def leave():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_leave(token, channel_id))

@APP.route('/channel/join', methods=['POST'])
def join():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_join(token, channel_id))

@APP.route('/channel/addowner', methods=['POST'])
def addowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_addowner(token, channel_id, u_id))

@APP.route('/channel/removeowner', methods=['POST'])
def removeowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_removeowner(token, channel_id, u_id))

@APP.route('/channels/list', methods=['GET'])
def list_():
    token = request.args.get('token')
    return dumps(channel_list(token))

@APP.route('/channels/listall', methods=['GET'])
def listall():
    token = request.args.get('token')
    return dumps(channel_listall(token))

@APP.route('/channels/create', methods=['POST'])
def create_new_channel():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return dumps(channel_create(token, name, is_public))

##################
# ECHO FUNCTIONS #
##################

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
