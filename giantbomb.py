import praw, urllib2, json
from prawoauth2 import PrawOAuth2Mini
from settings import app_key, app_secret, access_token, refresh_token, subreddit, user_agent

VERSION = '3.0.0'

def get_json():
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Reddit Sidebar')]
	response = opener.open('http://www.giantbomb.com/upcoming_json')
	data = json.load(response)
	return data

def create_table(data):
	table = '[](#calendar_start)\n'
	table += '>###Calendar\n'
	if len(data['upcoming']) != 0:
		table += 'Title | Time (PST)\n'
		table += ':-- |:--\n'
		for item in data['upcoming']:
			title = item['title']
			time = item['date']
			if(item['premium'] == True):
				table += '**' + title + '** | **[' + time + '](http://www.wolframalpha.com/input/?i=' + time + '+PST)**\n'
			else:
				table += title + ' | [' + time + '](http://www.wolframalpha.com/input/?i=' + time + '+PST)\n'
	table += '\n[](#calendar_end)'
	return table

def create_header(data):
	header = '[](#live_start)\n'
	if data['liveNow'] != None:
		header += '######[LIVE: ' + data['liveNow']['title'] + '](http://www.giantbomb.com/chat/)\n'
	header += '[](#live_end)'
	return header

def set_sidebar(table, header):
	user_agent_version = user_agent.replace('*', VERSION)
	r = praw.Reddit(user_agent = user_agent_version)
	o = PrawOAuth2Mini(r, app_key = app_key, app_secret = app_secret, access_token = access_token, scopes = ['identity', 'modconfig'], refresh_token = refresh_token)
	o.refresh()
	settings = r.get_settings(subreddit)
	sidebar_contents = settings['description']
	start = sidebar_contents.split('[](#calendar_start)', 1)[0]
	end = sidebar_contents.split('[](#calendar_end)', 1)[1]
	new_sidebar = start + table + end
	start = new_sidebar.split('[](#live_start)', 1)[0]
	end = new_sidebar.split('[](#live_end)', 1)[1]
	new_sidebar = start + header + end
	r.update_settings(r.get_subreddit(subreddit), description = new_sidebar)

def main():
	data = get_json()
	table = create_table(data)
	header = create_header(data)
	set_sidebar(table, header)

if __name__ == '__main__':
	main()