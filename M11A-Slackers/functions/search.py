''' Search functions for Slackr webapp '''
# pylint: disable=C0330
from functions.auth import get_user_from_token
from functions.channel import getListOfUsersChannels, get_channel_check_valid, getMessageFromID


def find_message(messages_list, messages, string):
    '''Function for finding messages from channels that user joined'''
    for message_id in messages_list:
        message = getMessageFromID(message_id)
        if string in message['message']:
            messages.append({
            'message_id': message['message_id'],
            'u_id': message['u_id'],
            'message': message['message'],
            'time_created': message['time_created'],
            'reacts': message['reacts'],
            'is_pinned': message['is_pinned'],
            })

def search(token, query_str):
    ''' Function for search messages with given string from channels that user joined '''

    user_dict = get_user_from_token(token)
    messages = []
    channel_list = getListOfUsersChannels(user_dict['u_id'])
    for channel in channel_list:
        current_channel = get_channel_check_valid(channel['channel_id'])
        messages_list = current_channel['messages']
        find_message(messages_list, messages, query_str)
    return messages
