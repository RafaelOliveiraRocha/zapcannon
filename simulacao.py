"""Plano local de mensagens; usa somente a biblioteca padrão do Python."""

import argparse
import csv
import json
import sys
from pathlib import Path


def ler_contatos(arquivo):
    """Valida todo o CSV antes de apresentar qualquer ação planejada."""
    contatos = []
    with Path(arquivo).open(encoding="utf-8-sig", newline="") as entrada:
        leitor = csv.DictReader(entrada, strict=True)
        campos = leitor.fieldnames
        if not campos:
            raise ValueError("CSV vazio: informe os cabeçalhos Nome e Número.")
        ausentes = [campo for campo in ("Nome", "Número") if campo not in campos]
        if ausentes:
            raise ValueError("Colunas obrigatórias ausentes: " + ", ".join(ausentes))
        if len(campos) != len(set(campos)):
            raise ValueError("O CSV contém cabeçalhos repetidos.")
        for posicao, linha in enumerate(leitor, start=1):
            if None in linha or any(valor is None for valor in linha.values()):
                raise ValueError(f"Registro {posicao}: quantidade de campos diferente do cabeçalho.")
            numero = linha["Número"]
            if not numero or any(digito not in "0123456789" for digito in numero):
                raise ValueError(f"Registro {posicao}: Número deve conter somente dígitos, sem espaços.")
            contatos.append((linha["Nome"], numero))
    return contatos


def main(argumentos=None):
    parser = argparse.ArgumentParser(
        description="Simulação local do ZapCannon, sem envio ou acesso a serviços."
    )
    parser.add_argument("--simular", action="store_true", required=True,
                        help="Seleciona explicitamente a demonstração sem efeitos externos.")
    parser.add_argument("--csv", required=True, help="CSV UTF-8 com Nome e Número.")
    parser.add_argument("--mensagem", required=True, help="Texto fictício da demonstração.")
    args = parser.parse_args(argumentos)
    if not args.mensagem.strip():
        print("Erro de entrada: a mensagem não pode estar vazia.", file=sys.stderr)
        return 2
    try:
        contatos = ler_contatos(args.csv)
    except (OSError, UnicodeError, csv.Error, ValueError) as erro:
        if isinstance(erro, ValueError) and not isinstance(erro, UnicodeError):
            detalhe = str(erro)
        elif isinstance(erro, UnicodeError):
            detalhe = "O CSV deve usar UTF-8."
        elif isinstance(erro, csv.Error):
            detalhe = "Não foi possível interpretar a estrutura do CSV."
        else:
            detalhe = "Não foi possível ler o arquivo CSV."
        print("Erro de entrada: " + detalhe, file=sys.stderr)
        return 2

    print("SIMULAÇÃO LOCAL — dados fornecidos não serão enviados.")
    print(f"Entrada validada: {len(contatos)} registros.")
    for posicao, (nome, numero) in enumerate(contatos, start=1):
        texto = f"{nome}\n{args.mensagem}" if nome else args.mensagem
        acao = json.dumps({"Número": numero, "texto": texto}, ensure_ascii=False)
        print(f"[{posicao}] PLANEJADO, NÃO ENVIADO: {acao}")
    print(f"Resumo: {len(contatos)} ações planejadas; 0 envios executados.")
    print("Nenhum navegador, conexão ou arquivo de resultado foi criado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
