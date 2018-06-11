# -*- coding: utf-8 -*-
from searchengine import crawler, searcher


def test_crawler(new=False):
    c = crawler("output/search.db")
    if new:
        c.createindextables()
        pages = ['https://www.york.ac.uk/teaching/cws/wws/webpage1.html']
        c.crawl(pages)
    c.calculatepagerank()


def test_match_words():
    s = searcher("output/search.db")
    print s.getmatchrows("simple web page")


def test_full_match_words():
    s = searcher("output/search.db")
    print s.getfullmatchrows("simple web page")


if __name__ == "__main__":
    test_crawler()
