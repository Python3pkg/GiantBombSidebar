# GiantBombSidebar
A simple Python script to get the upcoming Giant Bomb schedule and post it to the sidebar of reddit.com/r/GiantBomb.  This script was designed for Python 2.7.x.

# Setup
1. First run this to install the dependencies.
```
pip install -r requirements.txt
```
2. Next create an application at https://www.reddit.com/prefs/apps/.
3. Set the redirect uri to http://127.0.0.1:65010/authorize_callback.
4. Run the onetime file to generate your settings file.
```
python onetime.py
```
5. In the sidebar, place the following where you want the calendar to appear.
```
[](#calendar_start)
[](#calendar_end)
```
6. You can now run the file.
```
python giantbomb.py
```

# License
This script is licensed under the MIT license which is included.