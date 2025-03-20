import requests as rs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from wsba_nhl_scraper.data_scrape import combine_pbp_data, combine_shifts, combine_data, create_timeline 

# MAIN FUNCTIONS
def wsba_scrape_game(game_ids):
    pbps = []
    shifts_data = []
    for game_id in game_ids:
        print("Scraping data from game " + str(game_id))

        game_id = str(game_id)
        season = str(game_id[:4])+str(int(game_id[:4])+1)

        api = "https://api-web.nhle.com/v1/gamecenter/"+game_id+"/play-by-play"
        report = "https://www.nhl.com/scores/htmlreports/"+season+"/PL"+str(game_id)[-6:]+".HTM"
        home_log = "https://www.nhl.com/scores/htmlreports/"+season+"/TH"+str(game_id)[-6:]+".HTM"
        away_log = "https://www.nhl.com/scores/htmlreports/"+season+"/TV"+str(game_id)[-6:]+".HTM"

        json = rs.get(api).json()
        html = rs.get(report).content
        home_shift = rs.get(home_log).content
        away_shift = rs.get(away_log).content

        pbp = combine_pbp_data(json,html)
        shifts = combine_shifts(home_shift,away_shift,json,game_id).replace({"REMOVE":np.nan})

        pbps.append(pbp)
        shifts_data.append(shifts)
    
    pbp_df = pd.concat(pbps)
    shifts_df = pd.concat(shifts_data)

    df = combine_data(pbp_df,shifts_df)
    timeline = create_timeline(df)
    
    pbp_col = ['season','season_type','game_id','game_date',
        'away_team_abbr','home_team_abbr','event_num','event_id','period','period_type',
        "period_time_remaining",'seconds_elasped',"description",
        "situation_code","strength_state","home_team_defending_side","event_type_code","event_type",
        "shot_type","event_team_abbr","event_team_status","event_player_1_id","event_player_2_id","event_player_3_id",
        "event_player_1_name","event_player_2_name","event_player_3_name","event_player_1_pos","event_player_2_pos",
        "event_player_3_pos","event_goalie_id",
        "event_goalie_name","zone_code","x","y","x_fixed","y_fixed","x_adj","y_adj",
        "event_skaters","away_skaters","home_skaters",
        "event_distance","event_angle","away_score","home_score", "away_fenwick", "home_fenwick",
        "away_on_1","away_on_2","away_on_3","away_on_4","away_on_5","away_on_6","away_goalie",
        "home_on_1","home_on_2","home_on_3","home_on_4","home_on_5","home_on_6","home_goalie"]
    shifts_col = ['season', 'season_type', 'game_id', 'game_date', 'away_team_abbr', 'home_team_abbr', 'period', 'seconds_elasped', 
                  'strength_state', 'event_type', 'description', 'team_abbr', 'num_on', 'players_on', 'ids_on', 'num_off', 'players_off', 'ids_off', 'game_seconds_remaining',
                  'away_skaters', 'home_skaters', 
                  'away_on_1', 'away_on_2', 'away_on_3', 'away_on_4', 'away_on_5', 'away_on_6', 'away_goalie', 
                  'home_on_1', 'home_on_2', 'home_on_3', 'home_on_4', 'home_on_5', 'home_on_6', 'home_goalie'
                  ]
    
    remove = ['period-start','period-end','challenge','stoppage','change']
    return {"pbp":df.loc[~df['event_type'].isin(remove)][pbp_col],
            "shifts":df.loc[df['event_type']=='change'][shifts_col],
            "timeline":timeline
            }

                          

def wsba_scrape_schedule(season,start = "09-01", end = "08-01"):
    api = "https://api-web.nhle.com/v1/schedule/"

    new_year = ["01","02","03","04","05","06"]
    if start[:2] in new_year:
        start = str(int(season[:4])+1)+"-"+start
        end = str(season[:-4])+"-"+end
    else:
        start = str(season[:4])+"-"+start
        end = str(season[:-4])+"-"+end

    form = '%Y-%m-%d'

    start = datetime.strptime(start,form)
    end = datetime.strptime(end,form)

    game = []

    day = (end-start).days+1
    if day < 0:
        day = 365 + day
    for i in range(day):
        inc = start+timedelta(days=i)
        print("Scraping games on " + str(inc)[:10]+"...")
        
        get = rs.get(api+str(inc)[:10]).json()
        gameWeek = list(pd.json_normalize(get['gameWeek'])['games'])[0]

        for i in range(0,len(gameWeek)):
            game.append(pd.DataFrame({
                "id": [gameWeek[i]['id']],
                "season": [gameWeek[i]['season']],
                "season_type":[gameWeek[i]['gameType']],
                "game_center_link":[gameWeek[i]['gameCenterLink']]
                }))
    
    df = pd.concat(game)
    return df.loc[df['season_type']>1]

def wsba_scrape_season(season,start = "09-01", end = "08-01", local=False, local_path = ""):
    if local == True:
        load = pd.read_csv(local_path)
        load = load.loc[load['season'].astype(str)==season]
        game_ids = list(load['id'].astype(str))
    else:
        game_ids = list(wsba_scrape_schedule(season,start,end)['id'].astype(str))

    df = []
    df_s = []
    df_t = []
    errors = {}
    for game_id in game_ids: 
        try:
            data = wsba_scrape_game([game_id])
            df.append(data['pbp'])
            df_s.append(data['shifts'])
            df_t.append(data['timeline'])

        except: 
            print("An error occurred...")
            errors.update({
                "id": game_id,
            })

    
    pbp = pd.concat(df)
    shifts = pd.concat(df_s)
    timelines = pd.concat(df_t)
    errors = pd.DataFrame([errors])

    return {"pbp":pbp,
            'shifts':shifts,
            "timeline":timelines,
            "errors":errors}

def wsba_scrape_seasons_info(seasons = []):
    import requests as rs
    import pandas as pd

    api = "https://api.nhle.com/stats/rest/en/season"
    info = "https://api-web.nhle.com/v1/standings-season"
    data = rs.get(api).json()['data']
    data_2 = rs.get(info).json()['seasons']

    df = pd.json_normalize(data)
    df_2 = pd.json_normalize(data_2)

    df = pd.merge(df,df_2,how='outer',on=['id'])
    
    if len(seasons) > 0:
        return df.loc[df['id'].astype(str).isin(seasons)].sort_values(by=['id'])
    else:
        return df.sort_values(by=['id'])


def wsba_scrape_standings(arg = "now"):
    import requests as rs
    import pandas as pd
    
    api = "https://api-web.nhle.com/v1/standings/"+arg
    
    data = rs.get(api).json()['standings']

    return pd.json_normalize(data)