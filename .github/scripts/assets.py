"""Gera as imagens fixas do perfil (cabeçalho e cartões de assunto), em versão clara e escura.

Uso: python .github/scripts/assets.py
Os textos ficam aqui; para mudar algo no cabeçalho ou nos cartões, edite e rode de novo.
As cores seguem o portfólio (azul #164194, laranja #E84910)."""
import glob
import hashlib
import os
import re
from html import escape

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
FONTE = "'Segoe UI', Inter, 'Helvetica Neue', Arial, sans-serif"

TEMAS = {
    'light': {'fundo': '#FFFFFF', 'borda': '#D8DEE6', 'ink': '#0B2545', 'corpo': '#3D4A5C', 'sub': '#6C757D',
              'azul': '#164194', 'laranja': '#E84910', 'laranja_txt': '#B5360B', 'linha': '#E6EAF0'},
    'dark': {'fundo': '#0D1117', 'borda': '#30363D', 'ink': '#E6EDF3', 'corpo': '#C9D1D9', 'sub': '#8B949E',
             'azul': '#6CA6F0', 'laranja': '#E84910', 'laranja_txt': '#FFAD8E', 'linha': '#21262D'},
}

HERO = {
    'pt': {
        'papel': 'Instrutor de Tecnologia e Desenvolvimento de Sistemas',
        'linhas': [('BI', 'Power BI, DAX, Power Query'), ('Bancos', 'SQL, modelagem relacional'),
                   ('Análise', 'Python, Pandas, scikit-learn'), ('Automação', 'Python, Power Automate')],
        'desc': 'Matheus Ribeiro, Instrutor de Tecnologia e Desenvolvimento de Sistemas.',
    },
    'en': {
        'papel': 'Technology and Systems Development Instructor',
        'linhas': [('BI', 'Power BI, DAX, Power Query'), ('Databases', 'SQL, relational modeling'),
                   ('Analysis', 'Python, Pandas, scikit-learn'), ('Automation', 'Python, Power Automate')],
        'desc': 'Matheus Ribeiro, Technology and Systems Development Instructor.',
    },
}

# slug: (título pt, título en, quantidade, tópicos pt, tópicos en)
TILES = {
    'banco-de-dados': ('Banco de dados', 'Databases', 8,
                       ['Modelagem lógica', 'SQL: consultas e restrições', 'DQL avançado e ETL'],
                       ['Logical modeling', 'SQL: queries and constraints', 'Advanced DQL and ETL']),
    'python-e-ia': ('Python e IA', 'Python & AI', 2,
                    ['Fundamentos e automação', 'Análise de dados', 'Machine learning'],
                    ['Fundamentals and automation', 'Data analysis', 'Machine learning']),
    'desenvolvimento-web': ('Desenvolvimento web', 'Web development', 3,
                            ['Django e CRUD', 'Back-end em C# e .NET', 'Diagnóstico de erros'],
                            ['Django and CRUD', 'C# and .NET back end', 'Debugging']),
    'testes-e-qualidade': ('Testes e qualidade', 'Testing & quality', 3,
                           ['Testes de sistemas', 'pytest e relatórios', 'Testes de integração'],
                           ['System testing', 'pytest and reports', 'Integration tests']),
    'engenharia-e-akcit': ('Engenharia e AKCIT', 'Engineering & AKCIT', 4,
                           ['Requisitos', 'Arquitetura e diagramas', 'Monitoramento de APIs'],
                           ['Requirements', 'Architecture and diagrams', 'API monitoring']),
    'projetos': ('Projetos', 'Projects', 1,
                 ['BankFlow: filas e atendimento', 'Demonstração pública'],
                 ['BankFlow: queue management', 'Public demo']),
}


def t(x, y, txt, cor, tam, peso=400, extra=''):
    return (f'<text x="{x}" y="{y}" fill="{cor}" font-family="{FONTE}" font-size="{tam}" '
            f'font-weight="{peso}"{extra}>{escape(txt)}</text>')


CHIPS = ['Power BI', 'SQL', 'Python', 'DAX', 'ETL']
BARRAS = [38, 54, 46, 70, 62, 88, 80, 112, 104, 136]  # só decoração: uma série crescente


