import pandas as pd
import scrapy
import os
import re
import logging
from scrapy.utils.log import configure_logging 
from team_scraping.items import TeamItem

class bballReferenceTeamsSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logfile.txt',
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO
    )
    
    name = "teams"
    referenceURL = 'https://www.basketball-reference.com/'
    
    def start_requests(self):
        urls = [
            'https://www.basketball-reference.com/teams/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_initial)
    
    # table_headers = ['g', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'fg2', 'fg2a', 'fg2_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'wins', 'losses']
    
    df = pd.DataFrame()
    table_headers = []
    
    def parse_initial(self, response):
        print('Started crawling for teams from the following URL: ', response.url)
    
        
        teams_list = response.xpath('//*[@id="teams_active"]/tbody/tr/th/a').getall()
        # print(teams_list)
        
        for team in teams_list:
            x = re.split(">", team)
            team_link = re.search(r'\"(.*?)\"',x[0]).group(1)
            
            team_id = team_link.split("/")[2]
            
            team_name = re.split("<",x[1])[0]
            team_url = response.urljoin(team_link)
            
            # if team_name == 'New York Knicks':
            yield scrapy.Request(team_url,callback=self.parse_team_basic, meta= { "team_name":team_name , "team_id":team_id}, dont_filter=False)
            # break

    def parse_team_basic(self, response):
        details = response.xpath('//*[@id="meta"]/div[2]/p').getall()
        print(response.meta['team_name'])
        team_id = response.meta['team_id']
        team_data = TeamItem()
        team_data['team_id'] = team_id
        team_data['name'] = response.meta['team_name']
        for elem in details:
            # print(elem)
            # x = re.search(r'\>(.*?)\<',elem)
            x = re.findall('\>([^<]+)', elem)
            
            item = x[1].replace(':','')
            data = re.findall('\\n([^\\n]+)', x[2])
            data = [x.strip(' ') for x in data]
            if item == 'Location':
                team_data['location'] = data[0]
            elif item == 'Team Names' or item == 'Team Name':
                team_data['other_names'] = data[0]
            elif item == 'Seasons':
                team_data['seasons'] = data[1].replace(';','')
                team_data['seasons_years'] = data[3]
            elif item == 'Record':
                record = re.split(' ', data[0].replace(',', ''))
                team_data['tot_record'] = record[0]
                team_data['tot_record_pct'] = record[1]
            elif item == 'Playoff Appearances':
                team_data['playoffs'] = data[0]
            elif item == 'Championships':
                team_data['championships'] = data[0]
            else:
                pass
        
        links = response.xpath('//*[@id="' + team_id + '"]/tbody/tr/th/a/@href').getall()
        seasons = response.xpath('//*[@id="' + team_id + '"]/tbody/tr/th/a/text()').getall()
        # print(links)
        # print(seasons)
        seasons_covered = {
        "2009-10": False,
        "2010-11": False,
        "2011-12": False,
        "2012-13": False,
        "2013-14": False,
        "2014-15": False,
        "2015-16": False,
        "2016-17": False,
        "2017-18": False,
        "2018-19": False,
        "2019-20": False,
        "2020-21": False
        }
        for i, season in enumerate(seasons):
            if all(value == True for value in seasons_covered.values()):
                break
            
            if season in seasons_covered.keys():
                season_link = response.urljoin(links[i])
                yield scrapy.Request(season_link,callback=self.parse_team_season, meta= { "team_data":team_data, "season": season}, dont_filter=False)
                seasons_covered[season] = True
                # break
            else:
                continue
        
        
    def parse_team_season(self, response):
        team_data = response.meta['team_data']
        team_data['season_year'] = response.meta['season']
        print("Inside seasonal stats")
        
        # table = soup.find(id="team_and_opponent")
        
        headers_to_use =  response.xpath('//comment()').re(r'<th.*data-stat="(.?\w*).*</th>')
        
        for item in headers_to_use:
            if item in team_data.fields:
                if item not in self.table_headers:
                    self.table_headers.append(item)
        # value_to_use = response.xpath('//comment()').re(r'<thead><tr><th.*data-stat="player" >Team.*<td.*data-stat="' +'" >(.?\w*)</thead>')
        
        # f = open("new_file.txt", "a")
        # f.write(response.text)
        # f.close()
        # print(self.table_headers)
        for field in self.table_headers:
            value = response.xpath('//comment()').re(r'<tbody><tr ><th.*data-stat="player" >Team.*<td.*data-stat="'+ field + '" >(.?[a-zA-Z0-9,. ()&amp;]*)</td>')
            team_data[field] = value[0] if value else ""
            
        if team_data['arena_name'] != "":
            team_data['arena_name'] = team_data['arena_name'].replace('amp;', '')
            
        if team_data['attendance'] != "":
            team_data['attendance'] = int(team_data['attendance'].replace(',', ''))
            
        salaries = response.xpath('//comment()').re(r'<td.*data-stat="salary".*>\$(.*)</td>')
        salaries = [int(s.replace(',', '')) for s in salaries]
        
        team_data['total_salary'] = sum(salaries)
        team_data['avg_player_salary'] = round(sum(salaries)/ len(salaries),2)
        
        ages = response.xpath('//div[@id="div_per_game"] /table /tbody /tr /td[@data-stat="age"] /text()').getall()
    
        ages = [int(s) for s in ages]
        team_data['avg_team_age'] = round(sum(ages)/ len(ages),2)
        
        
        total_exp = response.xpath('//td [@data-stat="years_experience"] /text()').getall()
        
        total_exp = [0 if 'R' in s else int(s.replace(',', '')) for s in total_exp]
        team_data['avg_team_exp'] = round((sum(total_exp))/ len(total_exp),2)
        
        v = 0
        for e in total_exp:
            v = v + (e - team_data['avg_team_exp'])**2
        
        team_data['exp_variance'] = v / len(total_exp)-1
        
        # self.df = self.df.append(dict(team_data), ignore_index=True)
        
        df_new_row = pd.DataFrame([dict(team_data)])
        output_path='team_data.csv'
        df_new_row.to_csv(output_path, mode='a',index=False, header=not os.path.exists(output_path))  
        
        # print(df_new_row.head())
        # print(team_data)
        