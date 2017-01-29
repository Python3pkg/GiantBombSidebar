print '\nIf not set up, please create your application at:'
print 'https://www.reddit.com/prefs/apps/'
print 'Make sure you set it as a script and have the redirect uri be:'
print 'http://127.0.0.1:65010/authorize_callback\n'

app_key_input = raw_input('Please enter your app key: ')
app_secret_input = raw_input('Please enter your app secret: ')
app_name_input = raw_input('Please enter the name you used for the app: ')
subreddit_input = raw_input('Please enter your subreddit: ')
username_input = raw_input('Please enter your username: ')
user_agent = 'python:' + app_name_input + ':* (by /u/' + username_input + ')'
password_input = raw_input('Please enter your password: ')

settings = open('settings.py', 'w+')
settings.write('app_key = \'' + app_key_input + '\'')
settings.write('\napp_secret = \'' + app_secret_input + '\'')
settings.write('\nsubreddit_name = \'' + subreddit_input + '\'')
settings.write('\nusername = \'' + username_input + '\'')
settings.write('\npassword = \'' + password_input + '\'')
settings.write('\nuser_agent = \'' + user_agent + '\'')
settings.close()

print '\nSetup complete, you can now run giantbomb.py'