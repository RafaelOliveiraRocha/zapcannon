# ZapCannon

Projeto histórico de estudo, registrado em julho de 2023, que combina uma interface de upload de CSV com automação do WhatsApp Web em Python. A demonstração local permite conferir os textos planejados com dados fictícios, sem enviar mensagens ou acessar serviços.

## Organização e funcionamento

- `zapcannon.py`: interface Flask e fluxo de automação com pandas e Selenium/Firefox. A escolha da simulação ocorre antes dos imports dessas dependências.
- `simulacao.py`: validação e plano de mensagens no terminal, usando somente a biblioteca padrão do Python.
- `templates/` e `static/`: páginas Jinja/HTML, CSS, imagens e JavaScript; a interface usa jQuery.
- [examples/contatos-sinteticos.csv](examples/contatos-sinteticos.csv): entrada inteiramente fictícia.
- [examples/saida-simulacao.txt](examples/saida-simulacao.txt): saída de referência da demonstração.
- `outputs/`: resultados locais do fluxo real, criados quando necessário e ignorados pelo Git. Logs e configurações locais também não integram a entrega.

O texto histórico da página inicial descreve a origem em estudos e a passagem de um bot para uma aplicação web. As páginas mantêm seus créditos e a identidade visual de 2023. O repositório não inclui arquivo de licença.

## Demonstração sem envio

Requisito: Python 3. Não precisa instalar dependências, configurar driver ou possuir credenciais. Na raiz do projeto:

```bash
python3 -S -B zapcannon.py --simular \
  --csv examples/contatos-sinteticos.csv \
  --mensagem "Olá! Esta é uma demonstração fictícia."
```

`--simular` é obrigatório para a demonstração. `-S` evita o carregamento de pacotes pela inicialização de `site`; `-B` evita caches de bytecode. Qualquer argumento de linha de comando é tratado pela interface da simulação antes dos imports de Flask, pandas e Selenium. Argumentos incorretos são rejeitados; não iniciam a interface web.

Para consultar as opções sem carregar a automação:

```bash
python3 -S -B zapcannon.py --help
```

O exemplo tem três registros: dois nomes preenchidos e um vazio. Os números com prefixo `000` são marcadores fictícios da demonstração, não uma lista para o modo real. Para cada linha, o plano mostra o número e o texto: `Nome`, uma quebra de linha e a mensagem; quando o nome está vazio, somente a mensagem. O resumo deve ser **3 ações planejadas e 0 envios executados**.

A simulação valida toda a entrada antes de mostrar ações. Não constrói links de envio, abre navegador, controla teclado/mouse, usa rede ou grava CSV de resultado. Não apresenta ações planejadas como mensagens entregues.

## Formato da entrada

CSV com cabeçalho, vírgula como separador, UTF-8 (com ou sem BOM) e aspas CSV padrão:

| Campo | Papel |
|---|---|
| `Nome` | Nome para prefixar o texto; pode ficar vazio |
| `Número` | Destino; na simulação, texto preenchido com dígitos ASCII, sem espaços ou pontuação |

Os nomes e acentos dos cabeçalhos são exatos: `Nome` e `Número`. A simulação rejeita cabeçalhos ausentes/repetidos, registros com quantidade de campos incompatível, números vazios/incompatíveis e mensagem vazia. Colunas adicionais são aceitas, mas não entram no plano. Apenas cabeçalho é uma entrada válida com zero ações.

Números são preservados como texto na simulação. A validação não confirma DDI, DDD, existência do número ou presença no WhatsApp. Não há conversão de formatos ou remoção de duplicidades: cada linha válida produz uma ação planejada.

## Interface e execução real

Este é um fluxo diferente da demonstração: abre Firefox na **máquina que executa o Python**, acessa o WhatsApp Web, exige conexão da conta por QR Code e tenta enviar mensagens. Não usa uma API oficial do WhatsApp.

Dependências identificadas no código: Flask, pandas e Selenium 4, além de Firefox e geckodriver compatíveis. `requirements.txt` declara as dependências do modo real, sem fixar um ambiente histórico. Para preparar um ambiente separado:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export GECKODRIVER_PATH='/caminho/absoluto/para/geckodriver'
```

O driver é lido de `GECKODRIVER_PATH` no ambiente do processo. Configuração ausente impede sua criação. **Não há carregamento automático de `.env`.**

`python3 zapcannon.py`, **sem argumentos**, inicia a interface Flask local. O formulário envia `csv_file` e `mensagem` por POST para `/enviar_mensagens`; o envio é iniciado somente ao submeter esse formulário. Use esse fluxo apenas com contatos e mensagens cuja utilização seja apropriada e consentida.

O fluxo real lê o CSV com pandas, acrescenta `Status` se necessário e percorre todas as linhas. Prefixa nomes presentes, codifica o texto no link do WhatsApp, espera o botão e tenta clicar. Apresenta tentativas, sucessos e erros; salva o CSV com `Status` em `outputs/<nome-do-upload>` e oferece download. Um arquivo com o mesmo nome é sobrescrito; nomes diferentes deixam resultados anteriores nesse diretório.

## Limitações

- A simulação confere estrutura e texto; não verifica acesso ao WhatsApp Web, seletores, navegador/driver ou entrega de mensagens. Uma ação planejada não comprova que o envio real funcionaria.
- O parser da simulação mantém strings e trata nome vazio como ausente. O pandas do fluxo real infere tipos e ausentes; pode remover zeros iniciais ou interpretar números de outra forma.
- O fluxo real depende da interface do WhatsApp Web e de esperas fixas. O clique é contado como sucesso, sem confirmação de entrega ou leitura. Não há deduplicação nem filtro de registros previamente marcados como `Enviada`.
- A validação de upload do fluxo real é limitada. Erros são capturados de forma ampla e o driver é fechado somente no caminho normal; falhas anteriores podem deixar o navegador aberto.
- A aplicação mantém duas rotas para `/` e uma rota estática redundante. Não há controle de concorrência para resultados com o mesmo nome ou separação por sessão, nem autenticação para downloads. Não é um serviço preparado para exposição pública.
- As versões das dependências não estão fixadas. A reprodução do ambiente original não é garantida; a interface carrega jQuery e fontes externos quando aberta no navegador.
