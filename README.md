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
3. You can execute it via a CLI (`python3 archive.py`); with cron jobs every 20 minutes (`*/20 * * * * /usr/bin/python3 /path/to/file/archive.py`); or manually via the Web UI.

## Web UI

This Web UI is very minimalistic, and only displays media at the moment. See screenshots below.

### The catalog displaying all archived boards and threads:

![One](/screenshots/demo1.png)

### A thread displaying all its posts:

![Two](/screenshots/demo2.png)

## Web Deploy

The Web UI is only intended to be run locally; or publicly with some type of web server authentication like NGINX's basic auth. For example, you can skip get it up and running quickly with `python3 app.py`, and visiting `http://127.0.0.1:9090/archive_site`; or use NGINX as a reverse proxy and authenticator,

```nginx
server {
    server_name default_server;
    root /path/to/dir;

    auth_basic "Admin";
    auth_basic_user_file /etc/apache2/.htpasswd;

    client_max_body_size 10000m;

    location / {
        proxy_pass http://127.0.0.1:9090/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Prefix /;
    }
}
```

