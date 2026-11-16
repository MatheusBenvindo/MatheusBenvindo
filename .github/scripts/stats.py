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
    ano = datetime.date.today().year
    try:
        commits = api(f'/search/commits?q=author:{USER}+committer-date:>={ano}-01-01&per_page=1').get('total_count', 0)
    except Exception:
        commits = None
    return {
        'repos': len(proprios), 'estrelas': sum(r['stargazers_count'] for r in proprios), 'seguidores': u.get('followers', 0),
        'commits': commits, 'ano': ano, 'desde': (u.get('created_at') or '')[:4], 'langs': sorted(langs.items(), key=lambda x: -x[1])[:7],
    }


def tema(dark):
    return {'ink': '#E8EEF8' if dark else '#14213D', 'sub': '#9FB2CF' if dark else '#5B6B82', 'tit': '#5BB8F0' if dark else '#164194',
            'acc': '#E84910', 'linha': '#2A3A5C' if dark else '#D5DCE8', 'fundo': 'none'}


def card_stats(d, dark):
    t = tema(dark)
    itens = [('Repositórios públicos', d['repos']), (f'Commits em {d["ano"]}', d['commits'] if d['commits'] is not None else '–'),
             ('Estrelas recebidas', d['estrelas']), ('Seguidores', d['seguidores'])]
    linhas = ''.join(f'<g transform="translate(24,{70 + i * 34})"><rect width="6" height="20" rx="3" y="-15" fill="{t["acc"] if i == 0 else t["tit"]}"/>'
                     f'<text x="18" fill="{t["sub"]}" font-size="14">{k}</text><text x="372" text-anchor="end" fill="{t["ink"]}" font-size="16" font-weight="700">{v}</text></g>'
                     for i, (k, v) in enumerate(itens))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="210" viewBox="0 0 400 210" font-family="Segoe UI, Ubuntu, sans-serif">'
            f'<rect x=".5" y=".5" width="399" height="209" rx="10" fill="none" stroke="{t["linha"]}"/>'
            f'<text x="24" y="36" fill="{t["tit"]}" font-size="17" font-weight="700">Atividade no GitHub</text>'
            f'<text x="376" y="36" text-anchor="end" fill="{t["sub"]}" font-size="12">desde {d["desde"]}</text>{linhas}</svg>')


def card_langs(d, dark):
    t = tema(dark)
    tot = sum(v for _, v in d['langs']) or 1
    x, barra = 24, ''
    for k, v in d['langs']:
        w = 352 * v / tot
        barra += f'<rect x="{x:.1f}" y="52" width="{max(w, 1.5):.1f}" height="10" fill="{CORES.get(k, "#8E8E93")}"/>'
        x += w
    leg = ''
    for i, (k, v) in enumerate(d['langs']):
        cx, cy = 24 + (i % 2) * 180, 92 + (i // 2) * 26
        leg += (f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{CORES.get(k, "#8E8E93")}"/>'
                f'<text x="{cx + 16}" y="{cy}" fill="{t["ink"]}" font-size="13">{k} <tspan fill="{t["sub"]}">{v / tot * 100:.1f}%</tspan></text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="210" viewBox="0 0 400 210" font-family="Segoe UI, Ubuntu, sans-serif">'
            f'<rect x=".5" y=".5" width="399" height="209" rx="10" fill="none" stroke="{t["linha"]}"/>'
            f'<text x="24" y="36" fill="{t["tit"]}" font-size="17" font-weight="700">Linguagens mais usadas</text>'
            f'<clipPath id="c"><rect x="24" y="52" width="352" height="10" rx="5"/></clipPath><g clip-path="url(#c)">{barra}</g>{leg}</svg>')


if __name__ == '__main__':
    d = coletar()
    os.makedirs(OUT, exist_ok=True)
    for dark in (False, True):
        s = 'dark' if dark else 'light'
        open(os.path.join(OUT, f'stats-{s}.svg'), 'w', encoding='utf-8').write(card_stats(d, dark))
        open(os.path.join(OUT, f'langs-{s}.svg'), 'w', encoding='utf-8').write(card_langs(d, dark))
    print(json.dumps(d, ensure_ascii=False))
