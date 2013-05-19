#!/usr/bin/python
# -*- coding: utf-8

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

from time import sleep, asctime

def debug():
    reddit = praw.Reddit(user_agent='PetitEscalier bot, by u/keepthepace')
    user='keepthepace'
    print "Password for",user,"?"
    passwd=getpass.getpass()
    reddit.login(user, passwd)
    arr = []
    for a in reddit.get_subreddit("petitescalier").get_hot(limit=20):
        arr.append(a)
    return arr

def add_replies(replies):
    if len(replies)==0:
        return ""
    else:
        s=""
        for rep in replies:
            s+=' <div class="reply">\n'
            s+='  <div class="reply_header">\n'
            s+='   <span class="score">' + str(rep.score) + '</span>\n'
            s+='   <span class="author">' + rep.author.name.encode('utf8') + '</span>\n'
            s+='  </div>\n' # /reply_header
            s+='  <div class="reply_body">\n' 
            s+='<pre>' # En attendant un renderer a la reddit
            s+= rep.body.encode('utf8') + '</pre></div>\n'
            s+= add_replies(rep.replies)
            s+=' </div>\n' # /reply
    return s

if __name__ == "__main__":
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
            s+= '<link href="css.css" type="text/css" rel="stylesheet"></link>'
            s+="""<script>
    function toggleVisible(elem)
    {
        e=document.getElementById(elem);
        if((e.style.display=="none")||(e.style.display==""))
        {
            e.style.display="block";
        }
        else
        {
            e.style.display="none";
        }
    }
</script>\n"""
            num_rep=0;
            for post in sr:
                s += '<div class="post">\n'
                s += ' <div class="post_header">\n'
                s += '  <span class="score">' + str(post.score) + '</span>\n'
                s += '  <span class="post_title">' + post.title.encode('utf8') + '</span>\n'
                s += ' par '
                s += '  <span class="author">' + post.author.name.encode('utf8') + '</span>\n'
                s += ' </div>\n' # /post_header
                s += ' <div class="post_body"><pre>' + post.selftext.encode('utf8') + '</pre></div>\n'
                s += ' <a href="#" OnClick=\'toggleVisible("replies_'+str(num_rep)+'");return false;\'>Afficher les commentaires</a>'
                s += ' <div class="replies" id="replies_'+str(num_rep)+'\">\n'
                s += add_replies(post.comments)
                s += ' </div>' # /replies
                s += '</div>\n' # /post
                s += '\n'
                num_rep+=1

            fi = open("/var/www/Projects/PetitEscalierReadOnly/index.html", "w")
            fi.write(s)
            fi.close()
            print "Updated : " + asctime()
            sleep(3600) # One update every hour is quite enough for now
        except:
            print asctime(),"Exception in main program : "
            traceback.print_exc()
            sleep(300) # retry in 5 minutes

