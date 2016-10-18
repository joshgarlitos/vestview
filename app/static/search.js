
$(document).ready(function() {
	$("#ticker-search").on('keyup', function (e) {
	    if (e.keyCode == 13) {
	    	var ticker = $('#ticker-search').val().toUpperCase();
	        window.location.href = '/stock/' + ticker;
	    }
	});
});
