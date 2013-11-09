eventstream
===========

A projection-friendly Google+ and Twitter hashtag feed. Give it a 
hashtag and it'll display posts on a large screen during an event.

Requirements
------------

1. An AppEngine account, configured for Google+ access, and a server API key.
2. A twitter app, and its OAuth id and app secret.
3. Google AppEngine SDK (so you can deploy it).


Installation
-------------

1. cp config.py.sample to config.py
2. edit config.py with:
    - your twitter and g+ app info
    - the title and hashtag you want to search for
3. edit app.yaml with your AppEngine app id and deploy with Google AppEngine Launcher
4. fun!


Customization
-------------
1. Edit /static/assets/css/index.css to customize styles (optional)*
2. Edit /templates/index.html to tweak layout (optional)
3. Edit /static/assets/js/index.js if you really want to go nuts (super optional)

* This should display on a 1024x768 or larger projector. 

Use
-------------
- Use View->Fullscreen in Chrome or Firefox for optimum display.
- Posts and Tweets will display on the left column as they come in. The most recent tweet will update in the right column.
- Click on a post to enter focus mode and it will overtake the display. This is ideal for Q&A sessions.
- Click on a focused post to return to stream mode.
- Attach an image to your post. Yeah!

License
-------------

Unless otherwise noted, all files are Copyright (c) 2011 Jason M. Striegel (+Jason Striegel / @jmstriegel) and are released for use under the MIT open source license. See MIT-LICENSE.txt for details.


