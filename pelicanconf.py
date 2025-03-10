import os

HERE = os.path.dirname(os.path.abspath(__file__))
AUTHOR = "Steven Loria"
SITENAME = "stevenloria.com"
SITEURL = "https://stevenloria.com"
PATH = "content"
PAGE_PATHS = ["pages"]
TIMEZONE = "America/New_York"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Make URLs clean
ARTICLE_URL = "{slug}"
ARTICLE_SAVE_AS = "{slug}/index.html"
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}/index.html"

PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "assets",
    "post_stats",
    "pelican_gist",
    "pelican_alias",
    "sitemap",
]

# Blogroll
LINKS = None

DEFAULT_PAGINATION = False

THEME = "themes/sl"

RELATIVE_URLS = True

# Navigation sections and relative URL:
SECTIONS = [
    ("about", ""),
    ("projects", "projects"),
    ("scribbles", "archives.html"),
]

DEFAULT_CATEGORY = "uncategorized"
DATE_FORMAT = {"en": "%b %d, %Y"}
DEFAULT_DATE_FORMAT = "%b %d, %Y"

DISQUS_SITENAME = None
LINKEDIN_URL = "http://www.linkedin.com/in/sloria/"
GITHUB_URL = "http://github.com/sloria"

PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
LOCALE = ""
DEFAULT_PAGINATION = 10

FEED_RSS = "feeds/all.rss.xml"
CATEGORY_FEED_RSS = "feeds/{slug}.rss.xml"

OUTPUT_PATH = "./output/"

MAIL_USERNAME = "sloria1"
MAIL_HOST = "gmail.com"

# static paths will be copied under the same name
STATIC_PATHS = [
    "extra/CNAME",
    "extra/favicon.ico",
    "extra/icon.png",
    "extra/robots.txt",
]
EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/icon.png": {"path": "icon.png"},
    "extra/robots.txt": {"path": "robots.txt"},
}

# A list of files to copy from the source to the destination
# FILES_TO_COPY = (('extra/robots.txt', 'robots.txt'),)
# AUTOPREFIXER_BIN = './node_modules/.bin/postcss'
POSTCSS_BIN = os.path.join(HERE, "node_modules", ".bin", "postcss")
UGLIFYJS_BIN = os.path.join(HERE, "node_modules", ".bin", "uglifyjs")
ASSET_CONFIG = (
    ("POSTCSS_BIN", POSTCSS_BIN),
    ("UGLIFYJS_BIN", UGLIFYJS_BIN),
)

SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "exclude": ["tag/", "category/", "author/"],
}
