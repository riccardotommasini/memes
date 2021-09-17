import markdown
import re
import os

downloadables = list(filter(lambda s: s.endswith(".md") and s != "README.md", os.listdir(".")))
dl_names = [s[:-3] for s in downloadables]

main_md = open('README.md').read()
dl_mds = [open(f"{fn}").read() for fn in downloadables]

main_html, *dl_htmls = [markdown.markdown(md) for md in [main_md, *dl_mds]]

title, *dl_titles = [md.split("\n", 1)[0][2:].strip() for md in [main_md, *dl_mds]]

dl_links = [re.search(r"<a.*/a>", md).group(0) for md in dl_htmls]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@500&family=Roboto:wght@300&display=swap');
body {
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Roboto', sans-serif;
}
h1 {
    font-family: 'Roboto Slab', serif;
    font-size: xxx-large;
}
.dl {
    padding: 10;
    margin: 10;
    background-color: aliceblue;
    border-radius: 15px;
    cursor: pointer;
    text-align: left;
}
.page {
    width: 700px;
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: justify;
}
.page p, ol {
    margin-block-start: 0.3em;
    margin-block-end: 0.3em;

}

#dls {
    display: flex;
    justify-content: space-evenly;
    margin-top: 10px;
    margin-bottom: 30px;
}

a h2 {
    text-decoration: none;
}
"""

JS = """
function navTo(s) {
  window.location.href = s + ".html";
}
"""

def dl_button(i):
    return f"<div class=\"dl\" onclick=\"navTo('{dl_names[i]}')\"><h2>{dl_titles[i]}</h2>{dl_links[i]}</div>"

MAIN_HTML = f"""
<HTML>
    <HEAD>
        <TITLE>{title}</TITLE>
        <style>
        {CSS}
        </style>
        <script>
        {JS}
        </script>
    </HEAD>
    <BODY>
        <div class="page">
            {main_html}
            <div id="dls">
                {"".join(dl_button(i) for i in range(len(downloadables)))}
            </div>
        </div>
    </BODY>
</HTML>
"""
PAGE_HTMLS = [f"""
<HTML>
    <HEAD>
        <TITLE>{dl_titles[i]}</TITLE>
        <style>
        {CSS}
        </style>
    </HEAD>
    <BODY>
        <div class="page">
        <a href="index.html"><- back</a>
            {dl_htmls[i]}
        </div>
    </BODY>
</HTML>
""" for i in range(len(downloadables))]

with open('index.html', 'w', encoding='utf8') as f:
    f.write(MAIN_HTML)

for i in range(len(downloadables)):
    with open(f'{dl_names[i]}.html', 'w', encoding='utf8') as f:
        f.write(PAGE_HTMLS[i])