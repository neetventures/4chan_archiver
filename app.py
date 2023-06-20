from flask import Flask
# from werkzeug.middleware.proxy_fix import ProxyFix
from archive.archive_site import archive_site
import os

app = Flask(__name__)
app.secret_key = 'nf44857480243344t'
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.register_blueprint(archive_site, url_prefix='/archive_site')

app.run(host='0.0.0.0', debug=True, port=9090)
