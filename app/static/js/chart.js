/* chart page is at someurl.domain/chart/<symbol>
   so simply grab href, and then grab the symbol*/
var params = window.location.href.split("/");
var symbol = params[params.length - 1];
var companies = {
    "AAPL": "Apple",
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
    "IBM": "IBM",
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

$(function () {
    $.getJSON('/data/' + symbol, function (data) {
        // Create the chart

        var stockPairs = [];
        // the JSON data object is returned with most recent date first
        // so loop through backwards for correct timeseries x axis
        for( var i = data.length - 1; i >= 0; --i){
            var element = data[i];
            // for some reason, can only get timeseries to work with
            // unix epoch time, so this is fine for now...
            var date = new Date(element.date).getTime();
            stockPairs.push([date, parseInt(element.values.open)]);
        }

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

        });
    });
});
