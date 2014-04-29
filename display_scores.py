#===============================================================================
import utils
import os
import time
from led_sign.client import SignClient
#-------------------------------------------------------------------------------
def get_game_text(game):
    lines = []

    if "In-Progress" in game.status or "Final" in game.status:
        lines = [
                "%s:%s %s:%s" % (game.away, game.away_score, \
                        game.home, game.home_score),
                ]
        if "In-Progress" in game.status:
            lines += ["%s %s (%s)" % \
                    (game.clock, game.clock_section, game.league)]
        else:
            lines += ["%s (%s)" % (game.clock, game.league)]
    elif "Pre-Game" in game.status:
        lines = [
                "%s v. %s" % (game.away, game.home),
                "%s (%s)" % (game.start, game.league)
                ]
    elif "Postponed" in game.status:
        if game.home_score and game.away_score:
            lines = [
                    "%s:%s %s:%s" % (game.away, game.away_score, \
                            game.home, game.home_score),
                    "%s (%s)" % (game.clock, game.league)
                    ]
        else:
            lines = [
                    "%s v. %s" % (game.away, game.home),
                    "%s (%s)" % (game.clock, game.league)
                    ]
    elif "Suspended" in game.status:
        if game.home_score and game.away_score:
            lines = [
                    "%s:%s %s:%s" % (game.away, game.away_score, \
                            game.home, game.home_score),
                    "%s (%s)" % (game.clock_section, game.league)
                    ]
        else:
            lines = [
                    "%s v. %s" % (game.away, game.home),
                    "%s (%s)" % (game.clock_section, game.league)
                    ]
    return lines
#-------------------------------------------------------------------------------
def main():
    session = utils.session
    all_records = session.query(utils.Game).all()

    # New client to write to led sign
    pwd = os.path.dirname(os.path.realpath(__file__))
    led_sign_path = '/'.join([pwd, 'led_sign']) 
    glyphs_path = '/'.join([led_sign_path, 'glyphs'])

    sign_client = SignClient(glyphs_path, led_sign_path)

    for game in all_records:
        lines = get_game_text(game)
        sign_client.send_text_to_sign(lines)
        time.sleep(6)
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#===============================================================================
