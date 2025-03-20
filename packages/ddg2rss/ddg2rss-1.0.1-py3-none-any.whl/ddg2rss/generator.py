from duckduckgo_search import DDGS
from feedgen.feed import FeedGenerator
from slugify import slugify
import os


def rss_file(link, keywords, output_dir):

    file = f"rss-{slugify(keywords)}.xml"
    results = DDGS().news(
        keywords=f'"{keywords}"',
        region="fr-fr",
        safesearch="off",
        timelimit="w",
        max_results=20,
    )

    fg = FeedGenerator()
    fg.title(keywords)
    fg.description("Flux RSS de DuckDuckGo News, généré avec ddg2rss")
    fg.link(href=f"{link}/{file}")
    fg.language("fr")

    for result in results:
        fe = fg.add_entry()
        fe.pubDate(result["date"])
        fe.title(result["title"])
        fe.description(result["body"])
        fe.link(href=result["url"])
        fe.source(result["source"])

    output = os.path.join(output_dir, file)
    fg.rss_file(output)


if __name__ == "main":
    link = str(input("Lien racine : "))
    keywords = str(input("recherche : "))
    output_dir = str(input("output dir (absolute path): "))
    rss_file(link, keywords, output_dir)
