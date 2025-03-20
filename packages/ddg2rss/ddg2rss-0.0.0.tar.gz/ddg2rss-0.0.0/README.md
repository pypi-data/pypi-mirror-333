# DDG2RSS

[![](https://img.shields.io/pypi/v/ddg2rss)](https://pypi.org/project/ddg2rss/)
[![](https://img.shields.io/pypi/dm/ddg2rss)](https://pypi.org/project/ddg2rss/)
[![](https://gitlab.com/Thibaut_S/ddg2rss/badges/main/pipeline.svg)](https://gitlab.com/Thibaut_S/ddg2rss/-/pipelines)


Package python permettant de générer un flux rss au format xml, à partir de duckduckgo news, avec une recherche par mots clés.


Installation
---

```bash
python3 -m venv env
source env/bin/activate
pip install ddg2rss
```

Utilisation
---

```python
>>> from ddg2rss.generator import rss_file

>>> rss_file(
        link="https://public_link_of_your_output.xml", 
        keywords="Your search here",
        output_dir="/absolute/or/relative/path/to/your/output/directory"
    )
```
