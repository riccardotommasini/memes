import markdown
import re

downloadables = ['kym', 'kym_spotlight', 'kym_vision']

main_md = open('README.md').read()
dl_mds = [open(f"{fn}.md").read() for fn in downloadables]

main_html, *dl_htmls = [markdown.markdown(md) for md in [main_md, *dl_mds]]

title, *dl_titles = [md.split("\n", 1)[0][2:].strip() for md in [main_md, *dl_mds]]

dl_links = [re.search(r"<a.*/a>", md).group(0) for md in dl_htmls]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@500&family=Roboto:wght@300&display=swap');
body {
    margin: 0px;
    height:100%;
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
}
.page {
    width: 700px;
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center
}

#dls {
    display: flex;
    justify-content: space-evenly;
    margin-top: 50px;
}

a h2 {
    text-decoration: none;
}
"""

JS = """
function navTo(anchor) {
  document.location = document.location.toString().split('#')[0] + '#' + anchor;
}
"""

def dl_button(i):
    return f"<div class=\"dl\" onclick=\"navTo('{downloadables[i]}')\"><h2>{dl_titles[i]}</h2>{dl_links[i]}</div>"

HTML = f"""
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
            {"".join(f'<div class="page"> <a name="{downloadables[i]}">{dl_htmls[i]}</div>' for i in range(len(downloadables)))}
    </BODY>
</HTML>
"""
with open('index.html', 'w', encoding='utf8') as f:
    f.write(HTML)