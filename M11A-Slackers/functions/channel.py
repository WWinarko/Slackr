from functions.auth import get_data, get_user_from_token, get_user_from_uid
from functions.messages import getMessageFromID
from functions.error import ValueError, AccessError

#IMPORTANT
nextUnusedChannelId = 0

#THIS IS JUST A REPRESENTATION OF WHAT A CHANNEL STRUCTURE LOOKS LIKE
#CHANNEL STRUCTURES WILL SIT INSIDE THE LIST AT PATH data['channels']
channelStructure = {
    'name': "test_name",
    'channel_id': 1,
    'messages': [],
    'users': [],
    'owners': [],
    'is_private': True,
    'standup_running': False,
}

#THIS IS JUST A REPRESENTATION OF WHAT A USER STRUCTURE LOOKS LIKE
#USER STRUCTURES WILL GO INSIDE THE LIST AT PATH data['channels']['ANY_CHANNEL']['users']
userStructure = {
    'u_id': 1,
}

#IF YOU WANT TO GET DATA ON A USER IN A CHANNEL USE THE get_user_from_uid() function from user.py @Wincent

#DRY functions


def get_user_check_valid(token):
    userFromToken = get_user_from_token(token)  # function from auth branch

    # function from user branch
    if get_user_from_uid(userFromToken['u_id']) == False:
        raise ValueError()

    return userFromToken


def get_channel_check_valid(channel_id):
    data = get_data()
    channel_id = int(channel_id)
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    raise ValueError("Channel_id not refer to valid channel")


#BEGIN INTERFACE FUNCTIONS
def makeUIDOwnerChannel(u_id, channel_id):
    data = get_data()

    channel = get_channel_check_valid(channel_id)

    if channel == None:
        raise ValueError()
    else:
        if {'u_id': u_id} not in channel['owners']:
            channel['owners'].append({'u_id': u_id})


def removeUIDOwnerChannel(u_id, channel_id):
    data = get_data()

    channel = get_channel_check_valid(channel_id)

    if channel == None:
        raise ValueError()
    else:
        if {'u_id': u_id} in channel['owners']:
            channel['owners'].remove({'u_id': u_id})


def isUIDOwnerChannel(u_id, channel_id):
    data = get_data()

    channel = get_channel_check_valid(channel_id)

    if channel == None:
        raise ValueError()
    else:
        return {'u_id': u_id} in channel['owners']


def getChannelNameFromID(channel_id):
    data = get_data()

    channel = get_channel_check_valid(channel_id)

    if channel != None:
        return channel['name']
    else:
        return None


def getChannelMessagesFromId(channel_id):
    data = get_data()

    channel = get_channel_check_valid(channel_id)

    if channel != None:
        return channel['messages']
    else:
        return None


def getListOfUsersChannels(u_id):
    data = get_data()

    returnList = []
    for channel in data['channels']:
        if isUIDInChannel(u_id, channel['channel_id']):
            returnList.append(
                {'name': channel['name'], 'channel_id': channel['channel_id'], })

    return returnList


def isUIDInChannel(u_id, channel_id):
    data = get_data()
    u_id = int(u_id)
    channel_id = int(channel_id)
    for channel in data['channels']:
        if int(channel['channel_id']) == channel_id:
            for user in channel['users']:
                if int(user['u_id']) == u_id:
                    return True

    return False
#END INTERFACE FUNCTIONS


def channel_invite(token, channel_id, u_id):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    # this is variable we use to hold the channel we are trying to maniupulate
    currentChannel = get_channel_check_valid(channel_id)

    if isUIDInChannel(userFromToken['u_id'], channel_id) == False:
        raise AccessError(description="User is not in the channel")  # this should be an AccessError()

    if isUIDInChannel(u_id, channel_id):
         return {}  # no need to do more work as the user we are trying to add is already a member of the channel
    from functions.admin import get_user_from_uid
    #if we haven't returned by now we need to add the user to the channel
    userToAdd = get_user_from_uid(u_id)  # function from user branch

    if userToAdd == None:
        raise ValueError()
    else:
        if userToAdd['permission_id'] < 3:
            makeUIDOwnerChannel(userToAdd['u_id'], channel_id)
        currentChannel['users'].append(
            {'u_id': userToAdd['u_id'], })  # add the user

    return {}  # finally return


def channel_details(token, channel_id):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    currentChannel = get_channel_check_valid(channel_id)

    #verify the authorised user is a member of the channel
    if isUIDInChannel(userFromToken['u_id'], channel_id) == False:
        raise AccessError(
            description='Authorised user is not a member of channel with channel_id')

    #if we have reached this point it is safe to return the channel details
    ownerMembers = []
    allMembers = []

    from functions.user import user_profile

    for entry in currentChannel['owners']:
        ownerToAdd = user_profile(token, entry['u_id'])
        if ownerToAdd != None:
            ownerMembers.append(
                {'u_id': entry['u_id'], 'name_first': ownerToAdd['name_first'], 'name_last': ownerToAdd['name_last'], 'profile_img_url': ownerToAdd['profile_img_url'],})

    for entry in currentChannel['users']:
        userToAdd = user_profile(token, entry['u_id'])
        if userToAdd != None:
            allMembers.append(
                {'u_id': entry['u_id'], 'name_first': userToAdd['name_first'], 'name_last': userToAdd['name_last'], 'profile_img_url': userToAdd['profile_img_url'],})

    return {'name': currentChannel['name'], 'owner_members': ownerMembers, 'all_members': allMembers}


