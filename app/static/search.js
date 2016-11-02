
$(document).ready(function() {
	$("#ticker-search").on('keyup', function (e) {
	    if (e.keyCode == 13) {
	    	var ticker = $('#ticker-search').val().toUpperCase();
	        window.location.href = '/stock/' + ticker;
	    }
	});

	var availableTutorials = [
	{
		value: "AAPL",
		name: "Apple",
		price: 100
	},
	{
		value: "AXP",
		name: "American Express",
		price: 100 
	},
	{
		value: "BA",
		name: "Boeing",
		price: 100 
	},
	{
		value: "CAT",
		name: "Caterpillar",
		price: 100 
	},
	{
		value: "CSCO",
		name: "Cisco Systems",
		price: 100 
	},
	{
		value: "CVX",
		name: "Chevron",
		price: 100 
	},
	{
		value: "KO",
		name: "Coca Cola",
		price: 100 
	},
	{
		value: "DD",
		name: "DuPont",
		price: 100 
	},
	{
		value: "XOM",
		name: "ExxonMobil",
		price: 100 
	},
	{
		value: "GE",
		name: "General Electric",
		price: 100 
	},
	{
		value: "GS",
		name: "Goldman Sachs",
		price: 100 
	},
	{
		value: "HD",
		name: "Home Depot",
		price: 100 
	},
	{
		value: "IBM",
		name: "IBM",
		price: 100 
	},
	{
		value: "INTC",
		name: "Intel",
		price: 100 
	},
	{
		value: "JNJ",
		name: "Johnson & Johnson",
		price: 100 
	},
	{
		value: "JPM",
		name: "JPMorgan Chase",
		price: 100 
	},
	{
		value: "MCD",
		name: "McDonalds",
		price: 100 
	},
	{
		value: "MMM",
		name: "3M Company",
		price: 100 
	},
	{
		value: "MRK",
		name: "Merck",
		price: 100 
	},
	{
		value: "MSFT",
		name: "Microsoft",
		price: 100 
	},
	{
		value: "NKE",
		name: "Nike",
		price: 100 
	},
	{
		value: "PFE",
		name: "Pfizer",
		price: 100 
	},
	{
		value: "PG",
		name: "Proctor & Gamble",
		price: 100 
	},
	{
		value: "TRV",
		name: "The Travelers",
		price: 100 
	},
	{
		value: "UNH",
		name: "UnitedHealth",
		price: 100 
	},
	{
		value: "UTX",
		name: "United Technologies",
		price: 100 
	},
	{
		value: "V",
		name: "Vise",
		price: 100 
	},
	{
		value: "VZ",
		name: "Verizon",
		price: 100 
	},
	{
		value: "WMT",
		name: "Wal-Mart",
		price: 100 
	},
	{
		value: "DIS",
		name: "Walt Disney",
		price: 100 
	}
];
	$("#ticker-search").autocomplete({
		source: availableTutorials,

		select: function(event, ui){
			$("#ticker-search").val(ui.item.value)

			// show buttons & hide input bar here 
			
			$("#ticker-search").hide();

			console.log("Hannah")
			return false;

		},
		focus: function(event, ui) {
			console.log(event);
			console.log(ui);
			console.log('here!');

		},
		autoFocus: true,

	minLength:0,

	}).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
		return $( "<li class='ui-menu-item'></li>" )
		.data('ui-autocomplete-item', item)
		.append( "<div class='row'>" + "<div class='col-md-4'>" + "<div class='ticker-content'>" + item.value + "</div>" + "</div>" + "<div class='col-md-4'>" + "<div class='compName-content'>" + item.name + "</div>" + "</div>" + "<div class='col-md-4'>" + "<div class='price'>" + item.price + "</div>" + "</div>" + "</div>")
		.appendTo( ul );
    };

});