def hero(lang, tema):
    h = HERO[lang]
    w, a = 1200, 360
    escuro = tema == 'dark'
    g1, g2 = ('#0A1A3A', '#123A86') if escuro else ('#0B2350', '#164194')
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{a}" viewBox="0 0 {w} {a}" role="img" aria-labelledby="t d">',
         f'<title id="t">Matheus Ribeiro</title><desc id="d">{escape(h["desc"])}</desc>',
         '<defs>'
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>'
         '<radialGradient id="gl" cx="1" cy="1" r=".7"><stop stop-color="#E84910" stop-opacity=".28"/><stop offset="1" stop-color="#E84910" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="gl2" cx="0" cy="0" r=".6"><stop stop-color="#5BB8F0" stop-opacity=".18"/><stop offset="1" stop-color="#5BB8F0" stop-opacity="0"/></radialGradient>'
         '</defs>',
         '<style>.b{transform-box:fill-box;transform-origin:50% 100%;animation:up .8s cubic-bezier(.2,.8,.2,1) both}'
         '.l{stroke-dasharray:700;animation:ln 1.4s ease-out .6s both}'
         '@keyframes up{from{transform:scaleY(0)}to{transform:scaleY(1)}}@keyframes ln{from{stroke-dashoffset:700}to{stroke-dashoffset:0}}'
         '@media (prefers-reduced-motion: reduce){.b,.l{animation:none}}</style>',
         f'<rect width="{w}" height="{a}" rx="20" fill="url(#bg)"/>',
         f'<rect width="{w}" height="{a}" rx="20" fill="url(#gl)"/><rect width="{w}" height="{a}" rx="20" fill="url(#gl2)"/>',
         '<rect x="56" y="98" width="40" height="5" rx="2.5" fill="#E84910"/>',
         t(54, 168, 'Matheus Ribeiro', '#FFFFFF', 54, 700, ' letter-spacing="-1"'),
         t(56, 208, h['papel'], '#8EC5FF', 21, 600)]
    x = 56
    for c in CHIPS:
        cw = len(c) * 8.6 + 30
        p.append(f'<rect x="{x}" y="240" width="{cw:.0f}" height="32" rx="16" fill="#FFFFFF" fill-opacity=".08" stroke="#FFFFFF" stroke-opacity=".22"/>')
        p.append(t(x + cw / 2, 261, c, '#FFFFFF', 14, 600, ' text-anchor="middle"'))
        x += cw + 10
    # painel com gráfico decorativo
    px, py, pw, ph = 760, 56, 384, 248
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="#FFFFFF" fill-opacity=".06" stroke="#FFFFFF" stroke-opacity=".14"/>')
    for i in range(3):
        y = py + 70 + i * 50
        p.append(f'<line x1="{px + 24}" y1="{y}" x2="{px + pw - 24}" y2="{y}" stroke="#FFFFFF" stroke-opacity=".08" stroke-dasharray="4 6"/>')
    base = py + ph - 30
    bw, gap = 22, 12
    x0 = px + 28
    pts = []
    for i, v in enumerate(BARRAS):
        bx = x0 + i * (bw + gap)
        cor, op = ('#E84910', 1) if i == len(BARRAS) - 1 else ('#5BB8F0', .35 + .05 * i)
        p.append(f'<rect class="b" style="animation-delay:{i * .06:.2f}s" x="{bx}" y="{base - v}" width="{bw}" height="{v}" rx="6" fill="{cor}" fill-opacity="{op:.2f}"/>')
        pts.append(f'{bx + bw / 2:.0f},{base - v - 14}')
    p.append(f'<polyline class="l" points="{" ".join(pts)}" fill="none" stroke="#FFFFFF" stroke-opacity=".7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    lx, ly = pts[-1].split(',')
    p.append(f'<circle cx="{lx}" cy="{ly}" r="5" fill="#FFFFFF"/><circle cx="{lx}" cy="{ly}" r="10" fill="#FFFFFF" fill-opacity=".18"/>')
    p.append(f'<line x1="{px + 24}" y1="{base + .5}" x2="{px + pw - 24}" y2="{base + .5}" stroke="#FFFFFF" stroke-opacity=".25"/>')
    p.append('</svg>')
    return '\n'.join(p)


def tile(slug, lang, tema):
    tpt, ten, n, top_pt, top_en = TILES[slug]
    titulo, topicos = (tpt, top_pt) if lang == 'pt' else (ten, top_en)
    qtd = (f'{n} repositório' + ('s' if n != 1 else '')) if lang == 'pt' else (f'{n} repositor' + ('ies' if n != 1 else 'y'))
    g1, g2, borda = ('#163266', '#0E2148', '#5BB8F0') if tema == 'dark' else ('#164194', '#0B2350', '#164194')
    w, a = 360, 210
    gid = f'g{slug.replace("-", "")}'
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{a}" viewBox="0 0 {w} {a}" role="img" aria-label="{escape(titulo)}: {qtd}">',
         f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>'
         f'<radialGradient id="{gid}r" cx="1" cy="0" r=".8"><stop stop-color="#E84910" stop-opacity=".22"/><stop offset="1" stop-color="#E84910" stop-opacity="0"/></radialGradient></defs>',
         f'<rect x=".5" y=".5" width="{w - 1}" height="{a - 1}" rx="14" fill="url(#{gid})" stroke="{borda}" stroke-opacity=".35"/>',
         f'<rect x=".5" y=".5" width="{w - 1}" height="{a - 1}" rx="14" fill="url(#{gid}r)"/>',
         t(w - 22, a - 18, str(n), '#FFFFFF', 84, 800, ' text-anchor="end" fill-opacity=".10"'),
         '<rect x="24" y="26" width="22" height="4" rx="2" fill="#E84910"/>',
         t(24, 64, titulo, '#FFFFFF', 24, 700),
         t(24, 90, qtd, '#FFB08F', 15, 600),
         f'<line x1="24" y1="108" x2="{w - 24}" y2="108" stroke="#FFFFFF" stroke-opacity=".14"/>']
    for i, tp in enumerate(topicos):
        y = 138 + i * 25
        p.append(f'<circle cx="28" cy="{y - 5}" r="3" fill="#E84910"/>')
        p.append(t(40, y, tp, '#D3DEEF', 16))
    p.append('</svg>')
    return '\n'.join(p)


