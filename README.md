# ZapCannon

Preparar a mesma mensagem para uma lista de contatos exige repetir a seleção dos destinatários e a personalização do texto. O ZapCannon nasceu de uma necessidade operacional para automatizar essa preparação, mantendo os nomes e as mensagens organizados a partir de um CSV.

O projeto evoluiu de um script Python para uma interface web local com Flask, combinando uma aplicação prática com a trajetória de aprendizado em desenvolvimento e engenharia de software. A demonstração no terminal reproduz a preparação com dados inteiramente fictícios.

## Experimente a demonstração

Na raiz do projeto, com **Python 3**, sem instalar dependências:

```bash
python3 -S -B zapcannon.py --simular \
  --csv examples/contatos-sinteticos.csv \
  --mensagem "Olá! Esta é uma demonstração fictícia."
```

O fluxo é **leitura e validação do CSV → personalização pelo nome → textos preparados no terminal**. Quando `Nome` está preenchido, o texto recebe o nome, uma quebra de linha e a mensagem. Quando está vazio, recebe somente a mensagem.

A simulação usa a biblioteca padrão, antes dos imports de Flask, pandas e Selenium. Ela mantém os destinos como texto e mostra ações planejadas, sem links de envio, rede, navegador ou controles de teclado/mouse. Para consultar as opções: `python3 -S -B zapcannon.py --help`.

Prévia fiel de [examples/saida-simulacao.txt](examples/saida-simulacao.txt). Os três destinos são fictícios; `\n` representa uma quebra de linha:

| Destino fictício | Texto planejado |
|---|---|
| `000000000001` | `Pessoa Fictícia A\nOlá! Esta é uma demonstração fictícia.` |
| `000000000002` | `Pessoa Fictícia B\nOlá! Esta é uma demonstração fictícia.` |
| `000000000003` | `Olá! Esta é uma demonstração fictícia.` |

O resumo da demonstração é **3 ações planejadas e 0 envios executados**. O terceiro registro mostra o caso sem nome. A simulação apresenta o plano no terminal; não exporta CSV.

## Experimente outros textos e contatos fictícios

Crie uma cópia da [entrada fictícia](examples/contatos-sinteticos.csv):

```bash
mkdir -p outputs
cp examples/contatos-sinteticos.csv outputs/contatos-experimento.csv
```

Edite a cópia mantendo os cabeçalhos `Nome` e `Número`. Use apenas destinos fictícios para a demonstração, preserve-os como texto e deixe `Nome` vazio para experimentar a mensagem sem prefixo. Troque o texto em `--mensagem`:

```bash
python3 -S -B zapcannon.py --simular \
  --csv outputs/contatos-experimento.csv \
  --mensagem "Este é outro texto inteiramente fictício."
```

### Salve o plano como texto

O terminal pode capturar a saída em um arquivo `.txt` dentro de `outputs/`. Escolha um nome novo; o bloco abaixo usa `noclobber` para recusar a substituição de um arquivo existente:

```bash
mkdir -p outputs
(
  set -o noclobber
  python3 -S -B zapcannon.py --simular \
    --csv examples/contatos-sinteticos.csv \
    --mensagem "Olá! Esta é uma demonstração fictícia." \
    > outputs/plano-demonstracao-01.txt
)
```

Isso é redirecionamento da saída pelo terminal, não uma exportação do programa. O arquivo contém os textos planejados e o resumo, no mesmo formato da referência; a simulação continua sem gerar CSV.

## Formato da entrada

CSV com cabeçalho, vírgula como separador, UTF-8 com ou sem BOM e aspas CSV padrão:

| Campo | Uso |
|---|---|
| `Nome` | Prefixo da mensagem; pode ficar vazio |
| `Número` | Destino textual; na simulação, somente dígitos ASCII, sem espaços ou pontuação |

Os cabeçalhos são exatamente `Nome` e `Número`, incluindo os acentos. A simulação valida toda a entrada antes de apresentar o plano e rejeita cabeçalhos ausentes/repetidos, campos incompatíveis, destinos vazios ou fora do formato e mensagem vazia. Colunas adicionais são aceitas, mas não entram no plano. Uma entrada só com cabeçalho gera zero ações.

Cada linha válida produz uma ação planejada, inclusive destinos repetidos. O formato dos dígitos não determina DDI, DDD, existência do número ou presença no serviço.

## Estrutura

- `zapcannon.py`: entrada da CLI e aplicação local Flask, com pandas e Selenium/Firefox.
- `simulacao.py`: validação do CSV e preparação dos textos com a biblioteca padrão.
- `examples/`: contatos fictícios e saída de referência.
- `templates/` e `static/`: páginas Jinja/HTML, CSS, imagens e JavaScript com jQuery. Os créditos de autoria estão nas páginas, como [home.html](templates/home.html).
- `outputs/`: arquivos locais de demonstração e resultados da interface, ignorados pelo Git.

## Interface local: Flask e Firefox

A interface recebe o CSV e a mensagem, abre o Firefox na máquina que executa o Python e acessa o WhatsApp Web. A conta é conectada por QR Code; o processamento é acionado ao submeter o formulário.

Requisitos: **Flask, pandas, Selenium 4, Firefox e geckodriver compatível**. As dependências Python estão em [requirements.txt](requirements.txt):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export GECKODRIVER_PATH='/caminho/absoluto/para/geckodriver'
python3 zapcannon.py
```

Sem argumentos, o programa inicia a aplicação Flask local em `http://127.0.0.1:5000/`. `GECKODRIVER_PATH` é lido do ambiente do processo e precisa apontar para o executável do driver antes de iniciar a aplicação. Não há carregamento automático de `.env`.

O formulário envia `csv_file` e `mensagem` por POST para `/enviar_mensagens`. O fluxo lê o CSV com `pandas.read_csv`, que infere tipos e valores ausentes: destinos com zeros iniciais podem ser convertidos em números. O leitor da simulação, por sua vez, mantém strings.

A interface percorre todas as linhas, inclusive repetidas ou já marcadas como `Enviada`. Personaliza o texto pelo nome, abre a conversa e aciona o botão de envio. No resultado, `Enviada` e o contador de sucessos representam esse acionamento; `Falha` registra um erro de processamento. Entrega e leitura não são estados acompanhados pela aplicação.

O CSV atualizado com `Status`, sem índice adicional, fica em `outputs/<nome-do-upload>` e pode ser baixado pela interface. Uploads com o mesmo nome sobrescrevem esse resultado; nomes diferentes mantêm os arquivos anteriores.

Os seletores e as esperas dependem da interface do WhatsApp Web. O navegador é fechado ao concluir o fluxo normal; falhas anteriores podem deixá-lo aberto. A aplicação é local: os resultados não têm isolamento por sessão nem autenticação para download. As páginas carregam jQuery e fontes externos, e as dependências Python são declaradas sem versões fixas.
