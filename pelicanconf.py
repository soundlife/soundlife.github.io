# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'soundlife'
SITENAME = 'SoundLife开发日志'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zh'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = ()
SOCIAL = ()
DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
