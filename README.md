# bot-collie-app versão 1

## Versão 1
Essa versão tem o objetivo de tornar esse aplicativo um produto por assinatura.
É uma melhoria de UX e design em relação a versão anterior: versão 0 - beta.
E também haverá um refactor geral do código.
Em suma, tornar esse software profissional.

## Para ativar ambiente virtual
cd app
source bin/activate ou bin/activate

## Para rodar projeto
entrar no diretório /src
rodar:python3 main.py

## Para desativar ambiente virtual
deactivate

## Rodar o projeto
python3 src/main.py ou py src/main.py

## Criando novo banco de dados
Para criar um novo banco de dados excluir o arquivo bot-collie.db e descomentar a linha 384

## Usando pip no windows
Pode ser que dentro do ambiente virtual o pip não funcione, se isso acontecer:
1. Certificar-se que o pip funciona normal fora do ambiente
2. rodar: py -m pip install [pacote]

## Gerar executável com pyinstaller
procedimento pego do vídeo do python simplified -> link no obsidian
rodar:
pyinstaller --name nome_do_arquivo_exe --onefile --windowed --icon=imagem.ico main.py
no caso do projeto, rodar:
pyinstaller --name BotCollie --onefile --windowed --icon=assets/logo-icon.ico main.py

ele gera uma pasta dist com o exe, ele não roda se os arquivos que ele importa não estiver na mesma pasta (fotos, fontes e assets)

## Gerar executável com autoPytoexe
no terminal entrar na pasta src/
rodar comando: autopytoexe
se falhar tentar o comando: py -m auto_py_to_exe (windows nesse caso)
Script Location ->  escolher o arquivo principal
One File -> Selecionar One Directory
Console Window -> Window Based (hide the console)
Icon -> adicionar imagem para icone
Additional Files -> Colocar todos os arquivos que o projeto precisa para funcionar
clicar em converter

Ao terminar ele irá gerar uma pasta de nome output, o exe estára la dentro. Duplo clique nele e bala

## Zipar pasta com exe
Clicar com botão direito na pasta
Selecionar comprimir
Digitar nome do arquivo comprimido e bala