def channel_messages(token, channel_id, start):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    currentChannel = get_channel_check_valid(channel_id)
    #if start is greater than the number of messages in the channel raise ValueError()
    if int(start) > len(currentChannel['messages']):
        raise ValueError(
            description="start is greater than the total number of messages in the channel"
        )

    #verify the authorised user is a member of the channel

    if isUIDInChannel(userFromToken['u_id'], channel_id) == False:
        raise AccessError(
            description="Authorised user is not a member of channel with channel_id"
        )

    #if we get to this point we are ready to return the message data
    start = int(start)
    end = start + 50
    msgLen = len(currentChannel['messages'])
    if end > msgLen:
        end = msgLen

    pagedMessages = currentChannel['messages'][msgLen - end:msgLen - start]
    fullMessageData = []

    for m_id in pagedMessages:
        fullMessage = getMessageFromID(m_id)
        fullMessageData.append({
            'message_id': fullMessage['message_id'],
            'u_id': fullMessage['u_id'], 
            'message': fullMessage['message'], 
            'time_created': fullMessage['time_created'], 
            'reacts': fullMessage['reacts'], 
            'is_pinned': fullMessage['is_pinned'],
        })

    #if end == msgLen:
     #   end = -1

    # add functionality for pulling the required messages
    return {'messages': fullMessageData, 'start': start, 'end': end}


def channel_leave(token, channel_id):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    currentChannel = get_channel_check_valid(channel_id)
        
    if isUIDInChannel(userFromToken['u_id'], channel_id) == True:
        currentChannel['users'].remove({'u_id': userFromToken['u_id'], })
    else:
        raise AccessError(
            description='Authorised user is not a member of channel with channel_id')

    if {'u_id': userFromToken['u_id'], } in currentChannel['owners']:
        currentChannel['owners'].remove({'u_id': userFromToken['u_id'], })

    return {}


def channel_join(token, channel_id):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    currentChannel = get_channel_check_valid(channel_id)

    if isUIDInChannel(userFromToken['u_id'], channel_id) == True:
        return {}  # no need to do more work as the user we are trying to add is already a member of the channel

    #if we haven't returned by now we need to add the user to the channel
    if userFromToken['permission_id'] < 3:
        makeUIDOwnerChannel(userFromToken['u_id'], channel_id)
        currentChannel['users'].append({'u_id': userFromToken['u_id'], })
    elif currentChannel['is_private'] == True:
        raise AccessError(
                description="channel_id refers to a channel that is private and authorised user is not an admin or owner")
    else:
        currentChannel['users'].append({'u_id': userFromToken['u_id'], })

    return {}  # finally return


def channel_addowner(token, channel_id, u_id):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    currentChannel = get_channel_check_valid(channel_id)

    if isUIDInChannel(userFromToken['u_id'], channel_id) == False:
        raise ValueError()  # this should be an AccessError()

    #CHECK PERMISSION OF userFromToken to do this
    if isUIDOwnerChannel(userFromToken['u_id'], channel_id) == False or isUIDOwnerChannel(u_id, channel_id) == True:
        raise ValueError()

    makeUIDOwnerChannel(u_id, channel_id)
    return {}


def channel_removeowner(token, channel_id, u_id):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    currentChannel = get_channel_check_valid(channel_id)

    if isUIDInChannel(userFromToken['u_id'], channel_id) == False:
        raise ValueError()  # this should be an AccessError()

    #CHECK PERMISSION OF userFromToken to do this
    if isUIDOwnerChannel(userFromToken['u_id'], channel_id) == False or isUIDOwnerChannel(u_id, channel_id) == False:
        raise ValueError()

    removeUIDOwnerChannel(u_id, channel_id)  # this needs to be implemented

    return {}


def channel_list(token):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    returnChannelsList = getListOfUsersChannels(userFromToken['u_id'])

    return {'channels': returnChannelsList}


def channel_listall(token):
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    returnChannelsList = []

    for channel in data['channels']:
        returnChannelsList.append(
            {'name': channel['name'], 'channel_id': channel['channel_id'], })

    return {'channels': returnChannelsList}


def channel_create(token, name, is_public):
    global nextUnusedChannelId
    data = get_data()

    #authenticate the token
    userFromToken = get_user_check_valid(token)

    if len(name) > 20:
        raise ValueError(description='channel name too long')

    data['channels'].append({
        'name': name,
        'channel_id': nextUnusedChannelId,
        'messages': [],
        'users': [{'u_id': userFromToken['u_id'], }],
        'owners': [],
        'is_private': not is_public,
        'standup_running': False,  # standup_running is False by default
    })

    makeUIDOwnerChannel(userFromToken['u_id'], nextUnusedChannelId)

    temp = nextUnusedChannelId

    nextUnusedChannelId = nextUnusedChannelId + 1

    return {'channel_id': temp}
