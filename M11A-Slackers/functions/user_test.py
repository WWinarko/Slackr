''' Test for user.py functions'''
################################################################################
# user_tests.py                                                                #
################################################################################
# pylint: disable= C0103, C0330, W0105, W0622
import pytest
from functions.error import ValueError
from functions.user import (user_profile, user_profile_setemail, user_profile_sethandle,
                            user_profile_setname, users_all)
from functions.auth import auth_register, generate_token

auth_register_dict1 = auth_register('wincent@gmail.com', '12345678', 'Wincent', 'Winarko')
auth_register_dict2 = auth_register('jonathan@gmail.com', '12345678', 'Jonathan', 'Lee')
TOKEN = auth_register_dict1['token']
U_ID = auth_register_dict1['u_id']

################################################################################
# user_profile()                                                               #
################################################################################

def test_user_profile():
    ''' Test for getting user profile from u_id '''
    # TESTING
    # test for valid u_id
    assert user_profile(TOKEN, U_ID) == {
        'u_id': 1, 'email': 'wincent@gmail.com', 'name_first': 'Wincent',
        'profile_img_url': None, 'name_last': 'Winarko', 'handle_str': 'wincentwinarko'
    }
    with pytest.raises(ValueError):
        # test for u_id not a valid user
        user_profile(TOKEN, 3)
    invalid_token = generate_token(5)
    with pytest.raises(ValueError):
        # test for invalid token
        user_profile(invalid_token, 1)


################################################################################
# user_profile_setname()                                                       #
################################################################################

def test_user_profile_setname():
    ''' Test for changing user's first and last name '''
    assert user_profile_setname(TOKEN, "Frankie", "Willis") is None

    with pytest.raises(ValueError):
        user_profile_setname(
            TOKEN, "this_is_definitely_an_invalid_last_name_which_will_raise_a_value_error",
            "Willis"
        )

    with pytest.raises(ValueError):
        user_profile_setname(
            TOKEN, "Willis",
            "this_is_definitely_an_invalid_last_name_which_will_raise_a_value_error"
        )

################################################################################
# user_profile_sethandle()                                                     #
################################################################################

def test_user_profile_sethandle():
    ''' Test for changing user's handle '''
    with pytest.raises(ValueError):
        user_profile_sethandle(TOKEN, "ww")

    with pytest.raises(ValueError):
        user_profile_sethandle(TOKEN, "jonathanlee")

    assert user_profile_sethandle(TOKEN, "robertocarlos") is None

################################################################################
# user_profile_setemail()                                                      #
################################################################################

def test_user_profile_setemail():
    ''' Test for changing user's email '''
    with pytest.raises(ValueError):
        user_profile_setemail(TOKEN, "wincent000.com")

    with pytest.raises(ValueError):
        user_profile_setemail(TOKEN, "jonathan@gmail.com")

    assert user_profile_setemail(TOKEN, "winarko@gmail.com") is None

################################################################################
# users_all()                                                                  #
################################################################################

def test_users_all():
    ''' Test for getting all users in database'''
    assert users_all(TOKEN) == {
        'users' : [{'u_id': 1, 'email': 'winarko@gmail.com', 'name_first': 'Frankie',
                'name_last': 'Willis', 'handle_str': 'robertocarlos', 'profile_img_url': None},
                {'u_id': 2, 'email': 'jonathan@gmail.com', 'name_first': 'Jonathan',
                'name_last': 'Lee', 'handle_str': 'jonathanlee', 'profile_img_url': None}]
    }

    # check for invalid token
    invalid_token = generate_token(5)
    with pytest.raises(ValueError):
        users_all(invalid_token)

'''
################################################################################
# user_profiles_uploadphoto()                                                  #
################################################################################

def test_user_profile_uploadphoto():
    assert user_profile_uploadphoto("123456","test_url.com/image",0,0,512,512) == {}

    with pytest.raises(ValueError):
        user_profile_uploadphoto("123456","bad_url.com",0,0,512,512)

    with pytest.raises(ValueError):
        user_profile_uploadphoto("123456","test_url.com/image",-1,0,512,512)'''
