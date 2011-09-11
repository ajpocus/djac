$(function () {
  var canvas = $("#canvas")[0];
  var ctx = canvas.getContext('2d');
  var r = Math.min(canvas.width, canvas.height) / 2;
  var center = [canvas.width/2, canvas.height/2];

  function getColor () {
    var rgb = [];
    for (var i = 0; i < 3; i++) {
      rgb[i] = Math.round(100 * Math.random() + 155);
    }
    return 'rgb(' + rgb.join(',') + ')';
  }

  $.getJSON("/analytics/expenses/json/", function (data) {
    var done = 0;
    var legend = $("#legend tbody");
    
    for (percent in data) {
      var name = percent;
      var chunk = data[percent];
      ctx.beginPath();
      ctx.moveTo(center[0], center[1]);
      ctx.arc(center[0], center[1],
	r,
	Math.PI * (- 0.5 + 2 * done),
	Math.PI * (- 0.5 + 2 * (done + chunk)),
	false
      );

      ctx.lineTo(center[0], center[1]);
      ctx.closePath();
      ctx.fillStyle = getColor();
      ctx.fill();

      done += chunk;

      var legend = $("#legend");
      var n = "<span>" + name + "</span>";
      var nameSpan = $(n).attr('id', name).css('color', ctx.fillStyle);
      var p = "<span>" + (chunk*100).toFixed(2) + "%</span>";
      var percentSpan = $(p).addClass('percent').css('color', ctx.fillStyle);
      legend.append(nameSpan);
      legend.append(percentSpan);
      legend.append($("<br />"));
    };
  });
});
      
