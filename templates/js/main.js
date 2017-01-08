'use strict';

/****************************************************************************
 * Initial setup
 ****************************************************************************/

// var roomURL = document.getElementById('url');
var video = document.querySelector('video');
var photo = document.getElementById('photo');
var photoContext = photo.getContext('2d');
var photoData;
var photoTimer;
var PHOTO_INTERVAL = 500;

var photoContextW;
var photoContextH;

/****************************************************************************
 * User media (webcam)
 ****************************************************************************/

function initWebCam() {
    console.log('Getting user media (video) ...');
    navigator.mediaDevices.getUserMedia({
        audio: false,
        video: true
    })
        .then(gotStream)
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}

function gotStream(stream) {
    var streamURL = window.URL.createObjectURL(stream);
    console.log('getUserMedia video stream URL:', streamURL);
    window.stream = stream; // stream available to console
    video.src = streamURL;
    video.onloadedmetadata = function () {
        photo.width = photoContextW = 320;
        photo.height = photoContextH = 240;
        console.log('gotStream with with and height:', photoContextW, photoContextH);
    };
}

/****************************************************************************
 * Cookie and Session Cookie Functions
 ****************************************************************************/

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "";
}

function getSessionCookie() {
    var sessionCookie = getCookie("prophetSessionCookie");
    if (sessionCookie == "") {
        sessionCookie = Math.random().toString(36);
        window.document.cookie = "prophetSessionCookie=" + sessionCookie + "; expires=0; path=/";
    }
    return sessionCookie;
}

/****************************************************************************
 * Photo Functions
 ****************************************************************************/

function savePhoto() {
    photoContext.drawImage(video, 0, 0, photo.width, photo.height);
    photoData = photo.toDataURL().substring(22);
    var data = {
        image: photoData,
        user_id: getSessionCookie(),
        video_id: VIDEO_ID,
        timestamp: Math.round(player.getCurrentTime() * 2)
    };
    console.log(data);
    var jsonData = JSON.stringify(data);
    $.ajax({
        type: "POST",
        url: "/collect",
        headers: {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
        data: jsonData,
        crossDomain: true,
        dataType: "json"
    })
        .done(function (msg) {
            console.log(msg);
        });
}


/****************************************************************************
 * Aux functions, mostly UI-related
 ****************************************************************************/

function show() {
    Array.prototype.forEach.call(arguments, function (elem) {
        elem.style.display = null;
    });
}

function hide() {
    Array.prototype.forEach.call(arguments, function (elem) {
        elem.style.display = 'none';
    });
}

/****************************************************************************
 * YouTube Section
 ****************************************************************************/

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: VIDEO_ID,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    console.log('youtube player loaded');
    document.getElementById("title").innerText = player.getVideoData().title;
    event.target.playVideo();
}

let myPlayerState;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        //PLAYING
        console.log('video started');
        savePhoto();
        photoTimer = setInterval(savePhoto, PHOTO_INTERVAL);
    } else if (event.data == YT.PlayerState.PAUSED) {
        //PAUSED
        console.log('video paused')
        clearInterval(photoTimer);
        photoTimer = null;
    } else {
        clearInterval(photoTimer);
        photoTimer = null;
    }
}

function stopVideo() {
    player.stopVideo();
}


/****************************************************************************
 * Init
 ****************************************************************************/

initWebCam();