from flask import render_template, send_file, Blueprint, redirect, url_for, request
import json
import os
import glob
import html
from collections import defaultdict
import shutil
import subprocess

archive_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'archive'))

template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
archive_site = Blueprint('archive_site', __name__, template_folder=template_folder, static_folder=static_folder)

def file_name(board, no, ext=''):
    return f'{board}_{no}{ext}'

def get_thread_data(board, no):
    post_file = os.path.join(archive_path, file_name(board, no, '.json'))
    with open(post_file) as f:
        thread = json.load(f)
    for i, p in enumerate(thread['posts']):
        thread['posts'][i]['board'] = board
        if p.get('tim', None):
            thread['posts'][i]['media_file'] = f"{board}_{no}/{p['no']}_{p['tim']}{p['ext']}"
            thread['posts'][i]['thumbnail_file'] = f"{board}_{no}/{p['no']}_{p['tim']}s.jpg"
    return thread['posts']

def get_op_data(board, no):
    return get_thread_data(board, no)[0]

def get_archive_ops():
    b_ops = defaultdict(lambda: [])
    board_threads = [os.path.basename(f).split('.')[0] for f in glob.glob(archive_path + '/*.json')] # [('his', '14089540')]
    for board_thread in board_threads:
        b, t = board_thread.split('_')
        op = get_op_data(b, t)
        b_ops[b].insert(0, op)
    return b_ops

@archive_site.route("/favicon.ico")
def favicon():
    return archive_site.send_static_file("favicon.ico")

def get_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

@archive_site.route("/")
def home():
    b_ops = get_archive_ops()

    with open(get_path('archive_configs.py'), 'r') as file:
        config_text = file.read()
    with open(get_path('archive.log'), 'r') as file:
        log_text = file.read()
    return render_template("catalog.html", config_text=config_text, log_text=log_text, b_ops=b_ops, html=html)

@archive_site.route('/archive_configs', methods=['POST'])
def archive_configs():
    content = request.form['content']
    with open(get_path('archive_configs.py'), 'w') as file:
        file.write(content)
    return redirect(url_for('archive_site.home'))

@archive_site.route('/archive/<path:filename>')
def send_media(filename):
    path = os.path.join(archive_path, filename)
    return send_file(path)

@archive_site.route('/thread/<string:board>/<string:postnum>')
def thread(board, postnum):
    posts = get_thread_data(board, postnum)
    return render_template("thread.html", posts=posts)

@archive_site.route('/delete/<string:board>/<string:postnum>')
def delete(board, postnum):
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archive', f'{board}_{postnum}')
    f = f'{d}.json'

    if os.path.isdir(d):
        shutil.rmtree(d)

    if os.path.isfile(f):
        os.remove(f)

    return redirect(url_for('archive_site.home'))

@archive_site.route('/run', methods=['GET'])
def manual_execute():
    subprocess.run(['/usr/bin/python3', os.path.join(os.path.abspath(os.path.dirname(__file__)), 'archive.py')])
    return redirect('home')
