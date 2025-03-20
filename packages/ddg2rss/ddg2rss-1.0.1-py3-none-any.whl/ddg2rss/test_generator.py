from ddg2rss import generator
from os.path import isfile, join
from slugify import slugify
import os
import time


def test_rss_file():
    link = "https://duckduckgo.com"
    keywords = "DuckDuckGo News"
    output_dir = "rss-output"
    generator.rss_file(link, keywords, output_dir)
    output = join(".", output_dir, f"rss-{slugify(keywords)}.xml")
    if not isfile(join(".", output_dir, f"rss-{slugify(keywords)}.xml")):
        raise Exception
        assert False
    else:
        time.sleep(3)
        os.remove(output)
        assert True
