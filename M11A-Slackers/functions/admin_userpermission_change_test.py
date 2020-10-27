''' Admin functions test for Slackr webapp '''
# pylint: disable=W0622
import pytest
from functions.error import AccessError, ValueError
from functions.admin import admin_userpermission_change
from functions.auth import auth_register, get_user_from_token


def test_admin_userpermission_change():
    ''' test for change user permission by an admin or owner '''
    auth_dict1 = auth_register('wincent@gmail.com', '12345678', 'Wincent', 'Winarko')
    auth_dict2 = auth_register('jonathan@gmail.com', '12345678', 'Jonathan', 'Lee')
    token1 = auth_dict1['token']
    token2 = auth_dict2['token']

    with pytest.raises(ValueError):
        admin_userpermission_change(token1, 5, 3)

    with pytest.raises(ValueError):
        admin_userpermission_change(token1, 2, 4)

    with pytest.raises(AccessError):
        admin_userpermission_change(token2, 1, 3)

    # owner change member to admin
    admin_userpermission_change(token1, 2, 2)
    assert get_user_from_token(token2)['permission_id'] == 2

    with pytest.raises(AccessError):
        admin_userpermission_change(token2, 1, 1)

    # owner change admin to owner
    admin_userpermission_change(token1, 2, 1)
    assert get_user_from_token(token2)['permission_id'] == 1
    # owner change owner to admin
    admin_userpermission_change(token2, 1, 2)
    assert get_user_from_token(token1)['permission_id'] == 2
    # owner change admin to member
    admin_userpermission_change(token2, 1, 3)
    assert get_user_from_token(token1)['permission_id'] == 3
    # admin change member to admin
    admin_userpermission_change(token2, 2, 2)
    admin_userpermission_change(token2, 1, 2)
    assert get_user_from_token(token1)['permission_id'] == 2
    # admin change admin to member
    admin_userpermission_change(token1, 2, 3)
    assert get_user_from_token(token2)['permission_id'] == 3
