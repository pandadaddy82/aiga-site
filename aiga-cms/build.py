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
if _n != 1:
    print('WARNING: home insights section NOT matched')

# 홈 head 보강: 제목·설명·구조화 데이터(AIGA Korea / 키워드 / 창립자)
_new_home = re.sub(r'<title>.*?</title>',
    '<title>AI거버넌스협회 (AIGA Korea) — 신뢰를 규격으로, 거버넌스를 일상으로</title>',
    _new_home, count=1, flags=re.DOTALL)
_desc = ('AI거버넌스협회(AIGA Korea)는 기업·공공기관·소상공인·1인기업을 대상으로 '
         'AI 활용 진단, 생성형 AI 리스크 관리, AI 윤리 가이드라인, AI 거버넌스 교육·컨설팅을 제공하는 비영리 협회입니다. '
         '통제가 아니라 사람의 주도권에서 출발합니다.')
_new_home = re.sub(r'<meta name="description" content=".*?">',
    '<meta name="description" content="' + _desc + '">',
    _new_home, count=1, flags=re.DOTALL)
_jsonld = ('<script type="application/ld+json">\n'
    '{\n'
    '  "@context": "https://schema.org",\n'
    '  "@type": "Organization",\n'
    '  "name": "에이아이(AI)거버넌스협회",\n'
    '  "alternateName": ["AI거버넌스협회", "AIGA", "AIGA Korea", "AI Governance Association", "AI Governance Association Korea"],\n'
    '  "url": "' + SITE + '/",\n'
    '  "logo": "' + SITE + '/aiga-logo.png",\n'
    '  "image": "' + SITE + '/og-image.png",\n'
    '  "description": "' + _desc + '",\n'
    '  "slogan": "신뢰를 규격으로, 거버넌스를 일상으로",\n'
    '  "founder": {"@type": "Person", "name": "장도균"},\n'
    '  "email": "md454243@gmail.com",\n'
    '  "telephone": "+82-10-7278-6015",\n'
    '  "address": {\n'
    '    "@type": "PostalAddress",\n'
    '    "streetAddress": "하이파크1로91번길 4-1, 2층",\n'
    '    "addressLocality": "고양시 일산서구",\n'
    '    "addressRegion": "경기도",\n'
    '    "addressCountry": "KR"\n'
    '  },\n'
    '  "knowsAbout": ["AI 거버넌스", "AI 윤리", "생성형 AI", "AI 리스크 관리", "AI 규제", "한국 AI 기본법", "책임 있는 AI", "소상공인 AI 활용"],\n'
    '  "areaServed": "KR"\n'
    '}\n'
    '</script>')
_new_home = re.sub(r'<script type="application/ld\+json">.*?</script>',
    lambda m: _jsonld, _new_home, count=1, flags=re.DOTALL)
open(_home_path, 'w', encoding='utf-8').write(_new_home)
print('home head updated')

# 소개 페이지(/about) 생성
_about_meta = ('<title>AI거버넌스협회 (AIGA Korea) 소개</title>\n'
    '<meta name="description" content="' + _desc + '">\n'
    '<link rel="canonical" href="' + SITE + '/about/">\n'
    '<meta property="og:type" content="website">\n'
    '<meta property="og:title" content="AI거버넌스협회 (AIGA Korea) 소개">\n'
    '<meta property="og:description" content="' + _desc + '">\n'
    '<meta property="og:image" content="' + SITE + '/og-image.png">\n'
    '<meta name="theme-color" content="#0A1F16">')
