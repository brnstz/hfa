function yesterday_getUrlParam (paramName,hash) {
	var searchString = window.location.search.substring(1),
		  i, val, params = searchString.split("&");
		if(hash){
			searchString = window.location.hash;
		}
	  for (i=0;i<params.length;i++) {
		val = params[i].split("=");
		if (val[0] == paramName) {
		  return unescape(val[1]);
		}
	  }
	  return null;
}

function getPreviousDate() {
	var mydate = yesterday_getUrlParam("date");
	var mydateobj;
	if (mydate === null) {
		mydateobj = new Date();
	} else {
		mydateobj = new Date(Date.parse(mydate));
	}

	var today_mil = mydateobj.getTime();
	var yesterday_mil = today_mil - 86400000;
	var yesterday_obj = new Date(yesterday_mil);

	var yesterday_day = yesterday_obj.getUTCDate();
	var yesterday_month = yesterday_obj.getUTCMonth() + 1;
	var yesterday_year = yesterday_obj.getUTCFullYear();

	if (yesterday_day < 10) {
		yesterday_day = "0" + yesterday_day;
	}
	if (yesterday_month < 10) {
		yesterday_month = "0" + yesterday_month;
	}

	var yesterday_str = "" + yesterday_year + "-" + yesterday_month + "-" + yesterday_day;

	return yesterday_str;
}
