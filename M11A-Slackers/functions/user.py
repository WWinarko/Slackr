''' User functions for Slackr webapp '''
# pylint: disable= W0622, R1720, C0411, R0913
import urllib.request
from flask import request
from PIL import Image
import imghdr
from functions.error import ValueError
from functions.auth import (get_data, get_user_from_token, check_valid_email, check_name_length,
                            get_user_from_email, get_user_from_uid)

def check_valid_token(token):
    ''' Function for checking valid token '''
    data = get_data()
    user_dict = get_user_from_token(token)
    for user in data['users']:
        if user == user_dict:
            return True
    return False

def check_handle_length(handle_str):
    ''' Function for checking handle's length '''
    if len(handle_str) < 3 or len(handle_str) > 20:
        return False
    return True

def check_used_handle(handle_str):
    ''' Function for used handle '''
    data = get_data()
    for user in data['users']:
        if user['handle_str'] == handle_str:
            return True
    return False


def check_http_status(img_url):
    ''' Function for checking img_url http status '''
    image_url = urllib.request.urlopen(img_url)
    if image_url.status != 200:
        raise ValueError(
            description="img_url is returns an HTTP status other than 200")

def check_coordinate(width, height, x_start, y_start, x_end, y_end):
    ''' Function for checking given coordinates before cropping '''
    if x_end > width or y_end > height:
        raise ValueError(description="coordinate not within the dimension of the image")

    elif x_end <= x_start or y_end <= y_start:
        raise ValueError(description="Invalid coordinate")

def crop_image(img_url, x_start, y_start, x_end, y_end):
    ''' Function for cropping image according to coordinates '''
    image_object = Image.open(img_url)
    width, height = image_object.size
    check_coordinate(width, height, x_start, y_start, x_end, y_end)
    cropped = image_object.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_url)

def get_users():
    ''' Function for collecting all users in database '''
    data = get_data()
    users = []
    for user_dict in data['users']:
        users.append({
            'u_id': user_dict['u_id'],
            'email': user_dict['email'],
            'name_first': user_dict['name_first'],
            'name_last': user_dict['name_last'],
            'handle_str': user_dict['handle_str'],
            'profile_img_url': user_dict['profile_img_url']

        })
    return users


def user_profile(token, u_id):
    ''' Function for get user data '''
    user_dict = get_user_from_uid(u_id)
    if user_dict is None:
        raise ValueError(description="Invalid u_id")
    if not check_valid_token(token):
        raise ValueError(description="Invalid token")

    user = {
        'u_id': user_dict['u_id'],
        'email': user_dict['email'],
        'name_first': user_dict['name_first'],
        'name_last': user_dict['name_last'],
        'handle_str': user_dict['handle_str'],
        'profile_img_url': user_dict['profile_img_url']
        }
    return user
def user_profile_setname(token, name_first, name_last):
    ''' Function for set user's first name and last name '''
    if not check_name_length(name_first) or not check_name_length(name_last):
        raise ValueError(description="name length must in between 1 and 50")
    user_dict = get_user_from_token(token)
    user_dict['name_first'] = name_first
    user_dict['name_last'] = name_last

def user_profile_setemail(token, email):
    ''' Function for set user's email '''
    if not check_valid_email(email):
        raise ValueError(description="Invalid email")

    if get_user_from_email(email) is not None:
        raise ValueError(description="Email already in use")

    user_dict = get_user_from_token(token)
    user_dict['email'] = email

def user_profile_sethandle(token, handle_str):
    ''' Function for set user's handle '''
    if not check_handle_length(handle_str):
        raise ValueError(description='Handle length must in between 3 and 20')
    if check_used_handle(handle_str):
        raise ValueError(description='Handle has been used')

    user_dict = get_user_from_token(token)
    user_dict['handle_str'] = handle_str

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    ''' Function for uploading foto as user profile picture '''
    # check http status
    check_http_status(img_url)
    # get user dict
    user_dict = get_user_from_token(token)
    u_id = user_dict['u_id']
    #retrive the image and store to local server
    profile_img_url = "profile_imgs/{}.jpg".format(u_id)
    urllib.request.urlretrieve(img_url, profile_img_url)
    if imghdr.what(profile_img_url) != 'jpeg':
        raise ValueError(description="Image uploaded is not a JPG")
    # crop and save the image
    crop_image(profile_img_url, int(x_start), int(y_start), int(x_end), int(y_end))
    # store the cropped image as profile image
    user_dict['profile_img_url'] = request.host_url + profile_img_url

def users_all(token):
    ''' Function for collecting all the users in database '''
    if not check_valid_token(token):
        raise ValueError(description="invalid token")
    users = get_users()
    return {
        'users': users,
    }