_about_body = ('<article class="article">\n'
    '<div class="a-meta" style="margin-bottom:10px"><a href="../index.html" style="color:var(--gold);font-weight:700">홈</a> · 소개</div>\n'
    '<span class="a-tag">협회 소개</span>\n'
    '<h1>AI거버넌스협회 (AIGA Korea) 소개</h1>\n'
    '<p class="a-lead">AI거버넌스협회(AIGA Korea)는 기업·공공기관·소상공인·1인기업을 대상으로 AI 활용 진단, 생성형 AI 리스크 관리, AI 윤리 가이드라인, AI 거버넌스 교육과 컨설팅을 제공하는 비영리 협회입니다.</p>\n'
    '<p>우리는 ‘AI를 어떻게 막을 것인가’가 아니라 ‘사람이 어떻게 주도권을 잃지 않고 AI를 쓸 것인가’에서 출발합니다. 거버넌스는 선언이 아니라 실제로 작동하는 체계일 때 의미가 있다고 믿습니다. 그래서 신뢰를 누구나 검증할 수 있는 규격으로 만들고, 그 규격을 기업과 기관, 작은 가게까지 실제로 쓸 수 있게 건네는 일을 합니다.</p>\n'
    '<h2>하는 일</h2>\n'
    '<p>국내외 규제 지형과 현장 사례를 검증된 자료로 정리하는 연구·집필, 선언이 아니라 현장에서 따라 할 수 있는 절차로 만드는 표준·윤리 가이드라인, 세 주체 누구나 자기 자리에서 실행하도록 돕는 교육·세미나·자격, 그리고 조직을 진단하고 스스로 운영할 역량을 넘기는 컨설팅·자문입니다.</p>\n'
    '<h2>누구를 위한 곳인가</h2>\n'
    '<p>대기업만을 위한 거버넌스가 아닙니다. 기업과 공공기관은 물론, 특히 자원이 적은 소상공인과 1인 창업가가 실제로 지킬 수 있는 ‘작은 조직의 AI 거버넌스’를 중요하게 다룹니다. 완벽한 규칙 백 개가 아니라 지켜지는 규칙 세 개가 더 낫다고 믿습니다.</p>\n'
    '<h2>협회 개요</h2>\n'
    '<p>\n'
    '<strong>정식 명칭</strong> 에이아이(AI)거버넌스협회<br>\n'
    '<strong>영문 명칭</strong> AI Governance Association (AIGA Korea)<br>\n'
    '<strong>약칭</strong> AIGA<br>\n'
    '<strong>대표</strong> 장도균<br>\n'
    '<strong>성격</strong> 비영리 협회<br>\n'
    '<strong>고유번호</strong> 113-82-86431<br>\n'
    '<strong>소재지</strong> 경기도 고양시 일산서구 하이파크1로91번길 4-1, 2층<br>\n'
    '<strong>전화</strong> 010-7278-6015<br>\n'
    '<strong>이메일</strong> md454243@gmail.com\n'
    '</p>\n'
    '</article>\n'
    '<div class="a-foot"><div class="a-foot-box">\n'
    '<a class="a-back" href="../index.html">← 홈으로</a>\n'
    '<a class="a-cta" href="../index.html#join">상담 문의하기</a>\n'
    '</div></div>')
os.makedirs(os.path.join(OUT, 'about'), exist_ok=True)
open(os.path.join(OUT, 'about', 'index.html'), 'w', encoding='utf-8').write(render(_about_meta, _about_body))
print('about page created')

# 정보 페이지(content/pages/*.md) 생성 (about 포함 — 위 about 출력을 덮어씀)
_PAGES = os.path.join(ROOT, 'content', 'pages')
# (본문 끝 내비는 제거 — 상단 고정 메뉴로 대체)
_page_slugs = []
if os.path.isdir(_PAGES):
    for _fn in sorted(os.listdir(_PAGES)):
        if not _fn.endswith('.md'):
            continue
        _raw = open(os.path.join(_PAGES, _fn), encoding='utf-8').read()
        _mm = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', _raw, re.DOTALL)
        _fm = yaml.safe_load(_mm.group(1)) or {}
        _bmd = _mm.group(2).strip()
        _slug = str(_fm.get('slug') or os.path.splitext(_fn)[0])
        _ptitle = str(_fm.get('title', ''))
        _pdesc = str(_fm.get('description', ''))
        _bhtml = markdown.markdown(_bmd, extensions=['extra'])
        _bhtml = re.sub(r'^<p>', '<p class="a-lead">', _bhtml, count=1)
        _pmeta = ('<title>' + esc(_ptitle) + ' — AI거버넌스협회</title>\n'
            '<meta name="description" content="' + esc(_pdesc) + '">\n'
            '<link rel="canonical" href="' + SITE + '/' + _slug + '/">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:title" content="' + esc(_ptitle) + '">\n'
            '<meta property="og:description" content="' + esc(_pdesc) + '">\n'
            '<meta property="og:image" content="' + SITE + '/og-image.png">\n'
            '<meta name="theme-color" content="#0A1F16">')
        _pcontent = ('<article class="article">\n'
            '<div class="a-meta" style="margin-bottom:10px"><a href="../index.html" style="color:var(--gold);font-weight:700">홈</a> · ' + esc(_ptitle) + '</div>\n'
            '<h1>' + esc(_ptitle) + '</h1>\n'
            + _bhtml + '\n</article>')
        os.makedirs(os.path.join(OUT, _slug), exist_ok=True)
        open(os.path.join(OUT, _slug, 'index.html'), 'w', encoding='utf-8').write(render(_pmeta, _pcontent))
        _page_slugs.append(_slug)
