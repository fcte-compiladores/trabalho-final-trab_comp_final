import re
import sys
import os
import matplotlib.pyplot as plt

def remover_comentarios_e_strings(linhas):
    linhas_processadas = []
    padrao_str = re.compile(r'"(?:\\.|[^"\\])*"')
    for linha in linhas:
        linha = linha.split("//")[0]
        linha = re.sub(padrao_str, "", linha)
        linhas_processadas.append(linha)
    return linhas_processadas

def calcular_profundidade_aninhamento(corpo):
    max_depth = 0
    current_depth = 0
    for linha in corpo:
        if re.search(r'\b(if|for|while)\b', linha):
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        if '}' in linha:
            current_depth = max(0, current_depth - linha.count('}'))
    return max_depth

def detectar_codigo_morto(corpo):
    dead_lines = []
    dead = False
    for i, linha in enumerate(corpo):
        if dead and linha.strip() != "}":
            dead_lines.append(i+1) 
        if re.search(r'\breturn\b', linha):
            dead = True
        if '}' in linha:
            dead = False
    return dead_lines

def analisar_complexidade_arquivo(arquivo):
    with open(arquivo, encoding='utf-8') as f:
        linhas = f.readlines()
    linhas = remover_comentarios_e_strings(linhas)

    funcoes = []
    em_funcao = False
    nome_funcao = ""
    corpo_funcao = []
    chaves_abertas = 0
    linha_inicio = 0

    for i, linha in enumerate(linhas):
        fun_match = re.match(r'\s*fun\s+(\w+)\s*\(', linha)
        if fun_match and not em_funcao:
            em_funcao = True
            nome_funcao = fun_match.group(1)
            corpo_funcao = [linha]
            chaves_abertas = linha.count("{") - linha.count("}")
            linha_inicio = i+1
        elif em_funcao:
            corpo_funcao.append(linha)
            chaves_abertas += linha.count("{") - linha.count("}")
            if chaves_abertas == 0:
                funcoes.append({
                    'nome': nome_funcao,
                    'corpo': corpo_funcao,
                    'linhas': len(corpo_funcao),
                    'linha_inicio': linha_inicio
                })
                em_funcao = False

    relatorio = []
    for func in funcoes:
        cc = 1  
        for linha in func['corpo']:
            cc += len(re.findall(r'\bif\b', linha))
            cc += len(re.findall(r'\bwhile\b', linha))
            cc += len(re.findall(r'\bfor\b', linha))
            cc += len(re.findall(r'\band\b', linha))
            cc += len(re.findall(r'\bor\b', linha))
        profundidade = calcular_profundidade_aninhamento(func['corpo'])
        dead_lines = detectar_codigo_morto(func['corpo'])
        func['complexidade'] = cc
        func['aninhamento'] = profundidade
        func['dead_lines'] = dead_lines
        relatorio.append(func)
    return relatorio

def analisar_pasta(pasta):
    resultados = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.lox'):
            resultado = analisar_complexidade_arquivo(os.path.join(pasta, arquivo))
            resultados.append((arquivo, resultado))
    return resultados

def imprimir_relatorio(arquivo, relatorio, print_corpo=False):
    print(f"\nArquivo: {arquivo}")
    print(f"{'Função':<18}{'Linhas':<8}{'Compl.':<8}{'Aninh.':<8}{'Início':<7}{'Código morto':<20}")
    print("-" * 75)
    for func in relatorio:
        alerta = " <--- ALTO!" if func['complexidade'] >= 5 else ""
        dead = ", ".join(str(l) for l in func['dead_lines']) if func['dead_lines'] else "-"
        print(f"{func['nome']:<18}{func['linhas']:<8}{func['complexidade']:<8}{func['aninhamento']:<8}{func['linha_inicio']:<7}{dead:<20}{alerta}")
        if print_corpo:
            print("Corpo da função:")
            print("".join(func['corpo']))
    print()

def gerar_grafico(relatorios, nome_arquivo):
    funcoes = []
    complexidades = []
    for arquivo, relatorio in relatorios:
        for func in relatorio:
            funcoes.append(f"{func['nome']} ({arquivo})")
            complexidades.append(func['complexidade'])
    plt.figure(figsize=(8, max(3, len(funcoes) * 0.5)))
    plt.barh(funcoes, complexidades, color=['red' if c >= 5 else 'green' for c in complexidades])
    plt.xlabel('Complexidade ciclomática')
    plt.title('Complexidade por função')
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Gráfico salvo em {nome_arquivo}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python lox_cyclomatic.py <arquivo.lox> ou <pasta> [--corpo] [--grafico]")
        sys.exit(1)
    caminho = sys.argv[1]
    print_corpo = "--corpo" in sys.argv
    gerar_graf = "--grafico" in sys.argv

    if os.path.isdir(caminho):
        resultados = analisar_pasta(caminho)
        for arquivo, relatorio in resultados:
            imprimir_relatorio(arquivo, relatorio, print_corpo=print_corpo)
        if gerar_graf:
            gerar_grafico(resultados, "img/grafico_exemplo.png")
    else:
        relatorio = analisar_complexidade_arquivo(caminho)
        imprimir_relatorio(caminho, relatorio, print_corpo=print_corpo)
        if gerar_graf:
            gerar_grafico([(caminho, relatorio)], "img/grafico_exemplo.png")
