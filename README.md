# GiantBombSidebar
A simple Python  to get the upcoming Giant Bomb schedule and post it to the sidebar of https://www.reddit.com/r/giantbomb.  Also indicates in the header if a show is live.  This  was designed for Python 2.7.x.

Note: I would recommend talking to somebody who works at Giant Bomb if you intend to run this  regularly.

# Setup
1. First run this to install the dependencies.

    ```
    pip install -r requirements.txt
    ```

2. Next create an application at https://www.reddit.com/prefs/apps/.
3. Set the redirect uri to http://127.0.0.1:65010/authorize_callback.
4. Create a wiki page to base the sidebar off of on your subreddit.
5. Fill out config_example.yaml with the information you received and your reddit information.
6. Rename config_example.yaml to config.yaml
7. In the sidebar, place the following where you want the live header to appear.

    ```
    %%LIVE%%
    ```

8. Where you want the calendar to appear place the following.

    ```
    %%CALENDAR%%
    ```

9. Take the CSS from header.css and place it into the subreddit stylesheet.

10. You can now run the file.

    ```
    python giantbomb.py
    ```

11. Depending on your setup either use a cron, Windows Task Scheduler, or similar utilities to have this run every few minutes. My cron listing to have the script run every five minutes is the following:

    ```
    */5 * * * * cd /usr/local/GiantBombSidebar && /usr/bin/python /usr/local/GiantBombSidebar/giantbomb.py
    ```

# License
This  is licensed under the MIT license which is included.