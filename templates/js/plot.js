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
let gData1 = []
for (let i = 0; i < 4; i++) {
    let xy = randomXY();
    let datapoint = {
        x: xy[0],
        y: xy[1],
        type: 'scatter',
        name: 'random' + i
    }
    gData1.push(datapoint)
}

let gData = []
let vidId = VIDEO_ID;
let rawGData;
$.ajax("https://23.101.131.211/metric",{
  data: JSON.stringify({"video_id":vidId}),
  contentType: 'application/json',
  type: 'POST',
  success: function(data){
    rawGData = data;
  }
}).done(function(){
  emotions = Object.keys(rawGData[0]);
  emotions.splice(emotions.indexOf("timestamp"),1);

  for (let j=0; j < emotions.length; j++){
    x = []
    y = []
    for (let i = 0; i < rawGData.length; i++) {
      y.push(rawGData[i][emotions[j]])
      x.push(i/2)
    }
    let datapoint = {
      x,
      y,
      type: 'scatter',
      name: emotions[j]
    }
    gData.push(datapoint)
  }
  // for (let i = 0; i < emotions.length; i++) {
  //
  // }
  layout = {
      hovermode: 'closest',
      title: 'Click to fastforward video to current time'
  };
  Plotly.newPlot('graph', gData, layout);
  // enable click to skip to point in video
  let graph = document.getElementById('graph')
  graph.on('plotly_click', function (data) {
    player.seekTo(data.points[0].x, true);
  });
})

let rawData;
$.ajax("https://23.101.131.211/demographic",{
  data: JSON.stringify({"video_id":vidId}),
  contentType: 'application/json',
  type: 'POST',
  success: function(data){
    rawData = data;
  }
}).done(function(){
  let pData = [
    {
      y: ["13-17","18-24","25-35","35-44","45-54","55+"],
      x: rawData.age,
      type: 'bar',
      orientation: 'h'
  }]
  let bData = [
    {
      labels: ["male","female"],
      values: rawData.gender,
      type: 'pie'
  }]

  // plotly plot
  console.log('reach')

  Plotly.newPlot('barChart', bData);
  Plotly.newPlot('pieChart', pData,{title: 'Age'});
})
