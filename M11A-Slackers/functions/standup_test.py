''' Authorisation function tests '''
from time import sleep
import pytest
from functions.auth import auth_register
from functions.channel import channel_create
from functions.standup import standup_start, standup_send, standup_active
from functions.error import ValueError, AccessError

# SETUP

# channel creator
USER_DICT = auth_register('validemail2@gmail.com', 'validpassw0rd', 'Alasdair', 'Cooper')
TOKEN = USER_DICT['token']

# standup channel
CHANNEL_ID_DICT = channel_create(TOKEN, "test channel", False)
CHANNEL_ID = CHANNEL_ID_DICT['channel_id']

USER2_DICT = auth_register('goodemail2@gmail.com', 'goodpassw0rd', 'Avi', 'Dargan')
TOKEN2 = USER2_DICT['token']

################################################################################
# standup_start()                                                              #
################################################################################

def test_start():
    ''' Test valid standup start '''
    standup_start(TOKEN, CHANNEL_ID, 2)

def test_invalid_channel():
    ''' Test start on nonexistent channel '''
    sleep(3)

    with pytest.raises(ValueError, match=r"*"):
        standup_start(TOKEN, 12345, 2)

def test_active_standup():
    ''' Test start on channel with standup already active '''
    sleep(3)

    standup_start(TOKEN, CHANNEL_ID, 2)

    with pytest.raises(ValueError, match=r"*"):
        standup_start(TOKEN, CHANNEL_ID, 2)

def test_non_member():
    ''' Test start when user is not a member of the channel '''
    sleep(3)

    channel2_id_dict = channel_create(TOKEN, "test channel", False)
    channel2_id = channel2_id_dict['channel_id']

    with pytest.raises(AccessError, match=r"*"):
        standup_start(TOKEN2, channel2_id, 2)

################################################################################
# standup_active()                                                               #
################################################################################

def test_active():
    ''' Test standup_active when standup active '''
    sleep(3)

    standup_start(TOKEN, CHANNEL_ID, 2)

    assert standup_active(TOKEN, CHANNEL_ID)['is_active']

def test_not_active():
    ''' Test standup_active when standup not active '''
    sleep(3)

    assert not standup_active(TOKEN, CHANNEL_ID)['is_active']
    assert standup_active(TOKEN, CHANNEL_ID)['time_finish'] is None

################################################################################
# standup_send()                                                               #
################################################################################

def test_send():
    ''' Test sending a message to standup '''
    standup_start(TOKEN, CHANNEL_ID, 2)
    ret = standup_send(TOKEN, CHANNEL_ID, "Hello")
    assert ret == {}

def test_invalid_channel_send():
    ''' Test sending a message to a nonexistent channel's standup '''
    sleep(3)

    with pytest.raises(ValueError, match=r"*"):
        standup_send(TOKEN, 12345, "Hello")

def test_long_message():
    ''' Test sending a message over 1000 characters to a standup '''
    message = ""
    for _ in range(1010):
        message += "a"

    standup_start(TOKEN, CHANNEL_ID, 2)

    with pytest.raises(ValueError, match=r"*"):
        standup_send(TOKEN, CHANNEL_ID, message)

def test_no_standup():
    ''' Test sending a message to a channel with no standup active '''
    sleep(3)

    channel3_id_dict = channel_create(TOKEN, "test channel 2", False)
    channel3_id = channel3_id_dict['channel_id']

    with pytest.raises(ValueError, match=r"*"):
        standup_send(TOKEN, channel3_id, "Hello")

def test_non_member_send():
    ''' Test user who is not a member of channel attempting to send a message to standup '''
    standup_start(TOKEN, CHANNEL_ID, 2)

    with pytest.raises(AccessError, match=r"*"):
        standup_send(TOKEN2, CHANNEL_ID, "Hello")
