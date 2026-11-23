"""Gera as imagens fixas do perfil (cabeçalho e cartões de assunto), em versão clara e escura.

Uso: python .github/scripts/assets.py
Os textos ficam aqui; para mudar algo no cabeçalho ou nos cartões, edite e rode de novo.
As cores seguem o portfólio (azul #164194, laranja #E84910)."""
import os
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
        'papel': 'Dados e BI · Instrutor de tecnologia',
        'texto': ['Modelo dados, escrevo SQL e monto relatórios em Power BI.',
                  'Automatizo rotinas com Python e ensino isso em sala de aula.'],
        'linhas': [('BI', 'Power BI, DAX, Power Query'), ('Bancos', 'SQL, modelagem relacional'),
                   ('Análise', 'Python, Pandas, scikit-learn'), ('Automação', 'Python, Power Automate')],
        'desc': 'Matheus Ribeiro: dados e BI, instrutor de tecnologia.',
    },
    'en': {
        'papel': 'Data & BI · Technology instructor',
        'texto': ['I model data, write SQL and build Power BI reports.',
                  'I automate routines with Python and teach all of it in class.'],
        'linhas': [('BI', 'Power BI, DAX, Power Query'), ('Databases', 'SQL, relational modeling'),
                   ('Analysis', 'Python, Pandas, scikit-learn'), ('Automation', 'Python, Power Automate')],
        'desc': 'Matheus Ribeiro: data and BI, technology instructor.',
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


def hero(lang, tema):
    c, h = TEMAS[tema], HERO[lang]
    w, a = 1200, 330
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{a}" viewBox="0 0 {w} {a}" role="img" aria-labelledby="t d">',
         f'<title id="t">Matheus Ribeiro</title><desc id="d">{escape(h["desc"])}</desc>',
         f'<rect x=".5" y=".5" width="{w - 1}" height="{a - 1}" rx="12" fill="{c["fundo"]}" stroke="{c["borda"]}"/>',
         f'<rect x="56" y="64" width="36" height="4" rx="2" fill="{c["laranja"]}"/>',
         t(54, 132, 'Matheus Ribeiro', c['ink'], 50, 700, ' letter-spacing="-0.5"'),
         t(56, 174, h['papel'], c['azul'], 20, 600)]
    for i, linha in enumerate(h['texto']):
        p.append(t(56, 228 + i * 30, linha, c['corpo'], 19))
    x0 = 760
    p.append(f'<line x1="{x0 - 40}" y1="56" x2="{x0 - 40}" y2="{a - 56}" stroke="{c["linha"]}" stroke-width="1.5"/>')
    for i, (rot, val) in enumerate(h['linhas']):
        y = 86 + i * 56
        p.append(t(x0, y, rot, c['sub'], 15, 600))
        p.append(t(x0, y + 25, val, c['ink'], 19, 500))
    p.append('</svg>')
    return '\n'.join(p)


def tile(slug, lang, tema):
    c = TEMAS[tema]
    tpt, ten, n, top_pt, top_en = TILES[slug]
    titulo, topicos = (tpt, top_pt) if lang == 'pt' else (ten, top_en)
    qtd = (f'{n} repositório' + ('s' if n != 1 else '')) if lang == 'pt' else (f'{n} repositor' + ('ies' if n != 1 else 'y'))
    w, a = 360, 210
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{a}" viewBox="0 0 {w} {a}" role="img" aria-label="{escape(titulo)}: {qtd}">',
         f'<rect x=".5" y=".5" width="{w - 1}" height="{a - 1}" rx="10" fill="{c["fundo"]}" stroke="{c["borda"]}"/>',
         f'<rect x="24" y="24" width="20" height="3" rx="1.5" fill="{c["laranja"]}"/>',
         t(24, 62, titulo, c['ink'], 25, 700),
         t(24, 88, qtd, c['laranja_txt'], 16, 600),
         f'<line x1="24" y1="108" x2="{w - 24}" y2="108" stroke="{c["linha"]}"/>']
    for i, tp in enumerate(topicos):
        p.append(t(24, 138 + i * 26, tp, c['corpo'], 17))
    p.append('</svg>')
    return '\n'.join(p)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for lang in ('pt', 'en'):
        for tema in ('light', 'dark'):
            open(os.path.join(OUT, f'hero-{lang}-{tema}.svg'), 'w', encoding='utf-8').write(hero(lang, tema))
            for slug in TILES:
                open(os.path.join(OUT, f'tile-{lang}-{slug}-{tema}.svg'), 'w', encoding='utf-8').write(tile(slug, lang, tema))
    print('ok')
