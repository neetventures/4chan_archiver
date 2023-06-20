WATCHLIST = {
  'g': {
    'include': 'home server general', # downloads threads with 'home server general' in subject or comment.
    'exclude': None,
  },
  'ck': {
    'include': 'webm thread',
    'exclude': 'potatoes', # will not download webm threads with 'potatoes' in subject or comment.
  },
}
GLOBAL_EXCLUDE = 'tomatoes|potatoes' # exclude any post matching this regex
REQUEST_COOLDOWN = 0.25 # base time to sleep after making each request
COOLDOWN_VARIANCE = True # will add additional, random times to each request.