# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    team_id = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    other_names = scrapy.Field()
    seasons = scrapy.Field()
    seasons_years = scrapy.Field()
    tot_record = scrapy.Field()
    tot_record_pct = scrapy.Field()
    playoffs = scrapy.Field()
    championships = scrapy.Field()
    
    # per season stats
    season_year = scrapy.Field()
    g = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    mp = scrapy.Field()
    fg = scrapy.Field()
    fga = scrapy.Field()
    fg_pct = scrapy.Field()
    fg3 = scrapy.Field()
    fg3a = scrapy.Field()
    fg3_pct = scrapy.Field()
    fg2 = scrapy.Field()
    fg2a = scrapy.Field()
    fg2_pct = scrapy.Field()
    ft = scrapy.Field()
    fta = scrapy.Field()
    ft_pct = scrapy.Field()
    orb = scrapy.Field()
    drb = scrapy.Field()
    trb = scrapy.Field()
    ast = scrapy.Field()
    stl = scrapy.Field()
    blk = scrapy.Field()
    tov = scrapy.Field()
    pf = scrapy.Field()
    pts = scrapy.Field()
    off_rtg = scrapy.Field()
    def_rtg = scrapy.Field()
    arena_name = scrapy.Field()
    attendance =scrapy.Field()

    # Other season stats
    total_salary = scrapy.Field()
    avg_player_salary = scrapy.Field()
    avg_team_exp = scrapy.Field()
    avg_team_age = scrapy.Field()
    exp_variance = scrapy.Field()
    