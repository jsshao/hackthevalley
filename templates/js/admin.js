let tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let player;
function onYouTubePlayerAPIReady() {
    player = new YT.Player('player', {
        height: '400',
        width: '711',
        videoId: VIDEO_ID,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        },
    });
}
function onPlayerReady(event) {
    console.log('youtube player loaded')
    document.getElementById("title").innerText = player.getVideoData().title;
}

let myPlayerState;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        //PLAYING
        console.log('video started')
    } else if (event.data == YT.PlayerState.PAUSED) {
        //PAUSED
        console.log('video paused')
    }
}
