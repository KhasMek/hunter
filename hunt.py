#!/usr/bin/env python3
# THIS IS JUST A TEST OF RUNNNING IT BY IT'SELF.
#
# Downfalls
# - no file output
# - ...
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

logger = logging.getLogger()

ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
ch_formatter = logging.Formatter(' %(message)s')
ch.setFormatter(ch_formatter)

flogger = logging.FileHandler('hunter.log')
flogger.setLevel(logging.DEBUG)
# TODO: remove console shit from file messages, or modify class of console stream handler to manage that.
# https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
# flogger_formmatter = logging.Formatter('%(asctime)s [%(levelname)-5.8s]  %(message)s')
# TODO: I can look into the main scrapy logging module to see how it displays the name of the running scraper in the log
flogger_formmatter = logging.Formatter('%(asctime)s  [ %(levelname)-8.8s]  %(message)s')
flogger.setFormatter(flogger_formmatter)

# logging.basicConfig(handlers=[ch, flogger])
logger.addHandler(ch)
logger.addHandler(flogger)

logo = """

  ██░ ██  █    ██  ███▄    █ ▄▄▄█████▓▓█████  ██▀███
 ▓██░ ██▒ ██  ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
 ▒██▀▀██░▓██  ▒██░▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
 ░▓█ ░██ ▓▓█  ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄
 ░▓█▒░██▓▒▒█████▓ ▒██░   ▓██░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
  ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
  ▒ ░▒░ ░░░▒░ ░ ░ ░ ░░   ░ ▒░    ░     ░ ░  ░  ░▒ ░ ▒░
  ░  ░░ ░ ░░░ ░ ░    ░   ░ ░   ░         ░     ░░   ░
  ░  ░  ░   ░              ░             ░  ░   ░

     A website source scraper for all the things.
"""

print_settings = False
process = CrawlerProcess(get_project_settings())

# Maybe I should use `process.settings.update()` instead
process.settings.set('USER_AGENT',
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
process.settings.set('FEED_FORMAT', 'json')
process.settings.set('FEED_URI', 'results.json')
# process.settings.set('LOG_FILE', 'hunter.log')
process.settings.set('LOG_SHORT_NAMES', False)
# process.settings.set('LOG_STDOUT', True)


# This is what I'll use in the future.
# process.crawl('followall', domain='scrapinghub.com')
def main():
    print(logo)
    if print_settings:
        for k, v in process.settings.attributes.iteritems():
            print("{}: {}".format(k, v))
    process.crawl('minerhunter')
    process.start()
    print(" [-] Hunter Complete")


if __name__ == __name__:
    main()