print('pages built:', _page_slugs)

# llms.txt 갱신 (협회 사실 + 주요 페이지 + 최근 글)
_llms = ('# AI거버넌스협회 (AIGA · AIGA Korea · AI Governance Association)\n\n'
    "> AI거버넌스협회는 'AI를 어떻게 통제할 것인가'가 아니라 '인간이 어떻게 주도권을 쥘 것인가'에서 출발하는 대한민국의 비영리 협회입니다. 신뢰를 검증 가능한 규격으로 만들고, 선언이 아니라 실제로 작동하는 AI 거버넌스를 설계·보급합니다.\n"
    '> 참고: 일본의 동명 단체(AI Governance Association)와는 구별되는, 대한민국의 협회입니다.\n\n'
    '## 핵심 정보\n'
    '- 정식 명칭: 에이아이(AI)거버넌스협회\n'
    '- 영문: AI Governance Association (AIGA Korea)\n'
    '- 약칭: AIGA\n'
    '- 슬로건: 신뢰를 규격으로, 거버넌스를 일상으로.\n'
    '- 성격: 비영리 협회 (고유번호 113-82-86431)\n'
    '- 대표: 장도균\n'
    '- 대상: 기업·기관, 소상공인·1인 창업가, 공공·정책\n'
    '- 핵심 가치(3T): Trust(신뢰) · Transfer(이전) · Together(협력)\n\n'
    '## 하는 일\n'
    '- 연구·집필: 국내외 규제 지형과 현장 사례를 검증된 자료로 정리\n'
    '- 표준·윤리 가이드라인: 선언이 아닌, 현장에서 작동하는 절차로 설계\n'
    '- 교육·세미나·자격: 세 주체 누구나 자기 자리에서 실행하도록 교육\n'
    '- 컨설팅·자문: 실체 진단 → 시스템 구축 → 역량 이전\n\n'
    '## 주요 페이지\n'
    '- 소개: ' + SITE + '/about/\n'
    '- 미션과 가치: ' + SITE + '/mission/\n'
    '- 하는 일: ' + SITE + '/services/\n'
    '- AI 거버넌스 입문: ' + SITE + '/ai-governance-guide/\n'
    '- 인사이트(칼럼): ' + SITE + '/insights/\n'
    '- 문의: ' + SITE + '/contact/\n')
if posts:
    _llms += '\n## 최근 글\n'
    for _p in posts[:8]:
        _llms += '- ' + _p['title'] + ': ' + SITE + '/insights/' + _p['slug'] + '.html\n'
_llms += ('\n## 연락처\n'
    '- 이메일: md454243@gmail.com\n'
    '- 전화: 010-7278-6015\n'
    '- 주소: 경기도 고양시 일산서구 하이파크1로91번길 4-1, 2층\n'
    '- 웹사이트: ' + SITE + '/\n')
open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write(_llms)
print('llms.txt updated')

urls = [SITE + '/'] + [SITE + '/' + _s + '/' for _s in _page_slugs] + [SITE + '/insights/'] + [SITE + '/insights/' + p['slug'] + '.html' for p in posts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += '  <url><loc>' + u + '</loc></url>\n'
sm += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)

print('build ok:', len(posts), 'posts:', [p['slug'] for p in posts])
