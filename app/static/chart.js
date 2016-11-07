
$(document).ready(function() {

	console.log(hello);
});


// create graph
var options = {
	lineSmooth: Chartist.Interpolation.simple({
		divisor: 20
	}),
	axisY: {
		labelInterpolationFnc: function(value) {
			return value + ' h';
		}
	},
	fullWidth: true,
	height: 160,
	showPoint: true,
	chartPadding: {
		right: 30,
		left: 20
	}
}
// init a line chart 
var chart = new Chartist.Line('#ctReqs', data, options);
// set accent color
$('#ctReqs path').css('stroke', app.accentColor);
$('#ctReqs .ct-point').css('stroke', app.accentColor);

// Let's put a sequence number aside so we can use it in the event callbacks
var seq = 0;

// Once the chart is fully created we reset the sequence
chart.on('created', function() {
	seq = 0;

	// create tooltips for each point
	$('#ctReqs .ct-point').each(function(i, pnt){
		var inc = new Date();
		inc.setDate(weekAgo.getDate() + (i + 1));
		var day = app.helpers.intToDay(inc.getDay());

		$(pnt).attr('ct:day', day);
	});

	// animate path
	var path = $('#ctReqs path').get(0);
	var pathLen = path.getTotalLength();

	$('#ctReqs path').velocity({
		tween: 1
	},{
		duration: 4500,
		easing: 'eastInOut',
		progress: function(elements, complete, remaining, start, tweenValue){
			var adjustedLen = tweenValue * pathLen;
			$('path').attr('opacity', 1);
			path.setAttribute('stroke-dasharray', adjustedLen+' '+pathLen);
	}
	});

	// add tooltips
	var $chart = $('#ctReqs');
	var $tooltip = $chart
		.append('<div class="tooltip"></div>')
		.find('.tooltip')
		.hide();

	$chart.on('mouseenter', '.ct-point', function(event) {
			var $point = $(this),
		    	day = $point.attr('ct:day'),
		    	value = $point.attr('ct:value');

		  	$tooltip.html(day + ' <span>' + value + '</span>').show();

		  	$tooltip.css({
				left: $(this).attr('x1') - $tooltip.width() / 2 - 3,
				top: $(this).attr('y1') - $tooltip.height() - 30
			});
	});

	$chart.on('mouseleave', '.ct-point', function() {
	  $tooltip.hide();
	});
});

// On each drawn element by Chartist we use the Chartist.Svg API to trigger SMIL animations
chart.on('draw', function(data) {
	// set accent color
	$('#ctReqs path').css('stroke', app.accentColor);
	$('#ctReqs .ct-point').css('stroke', app.accentColor);
  if(data.type === 'point') {
    // If the drawn element is a line we do a simple opacity fade in. This could also be achieved using CSS3 animations.
    data.element.animate({
      opacity: {
        // The delay when we like to start the animation
        begin: seq++ * 80,
        // Duration of the animation
        dur: 1000,
        // The value where the animation should start
        from: 0,
        // The value where it should end
        to: 1
      }
    });
  } 
});

$('#ctReqs').addClass('show');
