import praw, urllib2
from bs4 import BeautifulSoup, SoupStrainer
from prawoauth2 import PrawOAuth2Mini
from settings import app_key, app_secret, access_token, refresh_token, subreddit, user_agent

VERSION = '1.0.0'

def get_html():
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open('http://www.giantbomb.com')
	html = response.read()
	return html

def create_table(html):
	product = SoupStrainer('dl', {'class': 'promo-upcoming'})
	soup = BeautifulSoup(html, parse_only = product)
	table = '[](#calendar_start)\n'
	table += '>###Calendar\n'
	table += 'Title | Time\n'
	table += ':-- |:--\n'
	for time in soup.findAll('dd'):
		title = time.div.h4.string
		showType = ''.join(time.div.p.strings).split('on', 1)[0].strip()
		showTime = ''.join(time.div.p.strings).split('on', 1)[1].strip()
		if(showType.startswith('Premium')):
			table += '**' + title + '** | **' +  showTime + '**\n'
		else:
			table += title + ' | ' +  showTime + ' | ' + '\n'
	table += '[](#calendar_end)'
	return table

def set_sidebar(table):
	user_agent_version = user_agent.replace('*', VERSION)
	r = praw.Reddit(user_agent = user_agent_version)
	o = PrawOAuth2Mini(r, app_key = app_key, app_secret = app_secret, access_token = access_token, scopes = ['identity', 'modconfig'], refresh_token = refresh_token)
	o.refresh()
	settings = r.get_settings(subreddit)
	sidebar_contents = settings['description']
	start = sidebar_contents.split('[](#calendar_start)', 1)[0] 
	end = sidebar_contents.split('[](#calendar_end)', 1)[1]
	new_sidebar = start + table + end
	r.update_settings(r.get_subreddit(subreddit), description = new_sidebar)

def main():
	html = get_html()
	table = create_table(html)
	set_sidebar(table)

main()