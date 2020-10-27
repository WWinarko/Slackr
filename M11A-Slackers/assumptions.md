# M11A-Slackers Assumptions

* Assumed that the return value '{}' is an empty dictionary.
* Assumed that, for test purposes, a user dictionary consists of an id, first name, and last name.
* Assumed that for functions such as channel_leave(), the exception raised is a general 'Exception'.
* Assumed that all functions need to be tested as individual components.
* Assumed that all alphanumeric characters can be used in the name field(s).
* Assumed that the user will re-register before every test.
* Assumed that a message can't be sent if it is empty.
* Assumed that a new message after being edited won't be more than 1000 characters.
* Assumed that the token passed to a function will be a valid token.