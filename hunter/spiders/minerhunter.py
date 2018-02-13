from itertools import chain
from scrapy.spiders import Spider
from scrapy.selector import Selector
from hunter.items import HunterItem
from scrapy.http import Request
from tld import get_tld
import re
import urllib
# https://stackoverflow.com/questions/24515268/how-to-crawl-multiple-domain-with-scrapy
# https://github.com/codingo/Minesweeper/blob/master/lib/update_sources.py
# https://raw.githubusercontent.com/ZeroDot1/CoinBlockerLists/master/list.txt

# Really, this "minerhunter" Should be more of a "listhunter" thant can accept multiple inputs (maybe from base hunt[er].py) and output files based on those names


class MySpider(Spider):
    name = "minerhunter"
    f = open('targets')
    # TODO: need to add allowed domains, otherwise it'll go everywhere
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        self.logger.debug('Parse function called on %s', response.url)
        # print("ASDOFIAS;JDF;LAKSJDFASDFASDFASDF\n{}\nASDOFIAS;JDF;LAKSJDFASDFASDFASDF\nASDOFIAS;JDF;LAKSJDFASDFASDFASDF\n{}\nASDOFIAS;JDF;LAKSJDFASDFASDFASDF\n\n".format(response, get_tld(response.request.url)))
        try:
            hxs = Selector(response)
            # This is a dynamic way of replicating allowed_domains bascially. There may be a smarter way to do it.
            domain = get_tld(response.request.url)
            try:
                title = response.selector.xpath('//title/text()').extract_first()
            except AttributeError:
                title = ''

            # CODE for crypto miners
            with open("list.txt", "r") as miner_list:
                for miner_string in miner_list:
                    # test = "//*[contains(text(), '{}')]".format(miner_string.rstrip()).decode('utf-8')
                    # for python2 it's just `urllib.quote_plus()` ref: https://docs.python.org/3/library/urllib.parse.html
                    text = "//*[contains(text(), '{}')]".format(urllib.parse.quote_plus(miner_string.rstrip()))
                    href = "//*[contains(@href, '{}')]".format(urllib.parse.quote_plus(miner_string.rstrip()))
                    # This should return results, or `"//*[contains(@src, '{}')]"`
                    script = "//*[contains(script, '{}')]".format(urllib.parse.quote_plus(miner_string.rstrip()))
                    # comment = "//*[contains(comment(), '{}')]".format(miner_string.rstrip())
                    comment = "//*[contains(comment(), '{}')]".format(miner_string.rstrip())
                    # TODO: each of these should get some sort of "type" field identifier I think.
                    miner_snippets_text = hxs.xpath(text).extract()
                    miner_snippets_href = hxs.xpath(href).extract()
                    miner_snippets_script = hxs.xpath(script).extract()
                    miner_snippets_comment = hxs.xpath(comment).extract()
                    for snippet in miner_snippets_text:
                        # print(getattr(snippet, 'xpath'))
                        miner = HunterItem()
                        miner['title'] = title
                        miner['kind'] = 'text'
                        miner['domain'] = str(domain)
                        miner['url'] = response.request.url
                        miner['snippet'] = snippet
                        self.logger.warn("[*] CryptoMiner found in plain text at %s", str(miner['url']))
                        yield miner
                    for snippet in miner_snippets_href:
                        miner = HunterItem()
                        miner['title'] = title
                        miner['kind'] = 'link'
                        miner['domain'] = str(domain)
                        miner['url'] = response.request.url
                        miner['snippet'] = snippet
                        self.logger.warn("[*] CryptoMiner found a link at %s", str(miner['url']))
                        yield miner
                    for snippet in miner_snippets_script:
                        miner = HunterItem()
                        miner['title'] = title
                        miner['kind'] = 'script'
                        miner['domain'] = str(domain)
                        miner['url'] = response.request.url
                        miner['snippet'] = snippet
                        self.logger.warn("[*] CryptoMiner found in a script at %s", str(miner['url']))
                        yield miner
                    for snippet in miner_snippets_comment:
                        miner = HunterItem()
                        miner['title'] = title
                        miner['kind'] = 'comment'
                        miner['domain'] = str(domain)
                        miner['url'] = response.request.url
                        comment_cleanup = '(<!-- <)(script|href)(.*?)({})(.*?)(> -->)'.format(miner_string.rstrip())
                        comment_cleanup_regex = re.compile(comment_cleanup, re.DOTALL)
                        clean_comment = comment_cleanup_regex.findall(snippet)[0]
                        clean = ' '.join(str(i) for i in clean_comment)
                        miner['snippet'] = clean
                        self.logger.warn("[*] CryptoMiner reference found in a comment at %s", str(miner['url']))
                        yield miner

                visited_links = []
                links = hxs.xpath('//a/@href').extract()
                # link_validator = re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
                link_validator_string = "^(?:http|https):\/\/{}?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$".format(domain)
                link_validator = re.compile(link_validator_string)
                # print("\nWWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOOWOWOWOWOWO\n{}\nWWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOWOOWOWOWOWOWO\n".format(link_validator_string))

                # TODO: This should probably be a standalone function somewhere.
                for link in links:
                    if link_validator.match(link) and not link in visited_links:
                        # print("\n==============================================\n{}\n{}\n==============================================\n".format(link, link_validator_string))
                        visited_links.append(link)
                        yield Request(link, self.parse)
                    else:
                        full_url = response.urljoin(link)
                        if link_validator.match(full_url) and not full_url in visited_links:
                            # print("\n----------------------------------------------\n{}\n{}\n----------------------------------------------\n".format(full_url, link_validator_string))
                            visited_links.append(full_url)
                            yield Request(full_url, self.parse)
        except AttributeError:
            # temp fix for "AttributeError: Response content isn't text"
            self.logger.error("[!] Response content isn't text - %s", response.request.url)
