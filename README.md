# 4chan Archiver + Web UI

## Archiver

The archiver script is `/archive/archive.py`.

1. It does not use any databases - textual thread content is only saved as json.
2. It has very flexible filtering capabilities. For example,
```python
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
```
3. You can execute it with cron jobs every 20 minutes with `*/20 * * * * /usr/bin/python3 /path/to/file/archive.py`, or manually via the Web UI.

## Web UI

This Web UI is very minimalistic, and is only intended to be run locally, or with NGINX's basic auth, or similar. See screenshots below.

### The Catalog displaying all archived boards and threads.

![One](/screenshots/demo1.png)

### A thread displaying all its posts.

![Two](/screenshots/demo2.png)