#===============================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import sys
import MySQLdb
import warnings 
import env_settings
from datetime import datetime
from pytz import timezone
import pytz
import dateutil.parser as dparser
#-------------------------------------------------------------------------------
warnings.filterwarnings( 
        action="ignore", 
        category=MySQLdb.Warning) 

host = env_settings.MYSQL_HOST
user = env_settings.MYSQL_USER
port = env_settings.MYSQL_PORT
password = env_settings.MYSQL_PASS
db_name = env_settings.MYSQL_DB

db_path = "mysql://%s:%s@%s:%s" % (user, password, host, port)
#-------------------------------------------------------------------------------
engine = create_engine(db_path, echo=False)
engine.execute("CREATE DATABASE IF NOT EXISTS %s" % db_name)
engine.execute("USE %s" % db_name)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
#-------------------------------------------------------------------------------
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    league = Column(String(50))
    start = Column(String(50))
    home = Column(String(50))
    away = Column(String(50))
    clock = Column(String(50))
    away_score = Column(String(50))
    home_score = Column(String(50))
    clock_section = Column(String(50))

    def __init__(self, *args, **kwargs):
        if kwargs:
            info  = kwargs.get('info')

            self.status = info['status']
            self.league = info['league'].upper()
            self.start = info['start']
            self.home = info['home'].upper()
            self.away = info['away'].upper()
            self.clock = info['clock'].upper()
            self.away_score = info['away-score']
            self.home_score = info['home-score']
            self.clock_section = info['clock-section'].upper()
#-------------------------------------------------------------------------------
Base.metadata.create_all(engine)
#-------------------------------------------------------------------------------
def localize_game_time(game_time, local_tz):
    game_tz = timezone(env_settings.GAME_TZ)

    # Get current UTC time
    current_date_format='%m/%d/%Y %H:%M:%S %Z'
    current_date_utc = datetime.now(tz=pytz.utc)

    # Convert current UTC to TZ game info is based off (Eastern)
    current_date_eastern = current_date_utc.astimezone(game_tz)

    # Tweak current Eastern time to use the hour & minute game is at
    # This is to assure we have every other part of the datetime obj correct
    game_date_eastern_str= "%s/%s/%s %s" % (
            current_date_eastern.month,
            current_date_eastern.day,
            current_date_eastern.year,
            game_time)

    game_date_eastern = game_tz.localize(dparser.parse(game_date_eastern_str))

    # Convert Eastern game time to the local TZ specified
    game_date_local = game_date_eastern.astimezone(timezone(local_tz))

    # Return hour:minute am/pm as we dont need rest of date info
    game_date_short_format = '%I:%M %p'
    game_date_local_short = game_date_local.strftime(game_date_short_format)

    return game_date_local_short
#===============================================================================
