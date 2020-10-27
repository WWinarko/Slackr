''' Message function tests '''
from datetime import datetime, timedelta
import time
import pytest

from functions.channel import channel_create, get_channel_check_valid, channel_join
from functions.messages import (message_send, message_sendlater, message_remove, message_edit,
                                message_pin, message_unpin, message_react, message_unreact,
                                getMessageFromID)
from functions.auth import get_data, auth_register

from functions.error import AccessError, ValueError

################################################################################
# setup for message tests                                                      #
################################################################################

# Set up a user.
userEmail = "example.email@domain.com"
userPassword = "Password123"
userFirstName = "First"
userLastName = "Last"
exampleUser = auth_register(userEmail, userPassword, userFirstName, userLastName)

userToken = exampleUser['token']
userID = exampleUser['u_id']

# user that is not in any channel
noAccessEmail = "noaccess@domain.com"
noAccessPassword = "Password321"
noAcessFirstName = "No"
noAccessLastName = "Access"
noAccessUser = auth_register(noAccessEmail, noAccessPassword, noAcessFirstName, noAccessLastName)

noAccessToken = noAccessUser['token']
noAccessID = noAccessUser['u_id']

# user that does not have owner/admin permissions
memberEmail = "member@domain.com"
memberPassword = "Member123"
memberFirstName = "Mr."
memberLastName = "Member"
memberUser = auth_register(memberEmail, memberPassword, memberFirstName, memberLastName)

memberToken = memberUser['token']
memberID = memberUser['u_id']

# Create a channel.
channelName = "Good Channel"
channel_create(userToken, channelName, True)

data = get_data()
testChannelDict = data['channels'][0]
testChannelID = testChannelDict['channel_id']

################################################################################
# message_sendlater()                                                          #
################################################################################

def test_message_sendlater():
    ''' Test the sendlater function '''
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"

    # 1001 characters constitutes an invalid message.
    invalid_message = """" 2ts9aYH2HsmgirYpHpQZvfiO1hUGPcUx3OMQjStpk2DntYt3qI1GLdxwMxLCt6k1dbiQTYgxazjcBg4FJssZKB9JmPhrn9GQUJVVCtt3S84uhMPTP2un99Pei7CX8urigxtzBURgjyYzr1wUHEh4rFsGmgHiaJRfiOlPTBTq2rZ5BRRAXcGuJhXU7wO63bubIBPIJlEmsF1azN00UA0xDWShANDdQskjn8dmiQVtUqlY1Bekj1BJjLmoBKmoWnAGVLPl7dJJEYjPuNj6Ws7u21vlP7LpayDzTPtnXva2kGoGppvGq1RFbFdtG9dsfWbp7X07uBsugYMJ2ZJfRO6r9Xnq3vLoMFq4TF9MiWyLqkefo1JsvV4H7rN7BstGXvOC3RjOjXCc7uqFuDwzBpFkT9R3rtQLTqrWD3KCckEvbWmQzUxQHMCNRgcy50m8NClbtIPxstMkzbacfQA9mpN92bC3YHAmn7SyzMAQ3gTG3cbAUO6bbveukPJwsYQr2BKZ17hFdL37eVGNfu3rJqvVZlKUObGJg5YteVSGnEyMcfvsaFW9NlxkAMmeBBYVtEo843tkc3o0SKfncduBxGisw8Q4UVbOyT7tToSeQundoNfNaVpCpwZswVSsF9vCCfS2T4z8B79pYjwQTUAw38vQAgQO4hKVgRFk4vCBjXkVpkD8px7L4wFBJx9QIIrfgOfbsph5iFwjmP45pqvk1lP1p4Pqy0IRKjg00hPkZHI64jBhK2oOFprEykdqHdLyfyBFpBJHJLieg4nLLSKx0YNIsu1h4ubRqrSBWF4Rsj1P8Lh7YXUG8i3ochWZGjNFu0safNEjRK72FPQFxDGwl4G64i4O9Z0VhiVNlHBcxnpHNqsn6h4bh3w9tzq1L9CDSkYNQFGuF8DI5EoLmwAUHO2bfe73AiDWYfvlKEp0BLzD5yLGvPHUz2Hdfun10tZJNcu3krCLenX5oVoJEmfRA8t5wvgRTDrLEaeEeuDaUbGCd
    """

    # 10 seconds in the future is a valid time.
    valid_time = datetime.now() + timedelta(seconds=10)

    # 10 seconds in the past is not a valid time.
    invalid_time = datetime.now() - timedelta(seconds=10)

    # an invalid channel id is any negative number
    invalid_channel_id = -1

    # check for value errors for invalid channel, lengthy messages, and invalid time.
    with pytest.raises(ValueError):
        message_sendlater(userToken, invalid_channel_id, valid_message, valid_time)
        message_sendlater(userToken, testChannelID, invalid_message, valid_time)
        message_sendlater(userToken, testChannelID, valid_message, invalid_time)

    # test for access errors
    global noAccessToken
    with pytest.raises(AccessError):
        message_sendlater(noAccessToken, testChannelID, valid_message, valid_time)

    # now just send message
    time_toSend = datetime.now().timestamp() + 10
    sent_messageID = message_sendlater(userToken, testChannelID, valid_message, time_toSend)

    # finally just test if the message ever gets sent
    time.sleep(11)
    channel = get_channel_check_valid(testChannelID)

    # if it worked then there is one message in the channel
    assert sent_messageID in channel['messages']

