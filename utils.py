from PyQt5.QtCore import QUrl

# Constants
DEFAULT_HOME_PAGE = 'http://google.com'
DEFAULT_ZOOM_FACTOR = 1.2
MAX_TITLE_LENGTH = 15

# Utility functions
def format_url(url):
    """Format URL for navigation"""
    if not url:
        return QUrl(DEFAULT_HOME_PAGE)
    
    if isinstance(url, str):
        if '.' not in url and ' ' not in url:
            return QUrl('https://www.google.com/search?q=' + url)
        elif ' ' in url:
            return QUrl('https://www.google.com/search?q=' + url.replace(' ', '+'))
        elif not url.startswith(('http://', 'https://')):
            return QUrl('https://' + url)
        return QUrl(url)
    elif isinstance(url, QUrl):
        return url
    else:
        return QUrl(DEFAULT_HOME_PAGE)

def truncate_title(title):
    """Truncate title to maximum length with ellipsis"""
    if not title:
        return ""
    return title[:MAX_TITLE_LENGTH] + '...' if len(title) > MAX_TITLE_LENGTH else title 