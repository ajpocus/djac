var DateRange = function (default_start, default_end) {
    var datepickerSelect = function(dateText, instance) {
	var start_date = $("#start-datepicker").datepicker("getDate");
	var end_date = $("#end-datepicker").datepicker("getDate");
	var start_year = start_date.getFullYear();
	var start_month = (start_date.getMonth() + 1);
	var start_day = start_date.getDate();
	var end_year = end_date.getFullYear();
	var end_month = (end_date.getMonth() + 1);
	var end_day = end_date.getDate();

	$.get("/accounts/json/",
	    {
		start_year: start_year,
		start_month: start_month,
		start_day: start_day,
		end_year: end_year,
		end_month: end_month,
		end_day: end_day,
	    },
	    success=function(data) {
		new_iface = $(data).find("#account-list");
		$("#account-list").replaceWith(new_iface);
	    },
	    dataType="html"
	);
    };	
	
    $("#start-datepicker").datepicker({
	inline: true,
	dateFormat: "mm/dd/yy",
	defaultDate: default_start,
	onSelect: datepickerSelect,
    });

    $("#end-datepicker").datepicker({
	inline: true,
	dateFormat: "mm/dd/yy",
	defaultDate: default_end,
	onSelect: datepickerSelect,
    });
};

