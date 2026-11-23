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


NAVY = {'light': '#0E2A5E', 'dark': '#112349'}
FERRAMENTAS = {'pt': 'Power BI, SQL, Python, DAX e ETL', 'en': 'Power BI, SQL, Python, DAX and ETL'}


def hero(lang, tema):
    h = HERO[lang]
    w, a = 1200, 240
    borda = '' if tema == 'light' else ' stroke="#2A4478"'
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{a}" viewBox="0 0 {w} {a}" role="img" aria-labelledby="t d">',
         f'<title id="t">Matheus Ribeiro</title><desc id="d">{escape(h["desc"])}</desc>',
         f'<rect x=".5" y=".5" width="{w - 1}" height="{a - 1}" rx="16" fill="{NAVY[tema]}"{borda}/>',
         t(56, 112, 'Matheus Ribeiro', '#FFFFFF', 60, 700, ' letter-spacing="-1.2"'),
         t(58, 156, h['papel'], '#A9C8F5', 25, 500),
         t(58, 196, FERRAMENTAS[lang], '#C9D6EA', 19),
         '</svg>']
    return '\n'.join(p)


def tile(slug, lang, tema):
    tpt, ten, n, top_pt, top_en = TILES[slug]
    titulo, topicos = (tpt, top_pt) if lang == 'pt' else (ten, top_en)
    qtd = (f'{n} repositório' + ('s' if n != 1 else '')) if lang == 'pt' else (f'{n} repositor' + ('ies' if n != 1 else 'y'))
    w, a = 360, 200
    borda = '' if tema == 'light' else ' stroke="#2A4478"'
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{a}" viewBox="0 0 {w} {a}" role="img" aria-label="{escape(titulo)}: {qtd}">',
         f'<rect x=".5" y=".5" width="{w - 1}" height="{a - 1}" rx="12" fill="{NAVY[tema]}"{borda}/>',
         t(26, 52, titulo, '#FFFFFF', 24, 700),
         t(26, 80, qtd, '#A9C8F5', 15, 500)]
    for i, tp in enumerate(topicos):
        p.append(t(26, 124 + i * 26, tp, '#D3DEEF', 17))
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
