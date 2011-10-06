
{% 	
var awayCode = this.away_file_code,
	awayWin  = this.away_win,
	awayLoss = this.away_loss,
	awayCity = this.away_team_city,
	awayName = this.away_team_name,
	awayTeam = awayName,
	awayCheckIn = this.hfa_data.away.count,

	homeCode = this.home_file_code,
	homeWin  = this.home_win,
	homeLoss = this.home_loss,
	homeCity = this.home_team_city,
	homeName = this.home_team_name,
	homeTeam = homeName,
	homeCheckIn = this.hfa_data.home.count,
	
	otherCheckIn = this.hfa_data.other.count,
	vs = awayName +" Fans vs " + homeName + " Fans",
	status = this.status.ind,
	statusTxt = (this.status.status === "P")? this.home_time : this.status.status,
	gID = this.gameday;
	
%}



<li>
	<table id="{%=gID%}" class="teamTable">
		<thead>
			<tr>
				<td class="status">{%=statusTxt%}</td>
				<th class="checkIns"><abbr title="CheckIns">Check Ins</abbr></th>
			</tr>
		</thead>
		<tbody>
			<tr class="away">
				<th>
					<div class="">
						<a href="http://mlb.mlb.com/index.jsp?c_id={%=awayCode%}" class="team {%=awayCode%}">{%=awayName%}
							<span class="record">({%=awayWin%}-{%=awayLoss%})</span>
						</a>
					</div>
				</th>
				<td class="checkIns">{%=awayCheckIn%}</td>
			</tr>
			<tr class="home">
				<th>
					<div class="">
						<a href="http://mlb.mlb.com/index.jsp?c_id={%=homeCode%}" class="team {%=homeCode%}">
							<abbr title="{%=homeTeam%}">@ {%=homeName%}</abbr><br/>
							<span class="record">({%=homeWin%}-{%=homeLoss%})</span>
						</a>
					</div>
				</th>
				<td class="checkIns">{%=homeCheckIn%}</td>
			</tr>
			<tr class="other">
				<th>
					<div class="">
							<a href="http://www.foursquare.com" class="team jetsetter">
							<abbr title="Other">Jetsetters</abbr><br/>
							<span class="record">(Always #winning!)</span>
							</a>
					</div>
				</th>
				<td class="checkIns">{%=otherCheckIn%}</td>
			</tr>
		</tbody>

	</table>
	
	<div class="footer">
		{%
			if(this.hfa_data.home.items.length !== 0 || this.hfa_data.away.items.length !== 0) {
		%}
		<a href="#" class="launchStats" data-gameid="{%=gID%}" data-awaycheck="{%=awayCheckIn%}" data-homecheck="{%=homeCheckIn%}" data-hometeam="{%=homeTeam%}" data-awayteam="{%=awayTeam%}" data-othercheck="{%=otherCheckIn%}">View Breakdown</a>
		{%
			}
		%}
	</div>
	
	<div id="stats_{%=gID%}" title="{%=vs%}" class="dialog">
		<div class="statsBreakdown" id="table_{%=gID%}"></div>
		<ol class="homeAwayStats">
			<li id="awayTeam">
				<h2>Hey {%=awayName%} fans! Don't get a swirley!</h2>
				<div class="whosHere">
					<ol>
						{%
							if(this.hfa_data.away.items.length !== 0){
								var awayFans = this.hfa_data.away.items;
								for (var x in awayFans){
									if(awayFans.hasOwnProperty(x) && x <= 15){
										var fan = awayFans[x],
											img = fan.user.photo,
											fanData = fan.user.firstName + " from " + fan.user.homeCity;
										%}
											<li><img src="{%=img%}" alt="{%=fanData%}"/></li>
										{%
									}
								}
							}
							
						%}
					</ol>
				</div>
			</li>
			<li id="homeTeam">
				<h2>{%=homeName%} fans, represent!</h2>
				<div class="whosHere">
					<ol>
						{%
							if(this.hfa_data.home.items.length !== 0){
								var homeFans = this.hfa_data.home.items;
								for (var x in homeFans){
									
									if(homeFans.hasOwnProperty(x) && x <= 8){
										
										var fan = homeFans[x],
											img = fan.user.photo,
											fanData = fan.user.firstName + " from " + fan.user.homeCity;
											if(img !=="https://foursquare.com/img/blank_boy.png" || img !=="https://foursquare.com/img/blank_girl.png"){
										%}
											<li><img src="{%=img%}" alt="{%=fanData%}"/></li>
										{%
										}
									}
								}
							}
							
						%}
					</ol>
				</div>
			</li>
		</ol>
		
	</div>
</li>