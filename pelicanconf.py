#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = u'Steven Loria'
SITENAME = u'stevenloria.com'
SITEURL = 'http://stevenloria.com'
PATH = 'content'
PAGE_PATHS = ['pages']
TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Make URLs clean
ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'

PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'assets',
    'post_stats',
    'pelican_gist',
]

# Blogroll
LINKS = None

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

THEME = 'themes/sl'

RELATIVE_URLS = True

# Navigation sections and relative URL:
SECTIONS = [
    ('about', ''),
    ('projects', 'projects'),
    ('scribbles', 'archives.html'),
    # ('Archive', 'archives.html'),
    # ('Tags', 'tags.html'),
]

DEFAULT_CATEGORY = 'uncategorized'
DATE_FORMAT = {
    'en': '%b %d, %Y'
}
DEFAULT_DATE_FORMAT = '%b %d, %Y'

DISQUS_SITENAME = None
TWITTER_USERNAME = 'sloria1'
LINKEDIN_URL = 'http://www.linkedin.com/in/sloria/'
GITHUB_URL = 'http://github.com/sloria'

PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
LOCALE = ""
DEFAULT_PAGINATION = 10

FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

OUTPUT_PATH = './output/'

GOOGLE_ANALYTICS_ACCOUNT = 'UA-39544608-1'

PIWIK_URL = None
PIWIK_SSL_URL = None
PIWIK_SITE_ID = None

MAIL_USERNAME = 'sloria1'
MAIL_HOST = 'gmail.com'

# static paths will be copied under the same name
STATIC_PATHS = ["images", 'extra/CNAME', 'extra/keybase.txt']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/keybase.txt': {'path': 'keybase.txt'},
}

# A list of files to copy from the source to the destination
# FILES_TO_COPY = (('extra/robots.txt', 'robots.txt'),)
# AUTOPREFIXER_BIN = './node_modules/.bin/postcss'
AUTOPREFIXER_BIN = os.path.join(HERE, 'node_modules', '.bin', 'postcss')
ASSET_CONFIG = (
    ('AUTOPREFIXER_BIN', AUTOPREFIXER_BIN),
    ('AUTOPREFIXER_BROWSERS', ['> 1%', 'last 2 versions']),
)
