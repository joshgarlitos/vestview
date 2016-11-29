
$(document).ready(function() {
	/* In order for autocomplete to work, you need an array of objects
	   in the format [ {value:<symbol>, name:<company>, price:<price>
	 */
	var autocompleteData = [];
	var companies = {
	    "AAPL": "Apple", "AXP": "American Express", "BA": "Boeing", "CAT": "Catepillar",
	    "CSCO": "Cisco", "CVX": "Chevron", "KO": "Coca Cola", "DD": "DuPont",
	    "XOM": "ExxonMobil", "GE": "General Electric", "GS": "Goldman Sachs",
	    "HD": "Home Depot", "IBM": "IBM", "INTC": "Intel", "JNJ": "Johnson & Johnson",
	    "JPM": "JPMorgan Chase", "MCD": "McDonald", "MMM": "3M", "MRK": "Merck",
	    "MSFT": "Microsoft", "NKE": "Nike", "PFE": "Pfizer", "PG": "Proctor & Gamble",
	    "TRV": "The Travelers", "UNH": "United Health", "UTX": "United Technologies",
	    "V": "Visa", "VZ": "Verizon", "WMT": "Wal-Mart", "DIS": "Walt Disney"
	};
	/* vestview.com/djia is simply a page with an array JSON objects,
	   each obj in this array corresponds to a stock's CURRENT info
	   however, a lot of this info isnt necessary (for autocomplete) ,
	   so we filter it down*/
	$.each(data, function(){
		autocompleteData.push(
				{value: this.symbol,
				name: companies[this.symbol],
				price: this.LastTradePriceOnly
				});
	});

	$("#ticker-search").on('keypress', function(e){
		//Only execute this when you have selected a company and your
		//two option buttons are showing

		if($('.catchup').css('display') == 'block'){
			$(".catchup").css("display", "none");
			$(".today").css("display", "none");
		}
	});

	$("#ticker-search").autocomplete({
		source: autocompleteData,

		select: function(event, ui){
			$("#ticker-search").val(ui.item.value)

			// show buttons & hide input bar here
			$(".catchup").css("display", "block");
			$(".today").css("display", "block");
			$(".info-text").css("display", "none");

			//change the size of the input bar
			$("#custom-search-input").addClass("col-md-8");
			$("#custom-search-input").addClass("col-md-offset-2");
			return true;

		},
		focus: function(event, ui) {

			var ul = $('#ui-id-1');
			var items = [];
			$("#ui-id-1 li").each(function() { items.push($(this).find('.ticker-content').text()) });
			var index = items.indexOf(ui.item.label) + 1;
			var el = $("#ui-id-1 li:nth-child("+index+")");

			// remove class from all items
			items.forEach(function(item){
				var ind = items.indexOf(item) + 1;
				var removeFocusEl = $("#ui-id-1 li:nth-child("+ind+")");
				removeFocusEl.removeClass('item-focus');
				$(removeFocusEl).off('click');
			});

			// add back class to the one that's currently focused
			el.addClass('item-focus');

			$(el).on('click', function(e){
				console.log('clicked!');
				$("#ticker-search").val(ui.item.value)
				$(".info-text").css("display", "none");

				// show buttons & hide input bar here

				return true;

			});

		},
		autoFocus: true,

	minLength:1,

	}).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
		$(".info-text").css("display", "none");
		return $( "<li class='ui-menu-item'></li>" )
		.data('ui-autocomplete-item', item)
		.append( "<div class='row item-height'><div class='dropdown item-height col-md-12'><div class='ticker-content'>" + item.value + "</div><div class='compName-content'>" + item.name + "</div><div class='price'>" + item.price + "</div></div></div>")
		.appendTo( ul );
    };

    /* listens for click on search button, someone refactor this*/
	
	$(".catchup-button").on("click", function(e){
		var ticker = $('#ticker-search').val().toUpperCase();
	    window.location.href = '/chart/' + ticker + "?p=1";
	});

	$(".today-button").on("click", function(e){
		var ticker = $('#ticker-search').val().toUpperCase();
	    window.location.href = '/chart/' + ticker;
	});

	

});


/*-----------------------------------------------------------------
   Updates timestamp every second on search page*/
var currTime = new Date();

function updateTimestamp() {
    /// Increment by one second
    currTime = new Date(currTime.getTime() + 1000);
    $('#timestamp').html(currTime.toGMTString());
}
// updates timestamp every second, bloat
$(function() {
	updateTimestamp();
	setInterval(updateTimestamp, 1000);
});
/*-------------------------------------------------------------------*/
