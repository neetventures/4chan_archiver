// utils

async function get(url){
  try {
    let res = await fetch(url);
    return await res;
  } catch (error) {
    console.log(error);
  }
}

function toggle(event, clss){
  var elements = document.getElementsByClassName(clss);
  for(let i = 0; i < elements.length; i++){
      elements[i].hidden = !elements[i].hidden;
  }
}

function delete_thread(event, url){
  var dialog = confirm("Delete this thread?\n" + url);
  if (dialog) {
    get(url);
  }
}

var max_loaded_videos = 100;
var loaded_video_media_outerhtml = [];
var loaded_video_media_src = [];
var loaded_video_thumbs_outerhtml = [];

function get_media(e){
  if(e.target.dataset.media_ext == '.webm')
  {
    loaded_video_thumbs_outerhtml.push(e.target.outerHTML);
    e.target.outerHTML = `<video controls autoplay loop>
      <source
        src="${e.target.dataset.media}"
        type="video/webm"
        data-media="${e.target.src.substr(e.target.src.indexOf('/archive_'))}"
        data-media_ext=".jpg"
      >
    </video>`
    loaded_video_media_outerhtml.push(e.target.outerHTML);
    loaded_video_media_src.push(e.target.dataset.media);

    if (loaded_video_media_src.length > max_loaded_videos){
      oldest_video_src = loaded_video_media_src.shift();
      oldest_video_thumbnail = loaded_video_thumbs_outerhtml.shift();
      var node = document.querySelector(`source[src="${oldest_video_src}"]`);
      node.parentNode.outerHTML = oldest_video_thumbnail;
    }

  }
  else {
    e.target.outerHTML = `<img src="${e.target.dataset.media}"
      data-media="${e.target.src.substr(e.target.src.indexOf('/archive_'))}"
      data-media_ext=".jpg"
      onclick="get_media(event)"
    >`
  }
}

function get_video(e){
  e.target.outerHTML = `<video controls autoplay>
    <source
      src="${e.target.dataset.media}"
      type="video/mp4"
    >
  </video>`
}
