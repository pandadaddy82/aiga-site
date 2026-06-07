import os, re, shutil
import yaml
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'output')
STATIC = os.path.join(ROOT, 'static')
CONTENT = os.path.join(ROOT, 'content', 'insights')
SITE = 'https://aigakorea.netlify.app'

page = open(os.path.join(ROOT, 'templates', 'page.html'), encoding='utf-8').read()

if os.path.exists(OUT):
    shutil.rmtree(OUT)
shutil.copytree(STATIC, OUT)
os.makedirs(os.path.join(OUT, 'insights'), exist_ok=True)


def render(meta_html, content_html):
    return page.replace('<!--META-->', meta_html).replace('<!--CONTENT-->', content_html)


def esc(s):
    s = s or ''
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


posts = []
for fn in sorted(os.listdir(CONTENT)):
    if not fn.endswith('.md'):
        continue
    raw = open(os.path.join(CONTENT, fn), encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', raw, re.DOTALL)
    fm = yaml.safe_load(m.group(1)) or {}
    body_md = m.group(2).strip()
    slug = str(fm.get('slug') or os.path.splitext(fn)[0])
    title = str(fm.get('title', ''))
    cat = str(fm.get('category', '인사이트'))
    summary = str(fm.get('summary', ''))
    date = str(fm.get('date', ''))[:10]
    body_html = markdown.markdown(body_md, extensions=['extra'])
    body_html = re.sub(r'^<p>', '<p class="a-lead">', body_html, count=1)
    ym = (date[:7].replace('-', '. ') + '.') if date else ''
    meta = (
        '<title>' + esc(title) + ' \u2014 AI\uac70\ubc84\ub10c\uc2a4\ud611\ud68c</title>\n'
        '<meta name="description" content="' + esc(summary) + '">\n'
        '<link rel="canonical" href="' + SITE + '/insights/' + slug + '.html">\n'
        '<meta property="og:type" content="article">\n'
        '<meta property="og:title" content="' + esc(title) + '">\n'
        '<meta property="og:description" content="' + esc(summary) + '">\n'
        '<meta property="og:url" content="' + SITE + '/insights/' + slug + '.html">\n'
        '<meta property="og:image" content="' + SITE + '/og-image.png">\n'
        '<meta name="theme-color" content="#0A1F16">'
    )
    article = (
        '<article class="article">\n'
        '<span class="a-tag">' + esc(cat) + '</span>\n'
        '<h1>' + esc(title) + '</h1>\n'
        '<div class="a-meta">\uae00 \u00b7 \uc7a5\ub3c4\uade0 (AI\uac70\ubc84\ub10c\uc2a4\ud611\ud68c) \u00b7 ' + date + '</div>\n'
        + body_html +
        '\n<p class="a-sign">\u2014 \uc7a5\ub3c4\uade0, AI\uac70\ubc84\ub10c\uc2a4\ud611\ud68c</p>\n'
        '</article>\n'
        '<div class="a-foot"><div class="a-foot-box">\n'
        '<a class="a-back" href="./">\u2190 \uc778\uc0ac\uc774\ud2b8 \ubaa9\ub85d\uc73c\ub85c</a>\n'
        '<a class="a-cta" href="../index.html#join">\uc0c1\ub2f4 \ubb38\uc758\ud558\uae30</a>\n'
        '</div></div>'
    )
    open(os.path.join(OUT, 'insights', slug + '.html'), 'w', encoding='utf-8').write(render(meta, article))
    posts.append({'slug': slug, 'title': title, 'cat': cat, 'summary': summary, 'date': date, 'ym': ym})

posts.sort(key=lambda p: p['date'], reverse=True)

cards = ''
for p in posts:
    cards += (
        '<a class="ins-card" href="' + p['slug'] + '.html">'
        '<span class="ic-tag">' + esc(p['cat']) + '</span>'
        '<h3>' + esc(p['title']) + '</h3>'
        '<p>' + esc(p['summary']) + '</p>'
        '<span class="ic-date">' + p['ym'] + '</span>'
        '<span class="ins-more">\uc77d\uc5b4\ubcf4\uae30 \u2192</span></a>\n'
    )

list_content = (
    '<section class="page-hero"><div class="wrap">'
    '<div class="crumb"><a href="../index.html">\ud648</a> \u00b7 \uc778\uc0ac\uc774\ud2b8</div>'
    '<span class="eyebrow">\uc778\uc0ac\uc774\ud2b8</span>'
    '<h1>\uadfc\uac70 \uc704\uc5d0\uc11c \ub9d0\ud569\ub2c8\ub2e4</h1>'
    '<p>\uc2e0\ub8b0\ub294 \uc6b0\ub9ac\uac00 \ub2e4\ub8e8\ub294 \uc8fc\uc81c\uc774\uc790, \uc6b0\ub9ac \uc2a4\uc2a4\ub85c \uc9c0\ucf1c\uc57c \ud560 \uc7ac\ud654\uc785\ub2c8\ub2e4. \uac80\uc99d\ub41c \uc0ac\uc2e4 \uc704\uc5d0\uc11c \uae00\uc744 \ud55c \ud3b8\uc529 \uc313\uc544\uac11\ub2c8\ub2e4.</p>'
    '</div></section>\n'
    '<section class="sec"><div class="wrap"><div class="ins-grid">\n' + cards + '</div></div></section>'
)
list_meta = (
    '<title>\uc778\uc0ac\uc774\ud2b8 \u2014 AI\uac70\ubc84\ub10c\uc2a4\ud611\ud68c</title>\n'
    '<meta name="description" content="AI \uac70\ubc84\ub10c\uc2a4\ub97c \uac80\uc99d\ub41c \uc0ac\uc2e4\ub85c \ud480\uc5b4\ub0b4\ub294 AI\uac70\ubc84\ub10c\uc2a4\ud611\ud68c\uc758 \uae00.">\n'
    '<link rel="canonical" href="' + SITE + '/insights/">\n'
    '<meta property="og:title" content="\uc778\uc0ac\uc774\ud2b8 \u2014 AI\uac70\ubc84\ub10c\uc2a4\ud611\ud68c">\n'
    '<meta property="og:image" content="' + SITE + '/og-image.png">\n'
    '<meta name="theme-color" content="#0A1F16">'
)
open(os.path.join(OUT, 'insights', 'index.html'), 'w', encoding='utf-8').write(render(list_meta, list_content))

# 홈 메인페이지(index.html)의 인사이트 카드를 최신 글 3개로 자동 채우기
_orbits = [
    '<circle cx="75" cy="75" r="60" stroke="rgba(248,246,240,.5)" stroke-width="1"/><circle cx="75" cy="15" r="5" fill="rgba(248,246,240,.7)"/>',
    '<ellipse cx="75" cy="75" rx="60" ry="36" stroke="rgba(248,246,240,.5)" stroke-width="1"/><circle cx="135" cy="75" r="5" fill="rgba(248,246,240,.7)"/>',
    '<circle cx="75" cy="75" r="48" stroke="rgba(248,246,240,.5)" stroke-width="1"/><circle cx="75" cy="135" r="5" fill="rgba(248,246,240,.7)"/>',
]
_home_cards = ''
for _i, _p in enumerate(posts[:3]):
    _d = '' if _i == 0 else ' d' + str(_i)
    _orbit = _orbits[_i % len(_orbits)]
    _home_cards += (
        '\n      <article class="icard reveal' + _d + '">\n'
        '        <div class="ihead"><svg class="ic-orbit" viewBox="0 0 150 150" fill="none">' + _orbit + '</svg></div>\n'
        '        <div class="ibody"><span class="ic-tag">' + esc(_p['cat']) + '</span><h4>' + esc(_p['title']) + '</h4><p>' + esc(_p['summary']) + '</p>'
        '<a class="ic-read" href="insights/' + _p['slug'] + '.html" style="display:inline-block;margin-top:16px;color:var(--gold);font-weight:700;font-size:14px">\uc77d\uc5b4\ubcf4\uae30 \u2192</a></div>\n'
        '      </article>'
    )
_home_cards += '\n    '
_home_path = os.path.join(OUT, 'index.html')
_home_html = open(_home_path, encoding='utf-8').read()
_pat = re.compile(r'<div class="insights">.*?</div>\s*<div style="text-align:center;margin-top:40px">', re.DOTALL)
_repl = '<div class="insights">' + _home_cards + '</div>\n    <div style="text-align:center;margin-top:40px">'
_new_home, _n = _pat.subn(lambda m: _repl, _home_html, count=1)
if _n == 1:
    open(_home_path, 'w', encoding='utf-8').write(_new_home)
    print('home insights updated:', len(posts[:3]), 'cards')
else:
    print('WARNING: home insights section NOT matched')

urls = [SITE + '/', SITE + '/insights/'] + [SITE + '/insights/' + p['slug'] + '.html' for p in posts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += '  <url><loc>' + u + '</loc></url>\n'
sm += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)

print('build ok:', len(posts), 'posts:', [p['slug'] for p in posts])
