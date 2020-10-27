''' Authorisation function tests '''
import pytest
from functions.auth import (auth_login, auth_register, auth_logout, auth_passwordreset_request,
                            auth_passwordreset_reset)
from functions.error import ValueError

# SETUP
auth_register('validemail@gmail.com', 'validpassw0rd', 'Alasdair', 'Cooper')
auth_register('goodemail@gmail.com', 'go0dpassword', 'Avi', 'Dargan')

################################################################################
# auth_login()                                                                 #
################################################################################

def test_login():
    ''' Test valid login attempt '''
    auth_login('validemail@gmail.com', 'validpassw0rd')

def test_switched_details():
    ''' Test valid details, but username and password from different accounts '''
    with pytest.raises(ValueError, match=r"*"):
        auth_login('validemail@gmail.com', 'go0dpassword')

def test_wrong_password():
    ''' Test incorrect password '''
    with pytest.raises(ValueError, match=r"*"):
        auth_login('validemail@gmail.com', 'wrongpassword')

def test_invalid_email():
    ''' Test invalid email '''
    with pytest.raises(ValueError, match=r"*"):
        auth_login('bademail', 'validpassw0rd')

def test_wrong_email():
    ''' Test valid but incorrect email '''
    with pytest.raises(ValueError, match=r"*"):
        auth_login('wrongemail@gmail.com', 'validpassw0rd')

################################################################################
# auth_logout()                                                                #
################################################################################

def auth_logout_test():
    ''' Test return value of any logout attempt '''
    assert auth_logout("12345") == {}

################################################################################
# auth_register()                                                              #
################################################################################

def test_invalid_email_register():
    ''' Test registration with invalid email '''
    with pytest.raises(ValueError, match=r"*"):
        auth_register('bademail', 'validpassw0rd', 'Alasdair', 'Cooper')

def test_email_in_use():
    ''' Test registration with email already in use '''
    with pytest.raises(ValueError, match=r"*"):
        auth_register('goodemail@gmail.com', 'go0dpassword', 'Avi', 'Dargan')

def test_invalid_pass():
    ''' Test registration with invalid password '''
    with pytest.raises(ValueError, match=r"*"):
        auth_register('email2@gmail.com', 'bad', 'Alasdair', 'Cooper')

def test_long_firstname():
    ''' Test registration with first name longer than 50 characters '''
    with pytest.raises(ValueError, match=r"*"):
        auth_register('email3@gmail.com', 'validpassw0rd',
                      'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'Cooper')

def test_long_lastname():
    ''' Test registration with last name longer than 50 characters '''
    with pytest.raises(ValueError, match=r"*"):
        auth_register('email4@gmail.com', 'validpassw0rd', 'Alasdair',
                      'Ccccccccccccccccccccccccccccccccccccccccccccccccccc')

################################################################################
# auth_passwordreset_request()                                                 #
################################################################################

def auth_passwordreset_request_test():
    ''' Test valid password reset request attempt '''
    # test for empty dictionary return value
    # assert auth_passwordreset_request(test_email) == {}

################################################################################
# auth_passwordreset_reset()                                                   #
################################################################################

def test_reset_newpass():
    ''' Test valid password reset attempt '''
    # SETUP
    reset_dict = auth_passwordreset_request('validemail@gmail.com')

    auth_passwordreset_reset(reset_dict['code'], 'newpassword')

    # TESTING
    auth_login('validemail@gmail.com', 'newpassword')      # test will fail if ValueError is raised

def test_reset_oldpass():
    ''' Try using the old password after changing it '''
    # SETUP
    reset_dict = auth_passwordreset_request('validemail@gmail.com')

    auth_passwordreset_reset(reset_dict['code'], 'validpassword')

    # TESTING
    with pytest.raises(ValueError, match=r"*"):
        auth_login('validemail@gmail.com', 'newpassw0rd')

def test_invalid_password():
    ''' Try changing the password to something invalid '''
    # SETUP
    reset_dict = auth_passwordreset_request('validemail@gmail.com')

    # TESTING
    with pytest.raises(ValueError, match=r"*"):
        auth_passwordreset_reset(reset_dict['code'], 'bad')

def test_invalid_code():
    ''' Try changing the password using an incorrect code '''
    # SETUP
    auth_passwordreset_request('validemail@gmail.com')

    # TESTING
    with pytest.raises(ValueError, match=r"*"):
        auth_passwordreset_reset('invalidcode', 'goodpassword')