def salvar(nome, conteudo, renomes):
    """Salva com um hash do conteúdo no nome (ex.: hero-pt-dark-1a2b3c4d.svg).
    Assim cada versão tem um endereço novo e o cache do GitHub não mostra imagem antiga."""
    h = hashlib.sha1(conteudo.encode('utf-8')).hexdigest()[:8]
    for velho in glob.glob(os.path.join(OUT, f'{nome}-' + '[0-9a-f]' * 8 + '.svg')) + glob.glob(os.path.join(OUT, f'{nome}.svg')):
        os.remove(velho)
    open(os.path.join(OUT, f'{nome}-{h}.svg'), 'w', encoding='utf-8').write(conteudo)
    renomes[nome] = f'{nome}-{h}.svg'


def atualizar_readmes(renomes):
    raiz = os.path.join(os.path.dirname(__file__), '..', '..')
    for arq in ('README.md', 'README.en.md'):
        cam = os.path.join(raiz, arq)
        txt = open(cam, encoding='utf-8').read()
        for nome, novo in renomes.items():
            txt = re.sub(rf'assets/{re.escape(nome)}(-[0-9a-f]{{8}})?\.svg(\?v=\d+)?', f'assets/{novo}', txt)
        txt = re.sub(r'(assets/[\w./-]+\.svg)\?v=\d+', r'\1', txt)
        open(cam, 'w', encoding='utf-8').write(txt)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    renomes = {}
    for lang in ('pt', 'en'):
        for tema in ('light', 'dark'):
            salvar(f'hero-{lang}-{tema}', hero(lang, tema), renomes)
            for slug in TILES:
                salvar(f'tile-{lang}-{slug}-{tema}', tile(slug, lang, tema), renomes)
    atualizar_readmes(renomes)
    print('ok')