################################################################################
# message_send()                                                               #
################################################################################

def test_message_send():
    ''' Test the send function '''
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"

    # 1001 characters constitutes an invalid message.
    invalid_message = """" 2ts9aYH2HsmgirYpHpQZvfiO1hUGPcUx3OMQjStpk2DntYt3qI1GLdxwMxLCt6k1dbiQTYgxazjcBg4FJssZKB9JmPhrn9GQUJVVCtt3S84uhMPTP2un99Pei7CX8urigxtzBURgjyYzr1wUHEh4rFsGmgHiaJRfiOlPTBTq2rZ5BRRAXcGuJhXU7wO63bubIBPIJlEmsF1azN00UA0xDWShANDdQskjn8dmiQVtUqlY1Bekj1BJjLmoBKmoWnAGVLPl7dJJEYjPuNj6Ws7u21vlP7LpayDzTPtnXva2kGoGppvGq1RFbFdtG9dsfWbp7X07uBsugYMJ2ZJfRO6r9Xnq3vLoMFq4TF9MiWyLqkefo1JsvV4H7rN7BstGXvOC3RjOjXCc7uqFuDwzBpFkT9R3rtQLTqrWD3KCckEvbWmQzUxQHMCNRgcy50m8NClbtIPxstMkzbacfQA9mpN92bC3YHAmn7SyzMAQ3gTG3cbAUO6bbveukPJwsYQr2BKZ17hFdL37eVGNfu3rJqvVZlKUObGJg5YteVSGnEyMcfvsaFW9NlxkAMmeBBYVtEo843tkc3o0SKfncduBxGisw8Q4UVbOyT7tToSeQundoNfNaVpCpwZswVSsF9vCCfS2T4z8B79pYjwQTUAw38vQAgQO4hKVgRFk4vCBjXkVpkD8px7L4wFBJx9QIIrfgOfbsph5iFwjmP45pqvk1lP1p4Pqy0IRKjg00hPkZHI64jBhK2oOFprEykdqHdLyfyBFpBJHJLieg4nLLSKx0YNIsu1h4ubRqrSBWF4Rsj1P8Lh7YXUG8i3ochWZGjNFu0safNEjRK72FPQFxDGwl4G64i4O9Z0VhiVNlHBcxnpHNqsn6h4bh3w9tzq1L9CDSkYNQFGuF8DI5EoLmwAUHO2bfe73AiDWYfvlKEp0BLzD5yLGvPHUz2Hdfun10tZJNcu3krCLenX5oVoJEmfRA8t5wvgRTDrLEaeEeuDaUbGCd
    """

    # check for value error when message is too large
    with pytest.raises(ValueError):
        message_send(userToken, testChannelID, invalid_message)

    # check for access error when user is not in channel
    global noAccessToken
    with pytest.raises(AccessError):
        message_send(noAccessToken, testChannelID, valid_message)

    # check if message actually gets sent
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()
    channel = get_channel_check_valid(testChannelID)
    assert sent_messageID in channel['messages']


################################################################################
# message_remove()                                                             #
################################################################################

def test_message_remove():
    ''' Test the remove function '''
    # first we need to send a message
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()

    # get a user who is not the one who sent it
    global memberToken
    channel_join(memberToken, testChannelID)

    # check for access error by non admins and non message owners
    with pytest.raises(AccessError):
        message_remove(memberToken, sent_messageID)

    # now just remove the message
    message_remove(userToken, sent_messageID)

    # check that its actually removed
    channel = get_channel_check_valid(testChannelID)
    assert sent_messageID not in channel['messages']

    # check for value error after its already been removed
    with pytest.raises(ValueError):
        message_remove(userToken, sent_messageID)

