from django.shortcuts import render, redirect
from django.db.models import Count
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"atl_conf": Team.objects.filter(league__name="Atlantic Soccer Conference"),
		"current_penguins": Player.objects.filter(curr_team__team_name__contains="Penguins"),
		"current_collegiate": Player.objects.filter(curr_team__league__name="International Collegiate Baseball Conference"),
		"current_amfootball_lopez": Player.objects.filter(curr_team__league__name="American Conference of Amateur Football", last_name="Lopez"),
		"all_football": Player.objects.filter(curr_team__league__sport__icontains="football"),
		"teams_sophia": Team.objects.filter(curr_players__first_name="Sophia"),
		"leagues_sophia": League.objects.filter(teams__curr_players__first_name="Sophia"),
		"flores": Player.objects.filter(last_name="Flores").exclude(curr_team__team_name="Roughriders"),
		"sam_evans": Team.objects.filter(all_players__first_name="Samuel", all_players__last_name="Evans"),
		"all_manitoba": Player.objects.filter(all_teams__team_name="Tiger-Cats"),
		"former_vikings": Player.objects.filter(all_teams__team_name="Vikings").exclude(curr_team__team_name="Vikings"),
		"jacob_gray_former": Team.objects.filter(all_players__first_name="Jacob", all_players__last_name="Gray").exclude(curr_players__first_name="Jacob", curr_players__last_name="Gray"),
		"all_joshua": Player.objects.filter(first_name="Joshua", all_teams__league__name="Atlantic Federation of Amateur Baseball Players"),
		"over_twelve": Team.objects.annotate(player_count=Count('all_players')).filter(player_count__gt=11),
		"sort_by_num": Player.objects.annotate(team_count=Count('all_teams')).order_by("team_count")

	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")