import praw, urllib2
from bs4 import BeautifulSoup, SoupStrainer
from prawoauth2 import PrawOAuth2Mini
from pytz import timezone
from datetime import datetime
from settings import app_key, app_secret, access_token, refresh_token, subreddit, user_agent

VERSION = '3.0.0'

def get_html(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url)
	html = response.read()
	return html

def create_table(html):
	product = SoupStrainer('dl', {'class': 'promo-upcoming'})
	soup = BeautifulSoup(html, 'html.parser', parse_only = product)
	table = '[](#calendar_start)\n'
	table += '>###Calendar\n'
	table += 'Title | Time (PST)\n'
	table += ':-- |:--\n'
	time = None
	for time in soup.findAll('dd'):
		title = time.div.h4.string
		showType = ''.join(time.div.p.strings).split('on', 1)[0].strip()
		showTime = ''.join(time.div.p.strings).split('on', 1)[1].strip()
		showTime = datetime.strptime(showTime, '%b %d, %Y %I:%M %p')
		showTime = timezone('US/Eastern').localize(showTime)
		showTime = showTime.astimezone(timezone('US/Pacific'))
		displayTime = datetime.strftime(showTime, '%b %d, %Y %I:%M %p')
		wolframTime = datetime.strftime(showTime, '%b+%d+%Y+%I:%M+%p')
		if(showType.startswith('Premium')):
			table += '**' + title + '** | **[' + displayTime + '](http://www.wolframalpha.com/input/?i=' + wolframTime + '+PST)**\n'
		else:
			table += title + ' | [' + displayTime + '](http://www.wolframalpha.com/input/?i=' + wolframTime + '+PST)\n'
	if time == None:
		table = '[](#calendar_start)\n'
		table += '>###Calendar\n'
	table += '\n[](#calendar_end)'
	return table

def check_live():
	html = get_html('http://www.giantbomb.com/chat')
	product = SoupStrainer('h2', {'class': 'header-border'})
	soup = BeautifulSoup(html, 'html.parser', parse_only = product)
	show = True
	for text in soup:
		if soup.string.strip() == 'There is currently no show.':
			show = False
	return show

def create_header(html):
	product = SoupStrainer('div', {'class': 'header-promotion__wrapper'})
	soup = BeautifulSoup(html, 'html.parser', parse_only = product)
	live = soup.span.time.text
	if 'Live' in live:
		check = check_live()
		if check == True:
			if hasattr(soup.span.p.a, 'string'):
				title = soup.span.p.a.string
			elif hasattr(soup.span.p, 'string'):
				title = soup.span.p.string
			else:
				pass
		title = title.strip()
		header = '[](#live_start)\n'
		header += '######[LIVE: ' + title + '](http://www.giantbomb.com/chat/)\n'
		header += '[](#live_end)'
	else:
		header = '[](#live_start)\n'
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
	html = get_html('http://www.giantbomb.com')
	table = create_table(html)
	header = create_header(html)
	set_sidebar(table, header)

if __name__ == '__main__':
    main()