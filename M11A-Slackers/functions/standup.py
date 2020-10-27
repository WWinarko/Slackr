''' Standup functions for Slackr webapp '''
# Disable false positive "Unable to import"
# pylint: disable=E0401
from datetime import datetime, timedelta
from threading import Timer
from functions.auth import get_data, get_user_from_token
from functions.channel import get_channel_check_valid
from functions.messages import message_send
from functions.channel import channel_messages
from functions.error import ValueError, AccessError

STANDUPS = []

def get_standups():
    ''' Returns global standup variable '''
    global STANDUPS
    return STANDUPS

def find_standup(channel_id):
    ''' Function to find standup given channel id,
        or return None if no standup in given channel '''
    for standup in STANDUPS:
        if standup['channel_id'] == channel_id:
            return standup

    return None

def standup_start(token, channel_id, length):
    ''' Function to begin a standup '''
    data = get_data()
    standups = get_standups()
    channel_id = int(channel_id)
    length = int(length)

    # find channel (and check if channel_id does not belong to a channel)
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            standup_channel = channel
            break
    else:
        # loop completed without finding channel_id
        raise ValueError(description="Invalid channel ID")

    # check if standup currently running in channel
    if standup_channel['standup_running']:
        raise ValueError(description="Standup already running in this channel")

    # check if user is in the channel
    standup_user = get_user_from_token(token)
    if {'u_id' : standup_user['u_id'],} not in standup_channel['users']:
        raise AccessError(description="User not a member of channel")

    # start time and finish time
    start = datetime.now()
    start_time = start.timestamp()

    finish = start + timedelta(seconds=length)
    finish_time = finish.timestamp()

    standup_channel['standup_running'] = True

    # add standup to dictionary
    standups.append({
        'messages': [],
        'channel_id': channel_id,
        'time_start': start_time,
        'time_finish': finish_time,
    })

    # begin a timer, at the end of which the messages are sent
    # using the standup_timeout function below
    Timer(length, standup_timeout, [token, channel_id]).start()

    return {
        'time_finish': finish_time,
    }

def standup_timeout(token, channel_id):
    ''' Function to end a standup and send out the messages '''
    standups = get_standups()
    channel_id = int(channel_id)

    curr_standup = find_standup(channel_id)

    standup_channel = get_channel_check_valid(channel_id)
    standup_channel['standup_running'] = False

    # send standup
    full_standup = ""
    for message in curr_standup['messages']:
        full_standup += message['handle'] + ": " + message['message'] + "\n"

    # remove trailing newline
    full_standup.rstrip()

    message_send(token, channel_id, full_standup)

def standup_active(token, channel_id):
    ''' Function to check if a standup is currently active in a channel '''
    standups = get_standups()
    channel_id = int(channel_id)

    standup_channel = get_channel_check_valid(channel_id)

    if standup_channel is None:
        raise ValueError(description="Invalid channel ID")

    curr_standup = find_standup(channel_id)

    if standup_channel['standup_running']:
        time_finish = curr_standup['time_finish']
        return {
            'is_active': True,
            'time_finish': time_finish,
        }

    return {
        'is_active': False,
        'time_finish': None,
    }

def standup_send(token, channel_id, message):
    ''' Function to send a message to a standup '''
    data = get_data()
    standups = get_standups()
    channel_id = int(channel_id)

    # find channel (and check if channel_id does not belong to a channel)
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            standup_channel = channel
            break
    else:
        # loop completed without finding channel_id
        raise ValueError(description="Invalid channel ID")

    # check if standup currently running in channel
    if not standup_channel['standup_running']:
        raise ValueError(description="No standup running in this channel")

    # check message is shorter than 1000 chars
    if len(message) > 1000:
        raise ValueError(description="Message too long")

    # check if user is in the channel
    standup_user = get_user_from_token(token)
    if {'u_id' : standup_user['u_id'],} not in standup_channel['users']:
        raise AccessError(description="User not a member of channel")

    # find standup and raise value error if none exists
    curr_standup = find_standup(channel_id)
    
    if curr_standup is None:
        raise ValueError(description="No standup running in this channel")

    # add message and name of user to list of messages
    message_sender = get_user_from_token(token)

    message_dict = {
        'message': message,
        'handle': message_sender['handle_str'],
    }

    curr_standup['messages'].append(message_dict)

    return {}
