$(function () {
  var canvas = $("#canvas");
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
    data.keys().forEach(function (percent) {
      var name = percent;
      var chunk = percent[name];
      ctx.beginPath();
      ctx.moveTo(center[0], center[1]);
      ctx.arc(center[0], center[1],
	radius,
	Math.PI * (- 0.5 + 2 * done),
	Math.PI * (- 0.5 + 2 * (done + chunk)),
      );

      ctx.lineTo(center[0], center[1]);
      ctx.closePath();
      ctx.fillStyle = getColor();
      ctx.fill();

      done += chunk;
    });
  });
});
      
