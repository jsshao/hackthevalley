let vidId = "VEX7KhIA3bU";
let fetchData = function(){
    $.ajax("https://23.101.131.211/demographic",{
      data: JSON.stringify({"video_id":vidId}),
      contentType: 'application/json',
      type: 'POST',
      success: function(data){
        console.log(data)
      }
    });
};
fetchData();
