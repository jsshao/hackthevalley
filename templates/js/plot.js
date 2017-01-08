// generate random x/y data
let randomXY = function () {
    let x = []
    let y = []
    let prev = 0.1;
    for (let i = 0; i < 157; i += 3) {
        x.push(i);
        let randomY;
        if (Math.round(Math.random())) {
            randomY = prev + Math.random()
        } else {
            randomY = prev - Math.random() * prev
        }
        y.push(randomY);
        prev = randomY
    }
    yMax = Math.max(...y)
    for (let i = 0, length = y.length; i < length; i++) {
        y[i] = y[i] / yMax;
    }
    return [x, y]
}
let data = []
for (let i = 0; i < 4; i++) {
    let xy = randomXY();
    let datapoint = {
        x: xy[0],
        y: xy[1],
        type: 'scatter',
        name: 'random' + i
    }
    data.push(datapoint)
}

layout = {
    hovermode: 'closest',
    title: 'Click to fastforward video to current time'
};

// plotly plot
let plot1 = document.getElementById('chart1')
Plotly.newPlot('chart1', data, layout);

// enable click to skip to point in video
plot1.on('plotly_click', function (data) {
    player.seekTo(data.points[0].x, true);
});
