import requests, json, re, os, time, datetime, random
from archive_configs import GLOBAL_EXCLUDE, WATCHLIST, REQUEST_COOLDOWN, COOLDOWN_VARIANCE

def make_path(path):
  if isinstance(path, str):
    path = [path]
  elif not isinstance(path, list):
    raise ValueError(path)
  return os.path.abspath(os.path.join(os.path.dirname(__file__), *path))

class URL:
  @staticmethod
  def catalog(board): return f'https://a.4cdn.org/{board}/catalog.json'

  @staticmethod
  def thread(board, postnum): return f'https://a.4cdn.org/{board}/thread/{postnum}.json'

  @staticmethod
  def media(board, image_id, ext): return f"""https://i.4cdn.org/{board}/{image_id}{ext}"""

  @staticmethod
  def thumbnail(board, image_id): return f"""https://i.4cdn.org/{board}/{image_id}s.jpg"""

def get_http_headers():
  return {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Accept": "application/json",
  }

def sleep():
  t = REQUEST_COOLDOWN
  if COOLDOWN_VARIANCE:
    t += random.random()
  time.sleep(t)

def fetch_json(url):
  response = requests.get(url, headers=get_http_headers())
  sleep()
  return json.loads(response.content)

def filter_catalog(pages, filters):
  catalog = [{'page': -1, 'threads': []}]
  for page in pages:
    for thread in page['threads']:
      for thread_attribute in ['sub', 'com']:
        if thread.get('sticky') == 1 or thread_attribute not in thread:
          continue

        content = thread[thread_attribute]
        if filters['include'] and not re.search(filters['include'], content, re.IGNORECASE):
          continue
        if filters['exclude'] and re.search(filters['exclude'], content, re.IGNORECASE):
          continue
        if GLOBAL_EXCLUDE and re.search(GLOBAL_EXCLUDE, content, re.IGNORECASE):
          continue

        catalog[0]['threads'].append(thread)
        break
  return catalog

def save_json(obj, path):
  with open(path, mode='w') as f:
    json.dump(obj, f)

def read_json(path):
  with open(path, mode='r') as f:
    return json.load(f)

def get_all_postnums_from_thread(thread):
  return [post['no'] for post in thread['posts']]

def post_has_image(post):
  return post.get('tim', None) and post.get('ext', None)

def get_all_post_images_from_thread(thread):
  post_images = []
  for post in thread['posts']:
    if post_has_image(post):
      post_images.append((post['no'], post['tim'], post['ext']))
  return post_images

def download_media(url, path):
  r = requests.get(url, stream=True)
  sleep()
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk:
        f.write(chunk)
        f.flush()

def get_date():
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def write_log(msg):
  with open(make_path('archive.log'), mode='a') as f:
    f.write(f"{get_date()}| {msg}\n")

def save_media(board, thread_filename, postnum, tim, ext):
  image_filepath = make_path(['archive', thread_filename, f"{postnum}_{tim}{ext}"])
  download_media(URL.media(board, tim, ext), image_filepath)

  thumbnail_filepath = make_path(['archive', thread_filename, f"{postnum}_{tim}s.jpg"])
  download_media(URL.thumbnail(board, tim), thumbnail_filepath)

def archive_thread(board, thread):
  thread_filename = f"{board}_{thread['posts'][0]['no']}"
  thread_file_path = make_path(['archive', f"{thread_filename}.json"])

  if not os.path.isfile(thread_file_path):
    write_log(f"Found a new thread.")
    save_json(thread, thread_file_path)
    count = 0
    for postnum, tim, ext in get_all_post_images_from_thread(thread):
      save_media(board, thread_filename, postnum, tim, ext)
      count += 1
    write_log(f'Saved {count} medias.')
    return

  write_log(f"Found more posts for thread.")
  saved_thread = read_json(thread_file_path)
  saved_thread_postnums = get_all_postnums_from_thread(saved_thread)
  for post in thread['posts']:
    if post['no'] not in saved_thread_postnums:
      saved_thread['posts'].append(post)
      if post_has_image(post):
        save_media(board, thread_filename, post['no'], post['tim'], post['ext'])

  save_json(saved_thread, thread_file_path)

def get_catalog_content(board, filters):
  catalog_content = fetch_json(URL.catalog(board))
  catalog_content = filter_catalog(catalog_content, filters)
  return catalog_content

def get_thread_content(board, postnum):
  thread_content = fetch_json(URL.thread(board, postnum))
  return thread_content

def main():
  for board, filters in WATCHLIST.items():
    write_log(f"Searching {board} : {filters}")
    catalog_content = get_catalog_content(board, filters)
    if catalog_content is None: continue

    for page in catalog_content:
      for thread in page['threads']:
        postnum = thread['no']
        thread_content = get_thread_content(board, postnum)
        if thread_content is None: continue
        archive_thread(board, thread_content)

if __name__=='__main__':
  # 4chan api docs: https://github.com/4chan/4chan-API/blob/master/pages/Endpoints_and_domains.md
  # cronjob: */20 * * * * /usr/bin/python3 /path/to/file/archive.py
  # running normally: python3 archive.py
  main()
