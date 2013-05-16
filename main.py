# This file is part of PetitEscalier Bot.
# 
# PetitEscalier Bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
# 
# PetitEscalier Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PetitEscalier Bot.  If not, see <http://www.gnu.org/licenses/>.
#
# (C) Copyright Yves Quemener, 2013

import praw

import traceback
import sys
import getpass

from time import sleep

reddit = praw.Reddit(user_agent='PetitEscalier bot, by u/keepthepace')
user='keepthepace'
print "Password for",user,"?"
passwd=getpass.getpass()
reddit.login(user, passwd)

while True:
    try:
        sr = reddit.get_subreddit("petitescalier").get_hot(limit=20)

        s=""
        s+='<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'
        for post in sr:
            s += '<div class="post">'
            s += '<span class="score">' + str(post.score) + '</span>'
            s += '<span class="post_title">' + post.title.encode('utf8') + '</span>'
            s += ' par '
            s += '<span class="author">' + post.author.name.encode('utf8') + '</span>'
            s += '</div>' # /post
            s += '\n'

        fi = open("/var/www/Projects/PetitEscalierReadOnly/index.html", "w")
        fi.write(s)
        fi.close()
        sleep(3600) # One update every hour is quite enough for now
    except:
        print asctime(),"Exception in main program : "
        traceback.print_exc()
        sleep(300) # retry in 5 minutes

