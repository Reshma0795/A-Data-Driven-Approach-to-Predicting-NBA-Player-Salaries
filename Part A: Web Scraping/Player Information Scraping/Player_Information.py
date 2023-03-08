from bs4 import BeautifulSoup, Comment
import requests
import csv
import time

def is_comment(element): 
    return isinstance(element, Comment)

draftpickinitialisingurl = "https://www.basketball-reference.com/players/a/afflaar01.html"
draftpickr = requests.get(draftpickinitialisingurl).text
draftpicksoup = BeautifulSoup(draftpickr, 'lxml')
draftallparas = draftpicksoup.find_all('p')
draftreqtext = draftallparas[9].find('strong').text
rankreqtext = draftallparas[8].find('strong').text

url_part1 = 'https://www.basketball-reference.com/leagues/NBA_'
url_part2 = '_totals.html'
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
salaryyears = ['2009-10','2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21']
urlamt = len(years)

cols = [['Player', 'Year', 'Season', 'Draft', 'Rank', 'Experience','Height','Weight','Pos','Age','Tm','G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P',
'2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','PER','TS%','BPM','WS','Player_Career_Salary','Player_Season_Salary']]

with open('final.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(cols)
try:
    for i in range(0, urlamt):
        print(f'{i+1} Done out of : {urlamt+1} years')
        url = url_part1 + str(years[i]) + url_part2
        player_salaries = []
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml')
        players = soup.find_all('td', {"data-stat":"player"})
        positions = soup.find_all('td', {"data-stat":"pos"})
        ages = soup.find_all('td', {"data-stat":"age"})
        teams = soup.find_all('td', {"data-stat":"team_id"})
        games = soup.find_all('td', {"data-stat":"g"})
        games_starteds = soup.find_all('td', {"data-stat":"gs"})
        minutes_playeds = soup.find_all('td', {"data-stat":"mp"})
        field_goals = soup.find_all('td', {"data-stat":"fg"})
        field_goal_attempts = soup.find_all('td', {"data-stat":"fga"})
        field_goal_percentages = soup.find_all('td', {"data-stat":"fg_pct"})
        three_pointers = soup.find_all('td', {"data-stat":"fg3"})
        three_pointers_attempts = soup.find_all('td', {"data-stat":"fg3a"})
        three_pointers_percentages = soup.find_all('td', {"data-stat":"fg3_pct"})
        two_pointers = soup.find_all('td', {"data-stat":"fg2"})
        two_pointers_attempts = soup.find_all('td', {"data-stat":"fg2a"})
        two_pointers_percentages = soup.find_all('td', {"data-stat":"fg2_pct"})
        effective_field_goal_percentages = soup.find_all('td', {"data-stat":"efg_pct"})
        free_throws = soup.find_all('td', {"data-stat":"ft"})
        free_throws_attempts = soup.find_all('td', {"data-stat":"fta"})
        free_throws_percentages = soup.find_all('td', {"data-stat":"ft_pct"})
        offensive_rebounds = soup.find_all('td', {"data-stat":"orb"})
        defensive_rebounds = soup.find_all('td', {"data-stat":"drb"})
        total_rebounds = soup.find_all('td', {"data-stat":"trb"})
        assists = soup.find_all('td', {"data-stat":"ast"})
        steals = soup.find_all('td', {"data-stat":"stl"})
        blocks = soup.find_all('td', {"data-stat":"blk"})
        turnovers = soup.find_all('td', {"data-stat":"tov"})
        personal_fouls = soup.find_all('td', {"data-stat":"pf"})
        points = soup.find_all('td', {"data-stat":"pts"})
        year = years[i]
        season = salaryyears[i]
        amt = len(players)
        for j in range(0, amt):
            time.sleep(3)
            print(f'{j+1} Done out of : {amt+1} players in the {i+1} Done out of : {urlamt+1} years range')
            player_link = players[j].find('a').get('href')
            player_url = 'https://www.basketball-reference.com' + player_link
            pr = requests.get(player_url).text
            psoup = BeautifulSoup(pr, 'lxml')
            height = psoup.find('span', {"itemprop":"height"}).text
            weight = psoup.find('span', {"itemprop":"weight"}).text
            drafters = psoup.find_all('p')
            draft = "n/a"
            rank = "n/a"
            experience = "n/a"
            year_salary = "n/a"
            advance_text = "advanced."
            per = "n/a"
            tsp = "n/a"
            bpm = "n/a"
            ws = "n/a"
            try:
                advancers =  psoup.find_all('tr', {"id" : advance_text+year})
                adsoup = BeautifulSoup(str(findallcomments), 'lxml')
                per = adsoup.find('td', {"data-stat" : "per"}).text
                tsp = adsoup.find('td', {"data-stat" : "ts_pct"}).text
                bpm = adsoup.find('td', {"data-stat" : "bpm"}).text
                ws = adsoup.find('td', {"data-stat" : "ws"}).text
            except:
                print("no advanced stats")
            try:
                for para in drafters:
                    if para.find('strong') and para.find('a'):
                        if para.find('strong').text == draftreqtext:
                            draft = para.find('a').text
            except:
                print("No change")
            try:
                for para in drafters:
                    if para.find('strong') and para.find('a'):
                        if para.find('strong').text == rankreqtext:
                            rank = para.find('a').next_sibling.text.split('(')[1].split(')')[0]
            except:
                print("No change")
            try:
                for para in drafters:
                    if para.find('strong'):
                        if para.find('strong').text == 'Career Length:':
                            experience = para.find('strong').next_sibling.text.split(' ')[0].split('\xa0')[1]
                        if para.find('strong').text == 'Experience:':
                            experience = para.find('strong').next_sibling.text.split(' ')[0].split('\xa0')[1]
            except:
                print("No change")

            try:
                findallcomments = psoup.find_all(text=is_comment)
                for element in findallcomments:
                    elementsoup = BeautifulSoup(str(element), 'lxml')
                    tfoots = elementsoup.find_all('tfoot')
                    for salary in tfoots:
                        salarysoup = BeautifulSoup(str(salary), 'lxml')
                        salaries = salarysoup.find_all('td', {"data-stat":"salary"})
                        for salary in salaries:
                            player_salary = salary.text
                try:
                    for element in findallcomments:
                        elementsoup = BeautifulSoup(str(element), 'lxml')
                        trrer = elementsoup.find_all('tr')
                        for tr in trrer:
                            trsoup = BeautifulSoup(str(tr), 'lxml')
                            tds = trsoup.find_all('th', {"data-stat":"season"})
                            for td in tds:
                                if td.text == salaryyears[i]:
                                    if td.next_sibling.next_sibling.next_sibling.text[0] == '$':
                                        year_salary = td.next_sibling.next_sibling.next_sibling.text
                except:
                    print("No change")
                entirelist = []
                player = players[j].text
                position = positions[j].text
                age = ages[j].text
                team = teams[j].text
                game = games[j].text
                games_started = games_starteds[j].text
                minutes_played = minutes_playeds[j].text
                field_goal = field_goals[j].text
                field_goal_attempt = field_goal_attempts[j].text
                field_goal_percentage = field_goal_percentages[j].text
                three_pointer = three_pointers[j].text
                three_pointers_attempt = three_pointers_attempts[j].text
                three_pointers_percentage = three_pointers_percentages[j].text
                two_pointer = two_pointers[j].text
                two_pointers_attempt = two_pointers_attempts[j].text
                two_pointers_percentage = two_pointers_percentages[j].text
                effective_field_goal_percentage = effective_field_goal_percentages[j].text
                free_throw = free_throws[j].text
                free_throws_attempt = free_throws_attempts[j].text
                free_throws_percentage = free_throws_percentages[j].text
                offensive_rebound = offensive_rebounds[j].text
                defensive_rebound = defensive_rebounds[j].text
                total_rebound = total_rebounds[j].text
                assist = assists[j].text
                steal = steals[j].text
                block = blocks[j].text
                turnover = turnovers[j].text
                personal_foul = personal_fouls[j].text
                point = points[j].text
                entirelist = [[player,year,season,draft,rank,experience,height,weight,position,age,team,game,games_started,minutes_played,field_goal,field_goal_attempt,field_goal_percentage,three_pointer,three_pointers_attempt,three_pointers_percentage,two_pointer,two_pointers_attempt,two_pointers_percentage,effective_field_goal_percentage,free_throw,free_throws_attempt,free_throws_percentage,offensive_rebound,defensive_rebound,total_rebound,assist,steal,block,turnover,personal_foul,point,per,tsp,bpm,ws,player_salary,year_salary]]
                with open('final.csv', 'a', newline='') as file:
                    mywriter = csv.writer(file, delimiter=',')
                    mywriter.writerows(entirelist)
            except Exception as e:
                print(e)
                print('error')
                continue
except:
    message = "Web Scrapping Started"
