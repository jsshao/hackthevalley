let tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

let player;
let currLoc;
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
        console.log('video started');
        let currTime = Math.round(player.getCurrentTime() * 2);

        moveCursor(currTime);

    } else if (event.data == YT.PlayerState.PAUSED) {
        //PAUSED
        console.log('video paused')
        stopAnimation()
    }
}

function moveCursor(targetLoc) {
    let duration = 500;
    // if (Math.abs(targetLoc-currLoc) > 1){
    //   duration = 0;
    // }
    console.log(targetLoc)
    let cut_index = names.indexOf('frame' + targetLoc)
    console.log(cut_index)
    let remaining_frames = frames.slice(cut_index)
    console.log(remaining_frames)

    Plotly.animate('graph', frames.slice(cut_index), {
        frame: [{duration: 500}],
        transition: [{
            duration: 500,
            easing: 'linear'
        },],
        mode: 'next'
    })
}


function stopAnimation() {
    Plotly.animate('graph', [], {mode: 'next'});
}


let gData = [{x: [0, 0], y: [0, 1], type: 'line', marker: {color: 'rgb(131, 131, 131)'}, name: 'Current Time'}]
let vidId = VIDEO_ID;
let rawGData;
var frames = [];
var names = [];
let colors = ['rgb(233, 69, 52)', 'rgb(233, 172, 52)', 'rgb(71, 36, 60)', 'rgb(126, 209, 47)', 'rgb(94, 66, 47)', 'rgb(57, 55, 163)', 'rgb(222, 198, 35)']
$.ajax("https://23.101.131.211/metric", {
    data: JSON.stringify({"video_id": vidId}),
    contentType: 'application/json',
    type: 'POST',
    success: function (data) {
        rawGData = data;
    }
}).done(function () {
    emotions = Object.keys(rawGData[0]);
    emotions.splice(emotions.indexOf("timestamp"), 1);
    emotions.splice(emotions.indexOf("contempt"), 1);

    for (let j = 0; j < emotions.length; j++) {
        x = []
        y = []
        for (let i = 0; i < rawGData.length; i++) {
            y.push(rawGData[i][emotions[j]])
            x.push(i / 2)
        }
        let datapoint = {
            x,
            y,
            type: 'scatter',
            name: emotions[j],
            marker: {
                color: colors[j]
            }
        }
        gData.push(datapoint)
    }
    layout = {
        hovermode: 'closest',
        title: 'Click to fastforward video to current time',
        xaxis: {range: [0, rawGData.length / 2]},
        yaxis: {range: [0, 1]}
    };
    Plotly.newPlot('graph', gData, layout);

    //moving cursor frames

    for (let i = 0; i < rawGData.length; i += 1) {
        name = 'frame' + i;
        frames.push({
            name: name,
            data: [{
                x: [i / 2, i / 2],
                y: [0, 1.1]
            }]
        });
        names.push(name);
    }
    Plotly.addFrames('graph', frames);

    // Plotly.animate('graph', names, {
    // 	frame: [{
    // 		duration: 500
    // 	}, ],
    // 	transition: [{
    // 		duration: 450,
    // 		easing: 'linear'
    // 	}, ],
    // 	mode: 'next'
    // })
})


let rawData;
$.ajax("https://23.101.131.211/demographic", {
    data: JSON.stringify({"video_id": vidId}),
    contentType: 'application/json',
    type: 'POST',
    success: function (data) {
        rawData = data;
    }
}).done(function () {
    let pData = [
        {
            y: ["13-17", "18-24", "25-35", "35-44", "45-54", "55+"],
            x: rawData.age,
            type: 'bar',
            orientation: 'h',
            marker: {
                color: 'rgb(144, 168, 205)'
            }
        }]
    let bData = [
        {
            labels: ["male", "female"],
            values: rawData.gender,
            marker: {
                colors: ['rgb(144, 168, 205)', 'rgb(247, 203, 202)']
            },
            type: 'pie'
        }]

    // plotly plot
    console.log('reach')

    Plotly.newPlot('barChart', bData);
    Plotly.newPlot('pieChart', pData, {title: 'Age'});
})
