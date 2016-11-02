
$(document).ready(function() {
	$("#ticker-search").on('keyup', function (e) {
	    if (e.keyCode == 13) {
	    	var ticker = $('#ticker-search').val().toUpperCase();
	        window.location.href = '/stock/' + ticker;
	    }
	});

	var availableTutorials = [
               "AAPL",
               "AXP",
               "BA",
               "CAT",
               "CSCO",
               "CVX",
               "KO",
               "DD",
               "XOM",
               "GE",
               "GS",
               "HD",
               "IBM",
               "INTC",
               "JNJ",
               "JPM",
               "MCD",
               "MMM",
               "MRK",
               "MSFT",
               "NKE",
               "PFE",
               "PG",
               "TRV",
               "UNH",
               "UTX",
               "V",
               "VZ",
               "WMT",
               "DIS"
            ];
            $("#ticker-search").autocomplete({
               source: availableTutorials
            });

});
