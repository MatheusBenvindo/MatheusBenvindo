"""Gera os cartões de estatísticas do perfil (SVG claro e escuro) com a API do GitHub.
Roda na GitHub Action diária; não depende de serviços de terceiros."""
import json, os, urllib.request, datetime

USER = os.environ.get('GH_USER', 'MatheusBenvindo')
TOKEN = os.environ.get('GITHUB_TOKEN', '')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
IGNORAR = {'Jupyter Notebook'}
CORES = {'Python': '#3572A5', 'JavaScript': '#F1E05A', 'HTML': '#E34C26', 'CSS': '#563D7C', 'TypeScript': '#3178C6', 'Java': '#B07219',
         'C#': '#178600', 'PHP': '#4F5D95', 'Shell': '#89E051', 'TSQL': '#E38C00', 'PLpgSQL': '#336790', 'C': '#555555', 'C++': '#F34B7D',
         'Dart': '#00B4AB', 'Kotlin': '#A97BFF', 'Go': '#00ADD8', 'Ruby': '#701516', 'Vue': '#41B883', 'SCSS': '#C6538C', 'Dockerfile': '#384D54'}


def api(url):
    req = urllib.request.Request(url if url.startswith('http') else 'https://api.github.com' + url,
                                 headers={'Accept': 'application/vnd.github+json', **({'Authorization': f'Bearer {TOKEN}'} if TOKEN else {})})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def coletar():
    u = api(f'/users/{USER}')
    repos, page = [], 1
    while True:
        lote = api(f'/users/{USER}/repos?per_page=100&page={page}&type=owner')
        repos += lote
        if len(lote) < 100: break
        page += 1
    proprios = [r for r in repos if not r['fork']]
    langs = {}
    for r in proprios:
        try:
            for k, v in api(r['languages_url']).items():
                if k not in IGNORAR: langs[k] = langs.get(k, 0) + v
        except Exception:
            pass
    hoje = datetime.date.today()
    meses = []
    for k in range(11, -1, -1):
        ano, mes = hoje.year, hoje.month - k
        while mes <= 0:
            ano, mes = ano - 1, mes + 12
        ini = datetime.date(ano, mes, 1)
        fim = (datetime.date(ano + (mes == 12), mes % 12 + 1, 1) - datetime.timedelta(days=1))
        try:
            n = api(f'/search/commits?q=author:{USER}+author-date:{ini}..{fim}&per_page=1').get('total_count', 0)
        except Exception:
            n = 0
        meses.append([f'{ano}-{mes:02d}', n])
    return {'repos': len(proprios), 'meses': meses, 'langs': sorted(langs.items(), key=lambda x: -x[1])[:6]}


FONTE = "'Segoe UI', Inter, 'Helvetica Neue', Arial, sans-serif"
NOMES_MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']


def moldura(dark, titulo, sub):
    fundo = '#112349' if dark else '#0E2A5E'
    borda = ' stroke="#2A4478"' if dark else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="230" viewBox="0 0 400 230" font-family="{FONTE}">'
            f'<rect x=".5" y=".5" width="399" height="229" rx="12" fill="{fundo}"{borda}/>'
            f'<text x="24" y="42" fill="#FFFFFF" font-size="18" font-weight="700">{titulo}</text>'
            f'<text x="24" y="64" fill="#A9C8F5" font-size="13">{sub}</text>')


def card_stats(d, dark):
    """Commits por mês nos últimos 12 meses. O mês atual fica em laranja."""
    meses = d['meses']
    total = sum(n for _, n in meses)
    maior = max([n for _, n in meses] + [1])
    topo, base, bw, gap = 96, 196, 22, 8
    barras = ''
    for i, (m, n) in enumerate(meses):
        x = 24 + i * (bw + gap)
        h = 0 if n == 0 else max(3, (base - topo) * n / maior)
        atual = i == len(meses) - 1
        cor = '#E84910' if atual else '#6F9FE6'
        barras += f'<rect x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="{cor}"/>'
        if n == maior or atual:
            barras += f'<text x="{x + bw / 2}" y="{base - h - 6:.1f}" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">{n}</text>'
        barras += f'<text x="{x + bw / 2}" y="214" text-anchor="middle" fill="#A9C8F5" font-size="10.5">{NOMES_MES[int(m[5:]) - 1]}</text>'
    barras += f'<line x1="24" y1="{base + .5}" x2="376" y2="{base + .5}" stroke="#FFFFFF" stroke-opacity=".2"/>'
    return moldura(dark, 'Commits por mês', f'{total} nos últimos 12 meses, em {d["repos"]} repositórios públicos') + barras + '</svg>'


def card_langs(d, dark):
    tot = sum(v for _, v in d['langs']) or 1
    x, barra = 24, ''
    for k, v in d['langs']:
        w = 352 * v / tot
        barra += f'<rect x="{x:.1f}" y="88" width="{max(w, 1.5):.1f}" height="8" fill="{CORES.get(k, "#8E8E93")}"/>'
        x += w
    leg = ''
    for i, (k, v) in enumerate(d['langs']):
        cx, cy = 24 + (i % 2) * 180, 132 + (i // 2) * 28
        leg += (f'<circle cx="{cx + 5}" cy="{cy - 4}" r="4.5" fill="{CORES.get(k, "#8E8E93")}"/>'
                f'<text x="{cx + 16}" y="{cy}" fill="#FFFFFF" font-size="13.5">{k} <tspan fill="#A9C8F5">{v / tot * 100:.1f}%</tspan></text>')
    return (moldura(dark, 'Linguagens mais usadas', 'por volume de código nos repositórios')
            + f'<clipPath id="c"><rect x="24" y="88" width="352" height="8" rx="4"/></clipPath><g clip-path="url(#c)">{barra}</g>{leg}</svg>')


if __name__ == '__main__':
    d = json.load(open(os.environ['STATS_JSON'])) if os.environ.get('STATS_JSON') else coletar()
    os.makedirs(OUT, exist_ok=True)
    for dark in (False, True):
        s = 'dark' if dark else 'light'
        open(os.path.join(OUT, f'stats-{s}.svg'), 'w', encoding='utf-8').write(card_stats(d, dark))
        open(os.path.join(OUT, f'langs-{s}.svg'), 'w', encoding='utf-8').write(card_langs(d, dark))
    print(json.dumps(d, ensure_ascii=False))
