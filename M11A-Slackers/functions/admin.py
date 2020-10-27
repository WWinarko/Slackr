''' Admin functions for Slackr webapp '''
# pylint: disable=E0401, W0622
from functions.error import AccessError, ValueError
from functions.auth import get_user_from_token, get_user_from_uid

def check_permission_id(permission_id):
    ''' Function to check permission_id '''
    if permission_id not in range(1, 4):
        return False
    return True
def check_user_permission(user_dict, permission_id):
    '''Function to check authorised privilege to change user permission'''
    if (user_dict['permission_id'] == 2 and permission_id == 1) or user_dict['permission_id'] == 3:
        return False
    return True

def change_permission(u_id, permission_id):
    ''' Function to change user's permission id '''
    user_dict2 = get_user_from_uid(u_id)
    user_dict2['permission_id'] = permission_id

def admin_userpermission_change(token, u_id, permission_id):
    ''' Function to change user's permission based on given permission_id '''
    # check given u_id refer to valid u_id
    if not get_user_from_uid(int(u_id)):
        raise ValueError(description='Invalid u_id')
    # check given permission_id refer to valid permission_id
    if not check_permission_id(int(permission_id)):
        raise ValueError(description='Invalid permission_id')
    user_dict1 = get_user_from_token(token)
    # check the authorised user is an admin or owner
    if not check_user_permission(user_dict1, int(permission_id)):
        raise AccessError('The authorised user is not an admin or owner')
    # change the permission id
    change_permission(int(u_id), int(permission_id))
