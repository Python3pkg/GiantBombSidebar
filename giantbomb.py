import praw, urllib2, httplib2, os, oauth2client, argparse
from bs4 import BeautifulSoup, SoupStrainer
from prawoauth2 import PrawOAuth2Mini
from pytz import timezone
from datetime import datetime, timedelta
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from settings import app_key, app_secret, access_token, refresh_token, subreddit, user_agent, calendar_id

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

VERSION = '2.0.0'


def get_credentials():
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'giantbombcalendar.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', 'https://www.googleapis.com/auth/calendar')
        flow.user_agent = 'GiantBombCalendar'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def setup_calendar():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)
	return service

def add_to_calendar(title, time, premium):
    service = setup_calendar()

    if premium == True:
    		title = title + ' (Premium)'
    title = title.replace('\'','')

    eventsResult = service.events().list(
        calendarId=calendar_id,
        q=title).execute()
    events = eventsResult.get('items', [])

    if not events:
    	start = datetime.strptime(time, '%b %d, %Y %I:%M %p')
    	start = timezone('US/Pacific').localize(start)
    	end = (start + timedelta(hours=1)).isoformat()
    	start = start.isoformat()
        event = {
          'summary': title,
          'start': {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': end,
            'timeZone': 'America/Los_Angeles',
          },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()

def clear_old_entries():
    service = setup_calendar()

    yesterday = datetime.now() - timedelta(1)
    yesterday = (timezone('US/Eastern').localize(yesterday)).isoformat()

    eventsResult = service.events().list(
        calendarId=calendar_id,
        singleEvents='True',
        orderBy='startTime',
        timeMax=yesterday).execute()
    events = eventsResult.get('items', [])
    for event in events:
        service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()

def get_html():
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open('http://www.giantbomb.com')
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
		showTime = '[' + displayTime + '](http://www.wolframalpha.com/input/?i=' + wolframTime + '+PST)'
		if(showType.startswith('Premium')):
			table += '**' + title + '** | **[' + displayTime + '](http://www.wolframalpha.com/input/?i=' + wolframTime + '+PST)**\n'
			add_to_calendar(title, displayTime, True)
		else:
			table += title + ' | [' + displayTime + '](http://www.wolframalpha.com/input/?i=' + wolframTime + '+PST)\n'
			add_to_calendar(title, displayTime, False)
	if time == None:
		table = '[](#calendar_start)\n'
		table += '>###Calendar\n'
	table += '\n[](#calendar_end)'
	return table

def create_header(html):
	product = SoupStrainer('div', {'class': 'header-promotion__wrapper'})
	soup = BeautifulSoup(html, 'html.parser', parse_only = product)
	live = soup.span.time.text
	if 'Live' in live:
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
	html = get_html()
	table = create_table(html)
	header = create_header(html)
	set_sidebar(table, header)
	clear_old_entries()

if __name__ == '__main__':
    main()