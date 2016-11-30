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
    "MCD": "McDonald's Corporation",
    "MMM": "3M Co",
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

let slideDirection = 'forwards';

let play = true;
let done = false;
setPlay(play);

let lastArticleDate = 0;
let lastTweetDate = 0;

let playbackMode = false;
let lastTweenValue = 0;
let stockPairs = [];
let articleLookup = {};
const TIMELINE_MAX = 10000;

$(function () {
    // create articles array to display later
    let tempDate = 0;
    for(let i = 0; i < articles.length; i++){
        // get current date
        let currentDate = articles[i].date;
        if(currentDate != tempDate){
            tempDate = currentDate;

            articleLookup[formatDate(currentDate)] = {
                'article': articles[i],
                'shown': false,
                'image': ''
            };

            findAndSaveImage(formatDate(currentDate), articles[i].url);
        }
    }

    $('#company').text(companies[symbol]);

    $('#timeline').on('input', function(e){
        setPlay(false);
        let value = e.currentTarget.value;
        let ratio = value / TIMELINE_MAX;
        updateChartPosition(ratio);

        updateSliderDirection(value);
    });

    // set dates on x-axis
    let axis = $('.bar').toArray();
    let dates = [];
    let inc = Math.floor((data.length - 1) / (axis.length - 1));

    // get the last item
    setAxisMeta(axis[axis.length - 1], data[0].date);
    // get rest of dates for axis
    for(let i = 0; i < axis.length - 1; i ++) {
        let length = data.length - 1;
        let index = length - (i * inc);
        let currentDate = data[index].date;
        setAxisMeta(axis[i], currentDate);
    }

    function setAxisMeta(el, currentDate){
        let formatted = moment(currentDate, 'YYYY-MM-DD').format('ddd, MMM Do');
        $(el).find('.meta').text(formatted);
    }


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

    let query = window.location.search.substring(1);
    let pair = query.split('=');
    if(pair[0] == 'p' && pair[1] == '1') {
        playbackMode = true;
    }

    renderStockChart(stockPairs);

    $('#play-pause').on('click', function(){
        if(play){
            setPlay(false);
            $('#ct-stocks path').velocity('stop', true);
            lastDate = 0;
        } else{ 
            setPlay(true);
            if(done) {
                done = false;
                lastTweenValue = 0;
            }

            animateStockChart();
        }
    });
    
});

function findAndSaveImage(lookupDate, url){
    $.ajax('http://opengraph.io/api/1.0/site/' + url)
     .done(function(data){
        console.log(data);
        console.log(data.hybridGraph.image);
        articleLookup[lookupDate].image = data.hybridGraph.image;
    });
}

let lastSlide = -1;
let lastDirection = 'none';
function updateSliderDirection(slide){
    if(slide < lastSlide){
        slideDirection = 'backwards';
        lastSlide = slide;
    } else if (slide > lastSlide) {
        slideDirection = 'forwards';
        lastSlide = slide;
    } else {
        console.log('slide values equal');
    }

    if(lastDirection != slideDirection){
        lastDirection = slideDirection;
        lastDate = 0;
    }
}


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
                if(playbackMode) {
                    animateStockChart();
                } else {
                    // update text since it won't be updated on playback
                    let last = stockPairs[stockPairs.length - 1];
                    $('#shown-date').text(formatDate(last[0]));
                    $('#price').text(last[1].toFixed(2));
                }
                $('#ct-stocks path').css('opacity', '1');
            }, 100);
        }, 400);

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
    
    /*
    // On each drawn element by Chartist we use the Chartist.Svg API to trigger SMIL animations
    chart.on('draw', function(data) {
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
      
    }); */

}


function animateStockChart(){
    // animate path
    

    let duration = 9000;
    let durationDiff = duration * (1 - lastTweenValue);
    // could try easing: 'easeInOut'

    $('#ct-stocks path').velocity({
        tween: [1, lastTweenValue]
    },{
        duration: durationDiff,
        easing: 'linear',
        progress: function(elements, complete, remaining, start, tweenValue){
            if(play){
                $('#timeline').val(tweenValue * TIMELINE_MAX);
                updateChartPosition(tweenValue);
            }
    }
    });
}


