import praw, urllib2, json
from settings import *

VERSION = '3.1.0'

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
	r = praw.Reddit(client_id = app_key, client_secret = app_secret, password = password, user_agent = user_agent_version, username = username)
	sidebar_contents = r.subreddit(subreddit_name).description
	start = sidebar_contents.split('[](#calendar_start)', 1)[0]
	end = sidebar_contents.split('[](#calendar_end)', 1)[1]
	new_sidebar = start + table + end
	start = new_sidebar.split('[](#live_start)', 1)[0]
	end = new_sidebar.split('[](#live_end)', 1)[1]
	new_sidebar = start + header + end
	r.subreddit(subreddit_name).mod.update(description = new_sidebar, spoilers_enabled = True)

def main():
	data = get_json()
	table = create_table(data)
	header = create_header(data)
	set_sidebar(table, header)

if __name__ == '__main__':
	main()