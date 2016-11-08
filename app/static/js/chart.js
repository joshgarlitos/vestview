/* chart page is at someurl.domain/chart/<symbol>
   so simply grab href, and then grab the symbol*/
var params = window.location.href.split("/");
var symbol = params[params.length - 1];
var companies = {
    "AAPL": "Apple Inc.",
    "AXP": "American Express",
    "BA": "Boeing",
    "CAT": "Catepillar",
    "CSCO": "Cisco",
    "CVX": "Chevron",
    "KO": "Coca Cola",
    "DD": "DuPont",
    "XOM": "ExxonMobil",
    "GE": "General Electric",
    "GS": "Goldman Sachs",
    "HD": "Home Depot",
    "IBM": "IBM Common Stock",
    "INTC": "Intel",
    "JNJ": "Johnson & Johnson",
    "JPM": "JPMorgan Chase",
    "MCD": "McDonald",
    "MMM": "3M",
    "MRK": "Merck",
    "MSFT": "Microsoft",
    "NKE": "Nike",
    "PFE": "Pfizer",
    "PG": "Proctor & Gamble",
    "TRV": "The Travelers",
    "UNH": "United Health",
    "UTX": "United Technologies",
    "V": "Visa",
    "VZ": "Verizon",
    "WMT": "Wal-Mart",
    "DIS": "Walt Disney"
}

let play = true;
let lastTweenValue = 0;
let stockPairs = [];
let lastPrice = 0;

$(function () {
    $('#company').text(companies[symbol]);

    // Create the chart
    // the JSON data object is returned with most recent date first
    // so loop through backwards for correct timeseries x axis
    for( var i = data.length - 1; i >= 0; --i){
        var element = data[i];
        // for some reason, can only get timeseries to work with
        // unix epoch time, so this is fine for now...
        var date = new Date(element.date).getTime();
        stockPairs.push([date, parseInt(element.values.open)]);
    }

    /* highcharts stuff 

    Highcharts.stockChart('stockchart', {
        rangeSelector: {
            selected: 1
        },

        title: {
            text: companies[symbol] + " \'s Stock Price"
        },
        series: [{
            name: companies[symbol],
            data: stockPairs,
            tooltip: {
                valueDecimals: 2
            }
        }],

    }); */

    renderStockChart(stockPairs);

    $('#play-pause').on('click', function(){
        console.log('click');
        if(play){
            play = false;
            $('#ct-stocks path').velocity('stop', true);
        } else{ 
            play = true;
            animateStockChart();
        }
    });

});


function renderStockChart(stock){

    let data = {
        labels: [],
        series: [[]]
    };

    for(let i = 0; i < stock.length; i++) {
        
        data.series[0].push(stock[i][1]);
    }

    // create graph
    var options = {
        lineSmooth: Chartist.Interpolation.simple({
            divisor: 300
        }),
        axisY: {
            labelInterpolationFnc: function(value) {
                return '$' + value;
            },
            onlyInteger: true,
            scaleMinSpace: 20
        },
        axisX: {
            // We can disable the grid for this axis
            showGrid: false,
            // and also don't show the label
            showLabel: false,
            offset: 0
        },
        fullWidth: true,
        height: 300,
        showPoint: false,
        chartPadding: {
            right: 0,
            left: 0
        }
        
    }
    // init a line chart 
    var chart = new Chartist.Line('#ct-stocks', data, options);

    // Let's put a sequence number aside so we can use it in the event callbacks
    var seq = 0;

    // Once the chart is fully created we reset the sequence
    chart.on('created', function() {
        seq = 0;

        setTimeout(function(){
            $('#ct-stocks .ct-label').addClass('show-label');
            $('#ct-stocks line').css('opacity', '1');

            setTimeout(function(){
                animateStockChart();
                $('#ct-stocks path').css('opacity', '1');
            }, 100);
        }, 200);

        /*
        // create tooltips for each point
        $('#ct-stocks .ct-point').each(function(i, pnt){
            var inc = new Date();
            inc.setDate(weekAgo.getDate() + (i + 1));
            var day = app.helpers.intToDay(inc.getDay());

            $(pnt).attr('ct:day', day);
        }); */

        /*
        // add tooltips
        var $chart = $('#ct-stocks');
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
        }); */
    });

    // On each drawn element by Chartist we use the Chartist.Svg API to trigger SMIL animations
    chart.on('draw', function(data) {
        // set accent color
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

    $('#ct-stocks').addClass('show');
}


function animateStockChart(){
    // animate path
    var path = $('#ct-stocks path').get(0);
    var pathLen = path.getTotalLength();

    let duration = 10000;
    let durationDiff = duration * (1 - lastTweenValue);
    // could try easing: 'easeInOut'

    $('#ct-stocks path').velocity({
        tween: [1, lastTweenValue]
    },{
        duration: durationDiff,
        easing: 'linear',
        progress: function(elements, complete, remaining, start, tweenValue){
            if(play){
                // save for if we stop
                lastTweenValue = tweenValue;

                // update path length
                var adjustedLen = tweenValue * pathLen;
                $('path').attr('opacity', 1);
                path.setAttribute('stroke-dasharray', adjustedLen+' '+pathLen);

                // update price number
                let obj = getCurrentStockAndDate(tweenValue);
                let price = obj.price.toFixed(2);
                $('#price').text(price);

                if(lastPrice < price) {
                    $('.status').addClass('up');
                    $('.status').removeClass('down');
                } else {
                    $('.status').addClass('down');
                    $('.status').removeClass('up');
                }

                lastPrice = price;

                let date = moment(obj.date).format('MMM Do, YYYY');
                console.log(date);
                $('#shown-date').text(date);
            }


            // adjusted length = current point
            // pathLen = max

            // current point = 0 at start, pathLen * tweenValue, 
            // tweenValue needs to be adjusted for remaining ratio 
            // duration needs to be shorter 
            // 
    }
    });
}

// uses global stockPairs array
function getCurrentStockAndDate(ratio){
    // get the index relative to progress of graph
    let currentIndex = ratio * (stockPairs.length - 1);
    let floor = stockPairs[Math.floor(currentIndex)][1];
    let ceiling = stockPairs[Math.ceil(currentIndex)][1];

    // estimate current price by using the percentage that it's between the two points on the graph
    let remainder = currentIndex % 1;
    let adjusted = (ceiling - floor) * remainder;
    let price = floor + adjusted;

    let date = stockPairs[Math.floor(currentIndex)][0];

    return {price: price, date: date};
}


