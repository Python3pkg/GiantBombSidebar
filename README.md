# GiantBombSidebar
A simple Python script to get the upcoming Giant Bomb schedule and post it to the sidebar of https://www.reddit.com/r/giantbomb.  Also indicates in the header if a show is live.  This script was designed for Python 2.7.x.

# Setup
1. First run this to install the dependencies.

    ```
    pip install -r requirements.txt
    ```

2. Next create an application at https://www.reddit.com/prefs/apps/.
3. Set the redirect uri to http://127.0.0.1:65010/authorize_callback.
4. Fill out config_example.yaml with the information you received and your reddit information.
5. Rename config_example.yaml to config.yaml
6. In the sidebar, place the following where you want the calendar to appear (with a new line after calender_end).

    ```
    [](#calendar_start)
    [](#calendar_end)
    ```

7. Where you want the header to appear place the following.

    ```
    [](#live_start)
    [](#live_end)
    ```

8. Take the CSS from header.css and place it into the subreddit stylesheet.

9. You can now run the file.

    ```
    python giantbomb.py
    ```

10. Depending on your setup either use a cron, Windows Task Scheduler, or similar utilities to have this run every few minutes.

# License
This script is licensed under the MIT license which is included.