function setPlay(bool) {
    play = bool;

    if(play) {
        slideDirection = 'forwards';
        $('.current-control .play').css('display', 'none');
        $('.current-control .pause').css('display', 'block');
    } else {
        $('.current-control .play').css('display', 'block');
        $('.current-control .pause').css('display', 'none');
    }
}


function updateChartPosition(tween){
    var path = $('#ct-stocks path').get(0);
    var pathLen = path.getTotalLength();

    if(tween == 1) {
        setPlay(false);
        done = true;
    }

    var adjustedLen = tween * pathLen;
    lastTweenValue = tween;

    $('path').attr('opacity', 1);
    path.setAttribute('stroke-dasharray', adjustedLen+' '+pathLen);

    updatePage(tween);
}


let lastDate = 0;
let lastUpdateSlider = -1;
function updatePage(tween){
    // update price number
    let obj = getCurrentStockAndDate(tween);
    let price = obj.price.toFixed(2);
    $('#price').text(price);

    if(obj.nextPrice > price) {
        $('.status').addClass('up');
        $('.status').removeClass('down');
    } else if(obj.nextPrice < price) {
        $('.status').addClass('down');
        $('.status').removeClass('up');
    } else {
        $('.status').removeClass('up');
        $('.status').removeClass('down');
    }

    // update date
    let date = formatDate(obj.date);
    $('#shown-date').text(date);

    // commented out for now, will work on
    // later for scrubbing ability
    //
    /* if(articleLookup[date].shown && slideDirection == 'backwards'){
        // moving backward
        articleLookup[date].shown = false;

        // check to see if this is actually removing
        $('#news').find('[id="'+ date + '"]').remove();
    } else */

    if (!articleLookup[date].shown && slideDirection == 'forwards'){
        // moving forward
        articleLookup[date].shown = true;
        console.log('news image: ', articleLookup[date].image);
        let el = generateArticleElement(date);

        $('#news').prepend(el);

        $('.newsbox').click(function(e){
            let url = $(e.currentTarget).attr('data-url');
            let win = window.open(url, '_blank');
            win.focus();
        });
    }
}

function generateArticleElement(date){
    let article = articleLookup[date].article;
    let div = '';
    
    let image = articleLookup[date].image;
    //let image = "https://g.foolcdn.com/image/?url=http%3A%2F%2Fg.foolcdn.com%2Feditorial%2Fimages%2F413807%2Fiphone-7-manufacturing-2.png&h=630&w=1200&op=resize";
    div += "<div class='newsbox' id='" + date + "' data-url='" + article.url + "'>";
    div += "<div class='image' style='background-image: url(\"" + image + "\")'></div>";
    div += "<div class='info'>";
    div += "<div class='title'>" + article.title + "</div>";
    div += "<div class='description'>" + article.source + ' - <span>' + moment(date, 'MMM Do, YYYY').format('dddd MMM. Do, YYYY') + "</span></div>";
    div += "<div class='blurb'>" + article.openingSentence + "</div>";
    div += "</div>";

    return div;
}

// function incase we want to change later
function formatDate(time) {
    return moment(time).format('MMM Do, YYYY');
}

// uses global stockPairs array
function getCurrentStockAndDate(ratioToAdjust){
    // get the index relative to progress of graph
    //console.log(ratio);
    ratio = adjustRatio(ratioToAdjust);


    let currentIndex = ratio * (stockPairs.length - 1);
    //console.log(currentIndex);
    let floor = stockPairs[Math.floor(currentIndex)][1];
    //console.log(floor);
    let ceiling = stockPairs[Math.ceil(currentIndex)][1];
    //console.log(ceiling);

    // estimate current price by using the percentage that it's between the two points on the graph
    let remainder = currentIndex % 1;
    let adjusted = (ceiling - floor) * remainder;
    let price = floor + adjusted;

    let nextPrice = ceiling;

    let date = stockPairs[Math.floor(currentIndex)][0];

    return {price: price, date: date, nextPrice: nextPrice};
}

function adjustRatio(ratio){
    yMax = 1;
    yMin = 0;

    xMin = 0.0017777777777777779;
    xMax = 1;

    percent = (ratio - xMin) / (xMax - xMin);
    output = percent * (yMax - yMin) + yMin;

    return output;
}











