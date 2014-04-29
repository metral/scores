##Scores (aka Ticker)

* Description: Homemade Sports Ticker using a Raspberry Pi & LED Sign
* Blog Post with Extended Info: https://medium.com/mikemetral/875c73a5339

## Install
 
  __Assumes__: Raspberry Pi running Raspbian release 2014-01-07
 
  * git clone https://github.com/metral/scores.git
  * cd scores/
  * git submodule init ; git submodule update
  * ./install.sh
    * (Auto starts supervisorctl from Usage section below)
  * Start ticker on boot
   * sed -i "s#exit 0#\\# Autostart ticker\nsleep 3; sudo supervisord -c /etc/supervisord.conf\n\nexit 0#g" /etc/rc.local 

## Usage (if not already running)
  
  * Start:
   * sudo supervisorctl start ticker
  * Stop
   * sudo supervisorctl stop ticker
  * Restart
   * sudo supervisorctl restart ticker

## Updates

  * cd scores/
  * git pull origin master ; git submodule foreach git pull origin master ; git pull
  * sudo supervisorctl restart ticker

