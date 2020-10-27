''' Message functions for Slackr webapp '''
from datetime import datetime, timezone
from threading import Timer
from functions.error import AccessError, ValueError
from functions.auth import get_data, get_user_from_token

# global constant to track the message IDs.
MESSAGE_ID_COUNTER = 0

def getMessageFromID(message_id):
    ''' Function which returns a message dictionary given the message id '''

    data = get_data()

    # loop through data dictionary for message with matching id.
    for message in data['messages']:
        if message['message_id'] == int(message_id):
            return message

    # if it gets here there is no such message
    return None

def check_user_reacted(token, message_id):
    ''' Function to check if the user has reacted to a message '''

    user_dict = get_user_from_token(token)
    u_id = user_dict['u_id']

    message_dict = getMessageFromID(message_id)
    for user_id in message_dict['reacts'][0]['u_ids']:
        if user_id == u_id:
            message_dict['reacts'][0]['is_this_user_reacted'] = True
            return True
        else:
            message_dict['reacts'][0]['is_this_user_reacted'] = False

    return False

def react_message(token, message_id, react_id):
    ''' Function allowing user to react to a message '''

    # get user and user id.
    user_dict = get_user_from_token(token)
    u_id = int(user_dict['u_id'])

    message_dict = getMessageFromID(message_id)

    # add react to the message.
    message_dict['reacts'][0]['u_ids'].append(u_id)
    message_dict['reacts'][0]['is_this_user_reacted'] = True

def unreact_message(token, message_id, react_id):
    ''' Function allowing user to unreact to a message '''

    # get user and user id.
    user_dict = get_user_from_token(token)
    u_id = int(user_dict['u_id'])

    message_dict = getMessageFromID(message_id)

    # remove the react from the message.
    message_dict['reacts'][0]['u_ids'].remove(u_id)
    message_dict['reacts'][0]['is_this_user_reacted'] = False

def message_send(token, channel_id, message):
    ''' Function allowing user to send a message '''

    # Certain imports are done within functions due to issues with
    # circular dependencies
    from functions.channel import get_channel_check_valid, isUIDInChannel

    data = get_data()

    global MESSAGE_ID_COUNTER

    # raise ValueError if message is longer than 1000 characters
    if len(message) > 1000:
        raise ValueError(description="Message too long.")

    # get user_id from token
    user = get_user_from_token(token)

    # raise AccessError if user does not exist.
    if user is None:
        raise AccessError(description="No such user.")

    # raise access error if user is not in channel
    if not isUIDInChannel(user['u_id'], channel_id):
        raise AccessError(description="User is not in channel.")

    # lock in current time in unix epoch time
    now = datetime.now().timestamp()

    # define new reacts dictionary
    reacts = {
        "react_id" : 1,
        "u_ids" : [],
        "is_this_user_reacted" : False,
    }

    # define new message object
    messageObject = {
        "message_id" : MESSAGE_ID_COUNTER,
        "u_id" : user['u_id'],
        "channel_id" : channel_id,
        "message" : message,
        "time_created" : now,
        "reacts" : [reacts],
        "is_pinned" : 0,
    }

    # increment message ids
    MESSAGE_ID_COUNTER += 1

    # get channel dict from channel_id
    channelObj = get_channel_check_valid(channel_id)

    # append new message to list of messages
    data['messages'].append(messageObject)
    channelObj['messages'].append(messageObject["message_id"])
    # return only the message id
    return {messageObject["message_id"]}

def message_sendlater(token, channel_id, message, time_sent):
    ''' Function allowing a user to send a message after a certain delay '''

    from functions.channel import get_channel_check_valid, isUIDInChannel

    # raise ValueError if message is longer than 1000 characters
    if len(message) > 1000:
        raise ValueError(description="Message is too large.")

    # raise ValueError if channel does not exist.
    if get_channel_check_valid(channel_id) is None:
        raise ValueError(description="Invalid channel.")

    # get user_id from token
    user = get_user_from_token(token)

    # raise AccessError if user doesnt exist.
    if user is None:
        raise AccessError(description="No such user.")

    # raise access error if user is not in channel
    if not isUIDInChannel(user['u_id'], channel_id):
        raise AccessError(description="User is not in channel.")

    # check that the user is not trying to send a message in the past.
    now = datetime.now().timestamp()

    timeToSend = float(time_sent)

    if now > timeToSend:
        raise ValueError(description="Cannot send message in the past.")

    # calculate when to send the message.
    secondsToSend = int(timeToSend - now)

    # start a timer thread to send that message.
    timer = Timer(secondsToSend, lambda: message_send(token, channel_id, message))
    timer.start()

    # since timer drops the message_id, we can just return the global message id
    return MESSAGE_ID_COUNTER

