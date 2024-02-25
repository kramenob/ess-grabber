main.py
start bot.py

    bot.py
    waiting messages from telegram chat
    by link-message, start grabber.py with giving link

        grabber.py
        with getting link from bot.py start browser.py

            browser.py
            open Chrome
            add vpn
            add soundcloud_downloader
            comeback to grabber.py

        open link
        return cookies
        save album info :: title, description, topics (./bin/info/info.md); cover (./bin/info/cover.png)
        resize cover to 500x500 px
        delete header & info sections
        saving tracks info while scrolling like array :: name-author, genre, mood, duration, bpm (./bin/tracks/tracks.py)
        create soundcloud link from tracks.py, save to array
        download every track by openning soundcloud track page, clicking "download" button (./bin/tracks/*.mp3)
        start soundclouder.py

            soundclouder.py
            open every track page by link (./bin/tracks/tracks.py)
            download every track by openning soundcloud track page, clicking "download" button (./bin/tracks/*.mp3)
            
            scheduler.py



            poster.py


                    