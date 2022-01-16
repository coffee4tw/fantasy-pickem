import requests
from bs4 import BeautifulSoup

class Matchup():

	def __init__(self, rank):
		self.rank = rank;
		self.home_team = ""
		self.away_team = ""
		self.home_pct = ""
		self.away_pct = ""
		self.confidence_rank = -1

	def __str__(self):
		return "{}: {} ({}) @ {} ({}) -- {} {}".format(self.rank, self.away_team, self.away_pct, self.home_team, self.home_pct, self.get_pick(), self.get_confidence_rank())

	def get_pick(self):
		if self.home_pct < self.away_pct:
			return self.away_team
		else:
			return self.home_team

	def get_confidence_pct(self):
		if self.home_pct < self.away_pct:
			return self.away_pct
		else:
			return self.home_pct

	def get_confidence_rank(self):
		return self.confidence_rank

if __name__ == '__main__':
	source_url = "https://football.fantasysports.yahoo.com/pickem"
	picks_url = "https://gridirongames.com/football-pools/nfl-pickem/pool-11472/"
	page = requests.get(source_url)

	soup = BeautifulSoup(page.content, "html.parser")
	pickem_table = soup.find_all("tbody", class_="ysptblcontent1")
	rows = pickem_table[0].find_all("tr")

	matchups = list()
	rank = 1
	match = Matchup(rank)
	for i in range(len(rows)):
		row = rows[i]
		pct = row.find("td", class_="number").text
		pct = int(pct[:len(pct)-1])
		team = row.find("td", class_="l").text
		# print(row.text, "==" , pct, team)

		if "@" in team:
			match.home_team = team[2:]
			match.home_pct = pct
		else:
			match.away_team = team
			match.away_pct = pct

		if i % 2 == 1:
			matchups.append(match)
			rank += 1
			match = Matchup(rank)

	print("*** SORTED BY CONFIDENCE ***")
	sorted_matchups = sorted(matchups, key=lambda x: x.get_confidence_pct())
	sorted_matchups.reverse()
	for i in range(len(sorted_matchups)):
		m = sorted_matchups[i]
		m.confidence_rank = len(sorted_matchups)-i
		print(m)

	print("*** SORTED BY SCHEDULE ***")
	for m in matchups:
		print(m)

	params = {
		"TB1": 38
	}
	for m in matchups:
		params["G{}".format(m.rank)] = m.get_pick()
		params["P{}".format(m.rank)] = m.get_confidence_rank()

	# res = requests.post(picks_url, params)
