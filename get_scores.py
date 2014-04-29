#===============================================================================
import pytz
import datetime
import time
import urllib2
import json
import os
import elementtree.ElementTree as ET
import utils
from utils import Game
import env_settings
#-------------------------------------------------------------------------------
URL = "http://scores.nbcsports.msnbc.com" + \
        "/ticker/data/gamesMSNBC.js.asp?jsonp=true&sport=%s&period=%d"
#-------------------------------------------------------------------------------
def today(league):
    yyyymmdd = int(datetime.datetime.now(\
            pytz.timezone('US/Pacific')).strftime("%Y%m%d"))
    games = []
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            f = urllib2.urlopen(URL % (league, yyyymmdd))
            jsonp = f.read()
            f.close()
            json_str = jsonp.replace(\
                    'shsMSNBCTicker.loadGamesData(', '').replace(');', '')
            json_parsed = json.loads(json_str)
            for game_str in json_parsed.get('games', []):
                game_tree = ET.XML(game_str)
                visiting_tree = game_tree.find('visiting-team')
                home_tree = game_tree.find('home-team')
                gamestate_tree = game_tree.find('gamestate')
                home = home_tree.get('alias').strip("#1234567890 ")
                away = visiting_tree.get('alias').strip("#1234567890 ")
                game_start = int(time.mktime(time.strptime(\
                        '%s %d' % (gamestate_tree.get('gametime'), yyyymmdd),\
                        '%I:%M %p %Y%m%d')))
                start = datetime.datetime.fromtimestamp(\
                        game_start,
                        pytz.timezone('US/Pacific')).strftime('%I:%M %p')
                start = utils.localize_game_time(start, env_settings.LOCAL_TZ)

                games.append({
                    'league': league.rstrip(),
                    'start': start.rstrip(),
                    'home': home.rstrip(),
                    'away': away.rstrip(),
                    'home-score': home_tree.get('score').rstrip(),
                    'away-score': visiting_tree.get('score').rstrip(),
                    'status': gamestate_tree.get('status').rstrip(),
                    'clock': gamestate_tree.get('display_status1').rstrip(),
                    'clock-section': gamestate_tree.get('display_status2').rstrip()
                    })
        except Exception, e:
            print e
            time.sleep(5)
            continue
        break

    return games
#-------------------------------------------------------------------------------
def main():
    for league in ['NFL', 'MLB', 'NBA', 'NHL', 'CBK', 'CFB']:
        todays_games = today(league)
        for game_info in todays_games:
            game = Game(info=game_info)
            utils.session.add(game)
            utils.session.commit()
        time.sleep(5)
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#===============================================================================