################################################################################
# message_edit()                                                               #
################################################################################

def test_message_edit():
    ''' Test the edit function '''
    # first we need to send a message
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"
    edited_message = "Bye!"
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()

    # get a user who is not the one who sent it
    global memberToken
    channel_join(memberToken, testChannelID)

    # check for access error by non admins and non message owners
    with pytest.raises(AccessError):
        message_edit(memberToken, sent_messageID, edited_message)

    # then just edit the message contents
    message_edit(userToken, sent_messageID, edited_message)

    # check that its actually edited
    newMessage = getMessageFromID(sent_messageID)
    assert newMessage['message'] == edited_message

    # now check that it deletes if you pass in an empty string
    message_edit(userToken, newMessage['message_id'], "")

    # check that its actually removed
    channel = get_channel_check_valid(testChannelID)
    assert newMessage not in channel['messages']


################################################################################
# message_react()                                                              #
################################################################################

def test_message_react():
    ''' Test the react function '''
    # first we need to send a message
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()
    validReactID = 1

    invalidMessageID = -1
    invalidReactID = -1

    # check for value error when invalid message id, invalid react id
    with pytest.raises(ValueError):
        message_react(userToken, invalidMessageID, validReactID)
        message_react(userToken, sent_messageID, invalidReactID)

    # now just react
    message_react(userToken, sent_messageID, validReactID)
    reactedMessage = getMessageFromID(sent_messageID)
    assert reactedMessage['reacts'][0]['is_this_user_reacted']

    # now check that therere is a value error when you try to react again
    with pytest.raises(ValueError):
        message_react(userToken, sent_messageID, validReactID)


################################################################################
# message_unreact()                                                            #
################################################################################

def test_message_unreact():
    ''' Test the unreact function '''
    # first we need to send a message
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()
    validReactID = 1

    # now we need to react to that message
    message_react(userToken, sent_messageID, validReactID)

    invalidMessageID = -1
    invalidReactID = -1

    # check for value errors for invalid message id and invalid react id
    with pytest.raises(ValueError):
        message_react(userToken, invalidMessageID, validReactID)
        message_react(userToken, sent_messageID, invalidReactID)

    # now just unreact to the message
    message_unreact(userToken, sent_messageID, validReactID)
    unreactedMessage = getMessageFromID(sent_messageID)
    assert unreactedMessage['reacts'][0]['is_this_user_reacted'] == False

    # now check that therere is a value error when you try to unreact again
    with pytest.raises(ValueError):
        message_unreact(userToken, sent_messageID, validReactID)


################################################################################
# message_pin()                                                                #
################################################################################

def test_message_pin():
    ''' Test the pin function '''
    # first we need to send a message
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()

    global memberToken
    global noAccessToken
    invalid_messageID = -1

    # check that you get value errors if non admin is pinning or if its invalid id
    with pytest.raises(ValueError):
        message_pin(userToken, invalid_messageID)
        message_pin(memberToken, sent_messageID)

    # check that you get an access error when the person is not in channel
    with pytest.raises(AccessError):
        message_pin(noAccessToken, sent_messageID)

    # now pin the message for real
    message_pin(userToken, sent_messageID)

    pinnedMessage = getMessageFromID(sent_messageID)
    assert pinnedMessage['is_pinned'] == 1

    # now check for value error if we try to pin it again
    with pytest.raises(ValueError):
        message_pin(userToken, sent_messageID)

################################################################################
# message_unpin()                                                              #
################################################################################

def test_message_unpin():
    ''' Test the unpin function '''
    # first we need to send a message
    global userToken
    global testChannelDict
    global testChannelID

    valid_message = "Hello!"
    sent_messageID = message_send(userToken, testChannelID, valid_message).pop()

    # now we just need to pin it
    message_pin(userToken, sent_messageID)

    global memberToken
    global noAccessToken
    invalid_messageID = -1

    # check that there is a value error when invalid message, non admin
    with pytest.raises(ValueError):
        message_unpin(userToken, invalid_messageID)
        message_unpin(memberToken, sent_messageID)

    # check that there is an access error when user is not in channel
    with pytest.raises(AccessError):
        message_unpin(noAccessToken, sent_messageID)

    # now unpin for real
    message_unpin(userToken, sent_messageID)

    unpinnedMessage = getMessageFromID(sent_messageID)
    assert unpinnedMessage['is_pinned'] == 0

    # now check for value error if we try to pin it again
    with pytest.raises(ValueError):
        message_unpin(userToken, sent_messageID)
