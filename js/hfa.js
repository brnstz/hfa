	var hfa = (function(){
		var dialogObj = {show: "blind",hide: "blind", width: 650},
			selectVal = "",
			getUrlParam = function(paramName,hash){
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
			},

			launchDialog = function(gameID){
				$( "#stats_"+gameID ).dialog(dialogObj);
			},
			authDialog = function(){
				$(".login").dialog();
			},
			generateTable = function(gameID,homeTeam,awayTeam,homeCheckIn,awayCheckIn, otherCheckIn){
				$("#table_"+gameID).empty();
					var total = homeCheckIn + awayCheckIn + otherCheckIn,
					homePercent = (homeCheckIn/total)*100,
					awayPercent = (awayCheckIn/total)*100,
					otherPercent = (otherCheckIn/total)*100;
					if(awayPercent !==0 && homePercent !== 0 && otherPercent !==0){
						var r = Raphael("table_"+gameID),
							pie = r.g.piechart(300, 150, 110, [homePercent,awayPercent, otherPercent], {legend: [homeTeam, awayTeam, "Jetsetters"], legendpos: "west", colors: ["90-#0CBADF:10-#fff","90-#FF6600:10-#fff","90-#ff0000:10-#000"], stroke: "#000"});
					}
			},
			_self = {
			getUrlParam : getUrlParam,
			getData : function(){
					var dfd = jQuery.Deferred(),
						tpl = "tpl/gameBox2.tpl",
						$list = $("#hfa ol"),
						getDate = getUrlParam("date");
						if (getDate === null) {
							var url = "http://hfa.brnstz.com/scoreboard.jsonp?callback=?"
						} else {
							var url = "http://hfa.brnstz.com/scoreboard.jsonp?date="+getDate+"&callback=?"
						}
						
					$.getJSON(url, function(json) {
						var total = json.data.total_checkins;
						$("#totalCheckins").html("Total Checkins: " + total)
						var game = json.data.games.game;
							$.each(game, function(i){
								var g = game[i];
								var tmp = $.template(tpl,g,true);
								$(tmp).appendTo($list);
							});
							dfd.resolve();
							$("#loader").hide();
					});
					
					return dfd.promise();
			},
			oauthUser: function(club){
				var CLIENT_ID = "5GJJEF4DNR1UKAC55XYIBTX2ZEBJ2ZBWH1N3FYIXITRJBSBK",
					YOUR_REGISTERED_REDIRECT_URI = "http://hfa.brnstz.com/success.html",
					_url = "https://foursquare.com/oauth2/authenticate?client_id="+CLIENT_ID+"&response_type=token&redirect_uri="+YOUR_REGISTERED_REDIRECT_URI;
				
				window.location.href = _url + "&" + club;
			},
			init: function(){
				$.when( hfa.getData() ).done(function(){
					
					$("#datepicker").datepicker({ 
						minDate: new Date(2011, 8, 17), 
						maxDate: new Date(),
						showOn: "button",
						buttonImage: "img/calendar.gif",
						buttonImageOnly: true,
						onSelect: function(dateText, inst) {

							var year = dateText.substring(6),
								month = dateText.substring(0,2),
								day   = dateText.substring(3,5),
								dateString = year+"-"+month+"-"+day,
								url = window.location.host + window.location.pathname + "?date="+dateString;

								window.location.href = "http://" + url;
						}
					});
					
					$(".launchStats").bind("click", function(){
						var $thisGameID = $(this).data("gameid"),
							homeTeam = $(this).data("hometeam"),
							awayTeam = $(this).data("awayteam"),
							homeCheckIn = $(this).data("homecheck"),
							otherCheckIn = $(this).data("othercheck"),
							awayCheckIn = $(this).data("awaycheck");
						launchDialog($thisGameID);
						generateTable($thisGameID,homeTeam,awayTeam,homeCheckIn,awayCheckIn,otherCheckIn);
						
					});
					
					$("#teamChoice").bind("click", function(){
						$(".login").slideDown();
					});
					
					$("#connectToFsq").bind("click", function(){
						hfa.oauthUser();
					});
					
					$("#teamSelect").bind("change", function(){
						selectVal = $(this).val();
						$("#connectToFsq").fadeIn();
						if(selectVal ===""){
							$("#connectToFsq").hide();
						}
					});
					
				});	
			}
		}
		return _self
}());