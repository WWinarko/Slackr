import pytest
from functions.channel import (channel_create, channel_invite, channel_details, channel_messages, channel_leave,
                               channel_join, channel_addowner, channel_removeowner, channel_list, channel_listall)
from functions.auth import auth_register, get_data
from functions.error import ValueError, AccessError

#first hard add two users to the server data
user1 = auth_register('test1@email.com','135ac246dc','sam','jacobs')
user2 = auth_register('test2@email.com','135ac246dc','kim','jacobs')
user3 = auth_register('test3@email.com','135ac246dc','kate','jacobs')

#create a channel owned by user1
def test_channel_create():
    assert channel_create(user1['token'],'test_channel',True) == {'channel_id' : 0}

    #run a call to channel_create which will raise ValueError()'s
    
    with pytest.raises(ValueError):
        channel_create(user1['token'],'this_name_is_too_long',True)
    

#attempt to invite user2 to test_channel
def test_channel_invite():
    #first run a few bad calls to channel_invite which will raise ValueError()'s
    with pytest.raises(ValueError):
        channel_invite(user2['token'],0,user2['u_id'])
    
    with pytest.raises(ValueError):
        channel_invite(user1['token'],0,'-100') #invalid u_id
    
    with pytest.raises(ValueError):
        channel_invite(user1['token'],-100,user2['u_id'])
    
    #now run a good call to channel_invite 
    assert channel_invite(user1['token'],0,user2['u_id']) == {}

def test_channel_details():
    #first run a few bad calls to channel_details which will raise ValueError()'s
    with pytest.raises(ValueError):
        channel_details(user1['token'],-100)
    
    with pytest.raises(ValueError):
        channel_details(user3['token'],0)

    #now run a good call to channel_details
    {'u_id' : user1['u_id'],'name_first' : 'sam','name_last' : 'jacobs',}
    assert channel_details(user1['token'],0) == {'name' : 'test_channel','owner_members' : [{'u_id' : user1['u_id'],'name_first' : 'sam','name_last' : 'jacobs',}],'all_members' : [{'u_id' : user1['u_id'],'name_first' : 'sam','name_last' : 'jacobs',}, {'u_id' : user2['u_id'],'name_first' : 'kim','name_last' : 'jacobs',}]}

def test_channel_messages():
    pass

def test_channel_leave():
    #first run a bad call to channel_leave which will raise ValueError()'s
    with pytest.raises(ValueError):
        channel_leave(user2['token'],-100)
    
    #now run a good call to channel_leave
    assert channel_leave(user2['token'],0) == {}

def test_channel_join():
    #first run a few bad calls to channel_join which will raise ValueError()'s
    with pytest.raises(ValueError):
        channel_join(user2['token'],-100)
    
    with pytest.raises(ValueError):
        data = get_data()
        for channel in data['channels']:
            channel['is_private'] = True
        
        channel_join(user2['token'],0)

    data = get_data()
    for channel in data['channels']:
        channel['is_private'] = False

    
    #now run a good call to channel_join
    assert channel_join(user2['token'],0) == {}

def test_channel_addowner():
    #first run a few bad calls to channel_addowner which will raise ValueError()'s
    with pytest.raises(ValueError):
        channel_addowner(user1['token'],-100,user2['u_id'])
    
    with pytest.raises(ValueError):
        channel_addowner(user1['token'],0,user1['u_id'])
    
    with pytest.raises(ValueError):
        channel_addowner(user2['token'],0,user2['u_id'])
    
    #now run a good call to channel_addowner
    channel_join(user2['token'],0)
    assert channel_addowner(user1['token'],0,user2['u_id']) == {}


def test_channel_removeowner():
    #first run a few bad calls to channel_removeowner which will raise ValueError()'s
    with pytest.raises(ValueError):
        channel_removeowner(user1['token'],-100,user2['u_id'])
    
    with pytest.raises(ValueError):
        channel_removeowner(user1['token'],0,user3['u_id'])
    
    with pytest.raises(ValueError):
        channel_removeowner(user3['token'],0,user1['u_id'])
    
    #now run a good call to channel_removeowner
    assert channel_removeowner(user1['token'],0,user2['u_id']) == {}

def test_channel_list():
    assert channel_list(user1['token']) == {'channels' : [{'channel_id' : 0, 'name' : 'test_channel'}]}

def test_channel_listall():
    assert channel_list(user1['token']) == {'channels' : [{'channel_id' : 0, 'name' : 'test_channel'}]}