def message_remove(token, message_id):
    ''' Function allowing a user to delete their own messages '''
    from functions.channel import get_channel_check_valid, isUIDOwnerChannel

    data = get_data()

    # raise ValueError if message_id does not exist.
    if getMessageFromID(message_id) is None:
        raise ValueError(description="Message with corresponding ID not found.")

    user = get_user_from_token(token)
    message = getMessageFromID(message_id)

    # raise AccessError if the user does not have permission to delete message.
    if message['u_id'] != user['u_id']:
        if not isUIDOwnerChannel(user['u_id'], message['channel_id']):
            raise AccessError(description="You do not have permission to delete this message.")


    channelObj = get_channel_check_valid(message['channel_id'])

    # remove the message from both data structures.
    channelObj['messages'].remove(int(message_id))
    data['messages'].remove(message)

    return {}

def message_edit(token, message_id, message):
    ''' Function allowing a user to edit their own messages '''

    # if message is empty, we just want to delete it.
    if message == "":
        return message_remove(token, message_id)

    # otherwise we just want to edit the message
    from functions.channel import isUIDOwnerChannel

    user = get_user_from_token(token)

    messageObject = getMessageFromID(message_id)

    # raise an AccessError if the user is not the original poster or an admin.
    if messageObject['u_id'] != user['u_id']:
        if not isUIDOwnerChannel(user['u_id'], messageObject['channel_id']):
            raise AccessError(description="You do not have permission to edit the message.")

    # edit the message.
    messageObject['message'] = message

    return {}

def message_react(token, message_id, react_id):
    ''' Function allowing users to react to messages '''
    # raise ValueError if the message doesn't exist. return value is not used.
    if getMessageFromID(message_id) is None:
        raise ValueError(description="Message with corresponding ID not found.")

    # raise value error if invalid react id, or if user has already reacted to this message.
    if int(react_id) != 1:
        raise ValueError(description="React_id is not a valid React ID")
    if check_user_reacted(token, message_id):
        raise ValueError(description="Authorised user has already reacted to this message")

    # add react to message.
    react_message(token, message_id, react_id)

    return {}

def message_unreact(token, message_id, react_id):
    ''' Function allowing a user to remove their reaction from a message '''

    # raise ValueError if the message doesn't exist.
    if getMessageFromID(message_id) is None:
        raise ValueError(description="Message with corresponding ID not found.")

    # raise value error if invalid react id, or if user has not reacted to this message.
    if int(react_id) != 1:
        raise ValueError(description="React_id is not a valid React ID")
    if not check_user_reacted(token, message_id):
        raise ValueError(description="Authorised user has not reacted to this message")

    # remove react from message.
    unreact_message(token, message_id, react_id)

    return {}

def message_pin(token, message_id):
    ''' Function allowing a channel owner to pin a message '''

    # raise ValueError if message_id does not exist.
    if getMessageFromID(message_id) is None:
        raise ValueError(description="Message with corresponding ID not found.")

    user = get_user_from_token(token)

    # raise access error if user is not permitted to unpin.
    if user['permission_id'] > 2:
        raise AccessError(description="You do not have permission to pin this message.")

    message = getMessageFromID(message_id)

    # raise value error if message is already pinned.
    if message['is_pinned'] == 1:
        raise ValueError(description="Message is already pinned.")

    # otherwise just pin.
    message['is_pinned'] = 1

    return {}

def message_unpin(token, message_id):
    ''' Function allowing a channel owner to unpin a message '''

    # raise ValueError if message_id does not exist.
    if getMessageFromID(message_id) is None:
        raise ValueError(description="Message with corresponding ID not found.")

    user = get_user_from_token(token)

    # raise access error if user is not permitted to unpin.
    if user['permission_id'] > 2:
        raise AccessError(description="You do not have permission to unpin this message.")

    message = getMessageFromID(message_id)

    # raise value error if message is already unpinned.
    if message['is_pinned'] == 0:
        raise ValueError(description="Message is already unpinned.")

    # otherwise just unpin.
    message['is_pinned'] = 0

    return {}
