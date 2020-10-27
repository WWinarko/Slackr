import pytest
from functions.auth import get_data, auth_register
from functions.messages import message_send
from functions.channel import channel_create, channel_invite
from functions.search import search

def test_search():
    pass
'''
    #SETUP   
    authRegDict1 = auth_register('wincent@gmail.com', '12345678', 'Wincent', 'Winarko')
    authRegDict2 = auth_register('jonathan@gmail.com', '12345678', 'Jonathan', 'Lee')
    token1 = authRegDict1['token']
    token2 = authRegDict2['token']
    # Create a channel.
    channels = {'channel_id' : []}
    channels['channel_id'].append(channel_create(token1, 'Channel 1', False))
    channels['channel_id'].append(channel_create(token1, 'Channel 2', False))
    channels['channel_id'].append(channel_create(token1, 'Channel 3', True))
    
    channel_invite(token1, 0, 2)    
    
    message_send(token2, 0, "This message for testing purpose only")
    message_send(token1, 1, "This message is also for testing purpose only")
    message_send(token1, 2, "This message for nothing")
    
    messages = search(token1,"testing")
    message_ids = []
    for message_id in messages['message_id']:
        message_ids.append(message_id)
        
    assert message_ids == [0,1]
    
    assert messages == [{'message_id': 0, 'u_id': 2, 'channel_id': 0, 'message': 'This message for testing purpose only', 
    'time_created': 1572192891.264463, 'reacts': {'react_id': 0, 'u_ids': [], 'is_this_user_reacted': 0}, 'is_pinned': 0}, 
    {'message_id': 1, 'u_id': 1, 'channel_id': 1, 'message': 'This message is also for testing purpose only', 
    'time_created': 1572192891.264543, 'reacts': {'react_id': 0, 'u_ids': [], 'is_this_user_reacted': 0}, 'is_pinned': 0}]'''
