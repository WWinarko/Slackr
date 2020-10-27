## Reasons for refactoring code in accordance with software engineering principles:
When code is first written, it can be done in a way which produces the desired
results by the deadline with little to no attention paid to its quality. When
this is the case, the code that is produced is not maintainable, and as a result
cannot adapt to changing specifications and can make simple bug fixes quite
obtuse. Such issues are known as code smells. As a client may have changing needs
throughout the lifetime of the project, the quality of code, and thereby its
maintainability is often an important feature that needs attention.

In order to produce good code from poor code, it must be refactored. This can
include simplifying control structures, removing unnecessary bloat, or even
re-writing entire functions. In producing a solution for Iteration 2, the codebase
that was submitted included poorly designed control structures and unused
variables, among other issues. As a result, we employed two common methodologies
to improve it, namely the KISS (Keep It Simple, Stupid) and DRY (Don't Repeat
Yourself) methodologies. Furthermore, we chose to also combat some design smells,
which was mainly done by simplifying control structures.

Throughout the revision of our code we noted a few code smells were present.
These included fragility, opacity, needless complexity, and needless
repetition. By fixing these issues, we were able to simplify our code and make it
of higher quality, as shown below.

#### Example of Old Code:
```python
for message in data['messages']:
    if message['message_id'] == message_id:
        if message['u_id'] != user['u_id']:
            if not isUIDOwnerChannel(user['u_id'], message['channel_id']):
                raise AccessError(description="You do not have permission to delete this message.")
```
Upon first sight, one can tell that this code is overly complicated. The above
block uses nested loops in trying to locate a message from ID, and then checks
if that message's poster is the active user, or if the active user is an owner
of the channel. This above code was simplified as follows.

#### Example of New Code:
```python
message = getMessageFromID(message_id)

# raise AccessError if the user does not have permission to delete message.
if message['u_id'] != user['u_id']:
    if not isUIDOwnerChannel(user['u_id'], message['channel_id']):
        raise AccessError(description="You do not have permission to delete this message.")
```
Firstly, the message was obtained from a specific function that executed the same
loop. This was created because this was found to be a common need of many functions
and thus warranted its own function in order to avoid needless repetition in
accordance with the DRY principle.

The code at points was quite fragile, as we noticed it broke when correcting the
'reacts' field of the message object to be a list of dictionaries. This unfortunately
had to be corrected manually. The code at times was also opaque and had needless repetition or complexity, as
can be seen in the above code blocks. This was corrected throughout the codebase
in similar ways.

## Code modifications:

#### auth.py:
* Placed error checking for valid email address into seperate function
* Placed error checking for name length into seperate function

#### standup.py:
* Cleaned up imports to import specific functions from modules
* Placed code to find standup in global list into seperate function
* Use function from channel.py to check if a given channel exists rather than doing it manually

#### messages.py:
* Added comments to various blocks of code that may have been difficult to understand.
* Removed repeated 'for' loops when locating message object by ID.
* Added more calls for the 'message from ID' function.
* Removed unnessecary variables in functions.
* Added descriptions to error checks to make bug-fixing easier.

#### channel.py & channel_test.py:
* Changed imports from wildcard to specific functions

#### user.py & admin.py:
* Used helper function from auth.py(check_valid_email) to check valid email instead of 
  checking it directly in user_profile_setemail(KISS)
* Moved check_name_length to auth.py because auth need to check name_length too(DRY)
* Used get_user_from_email from auth.py instead of check_used_email to check used email(DRY)
* Moving find_user_from_id from admin.py to auth.py as get_user_from_uid(DRY)
* Used  get_user_from_uid for checking valid u_id instead of check_valid_user_id which do same thing(DRY)
* Added change_permission at admin.py to make it maintainable and understandable(DRY)

### search.py:
* Used get_user_from_token from auth.py to get user
* Used getListOfUsersChannels from channel.py to get list of channel which the user joined
* Used get_channel_check_valid from channel.py to get channel dict from getListOfUsersChannels
* USed getMessageFromID from channel.py to get message dict from message_id in channel dict
