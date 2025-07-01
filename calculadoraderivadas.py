import re

def derivar_termo(termo):
    termo = termo.strip()
    
    if 'x' not in termo:
        return '0'

    match = re.match(r'([+-]?\d*)\*?x(\^(\d+))?', termo)
    if not match:
        return 'Erro: termo mal formatado'

    coef = match.group(1)
    exp = match.group(3)

    coef = int(coef) if coef not in ('', '+', '-') else int(coef + '1')
    exp = int(exp) if exp else 1

    novo_coef = coef * exp
    novo_exp = exp - 1

    if novo_exp == 0:
        return f"{novo_coef}"
    elif novo_exp == 1:
        return f"{novo_coef}*x"
    else:
        return f"{novo_coef}*x^{novo_exp}"

def derivar(expressao):
    termos = expressao.replace('-', '+-').split('+')
    derivados = [derivar_termo(t) for t in termos if t.strip()]
    return ' + '.join(derivados).replace('+-', '- ')

if __name__ == "__main__":
    print("Calculadora de Derivadas (modo matemático)")
    expressao = input("Digite uma função polinomial (ex: 3*x^2 + 2*x - 5): ")
    resultado = derivar(expressao)
    print("Derivada:", resultado)
