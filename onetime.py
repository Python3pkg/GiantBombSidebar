import praw
from prawoauth2 import PrawOAuth2Server
from settings import app_key, app_secret

print "\nIf not set up, please create your application at:"
print "https://www.reddit.com/prefs/apps/"
print "Make sure you set it as a script and have the redirect uri be:"
print "http://127.0.0.1:65010/authorize_callback\n"

app_key_input = raw_input("Please enter your app key: ")
app_secret_input = raw_input("Please enter your app secret: ")
subreddit_input = raw_input("Please enter your subreddit: ")\

print "Your web browser will now open, please accept the agreement"

r = praw.Reddit(user_agent = 'GiantBombSidebar by /u/Skelotic found at https://github.com/SDFortier/GiantBombSidebar')
o = PrawOAuth2Server(r, app_key = app_key_input, app_secret = app_secret_input, state = 'GiantBombSidebar by /u/Skelotic found at https://github.com/SDFortier/GiantBombSidebar', scopes = ['identity', 'modconfig'])
o.start()
tokens = o.get_access_codes()

settings = open('settings.py', 'w+')
settings.write('app_key = \'' + app_key_input + '\'')
settings.write('\napp_secret = \'' + app_secret_input + '\'')
settings.write('\naccess_token = \'' + tokens['access_token'] + '\'')
settings.write('\nrefresh_token = \''  + tokens['refresh_token'] + '\'')
settings.write('\nsubreddit = \'' + subreddit_input + '\'')
settings.close()

print "\nSetup complete, you can now run giantbomb.py"