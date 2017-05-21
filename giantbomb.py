import praw, urllib.request, urllib.error, urllib.parse, json, yaml

VERSION = '3.3.0'

def get_config():
	with open('config.yaml', 'r') as file:
		config = yaml.load(file)
	return config

def get_json():
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Reddit Sidebar')]
	response = opener.open('http://www.giantbomb.com/upcoming_json')
	data = json.load(response)
	return data

def create_live(data):
	live = ""
	if data['liveNow'] != None:
		live = '######[LIVE: ' + data['liveNow']['title'] + '](http://www.giantbomb.com/chat/)'
	return live

def create_calendar(data):
	calendar = '>###Calendar'
	if len(data['upcoming']) != 0:
		calendar += '\nTitle | Time (PST)'
		calendar += '\n:-- |:--'
		for item in data['upcoming']:
			if(item['premium'] == True):
				calendar += '\n**' + item['title'] + '** | **[' + item['date'] + '](http://www.wolframalpha.com/input/?i=' + item['date'].replace(' ', '+') + '+PST)**'
			else:
				calendar += '\n' + item['title'] + ' | [' + item['date'] + '](http://www.wolframalpha.com/input/?i=' + item['date'].replace(' ', '+') + '+PST)'
	return calendar

def set_sidebar(live, calendar, config):
	user_agent = 'python:' + config['app_name'] + ':' + VERSION + ' (by /u/' + config['username'] + ')'
	reddit = praw.Reddit(client_id = config['app_key'], client_secret = config['app_secret'], password = config['password'], user_agent = user_agent, username = config['username'])
	sidebar = reddit.subreddit(config['subreddit']).wiki[config['wiki_page']].content_md
	sidebar = sidebar.replace('%%LIVE%%', live)
	sidebar = sidebar.replace('%%CALENDAR%%', calendar)
	reddit.subreddit(config['subreddit']).mod.update(description = sidebar, spoilers_enabled = True)

def main():
	config = get_config()
	data = get_json()
	live = create_live(data)
	calendar = create_calendar(data)
	set_sidebar(live, calendar, config)

if __name__ == '__main__':
	main()