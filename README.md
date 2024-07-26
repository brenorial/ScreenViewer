# Screen Viewer App

Aplicativo desenvolvido em Python usando `customtkinter` para visualizar múltiplos monitores em tempo real. O usuário pode selecionar quais monitores deseja visualizar e iniciar a visualização ao pressionar um botão "Play".

## Funcionalidades

- Listagem de todos os monitores disponíveis.
- Seleção de múltiplos monitores para visualização.
- Exibição das capturas de tela dos monitores selecionados em tempo real.

## Dependências

- `mss`: Para capturar a tela.
- `Pillow`: Para manipulação de imagens.
- `customtkinter`: Para a interface do usuário.

## Instalação

Instale as dependências utilizando `pip`:

```bash
pip install mss pillow customtkinter
```

# Convertendo o Aplicativo Python em um Executável `.exe` com PyInstaller

Para converter um aplicativo Python em um executável `.exe`, você pode usar uma ferramenta como `PyInstaller`. Abaixo estão os passos para usar o `PyInstaller`, que é uma das ferramentas mais populares para essa tarefa.

## Passos para Converter um Aplicativo Python em `.exe` com PyInstaller

### 1. Instale o PyInstaller

Primeiro, você precisa instalar o `PyInstaller`. Isso pode ser feito com o seguinte comando:

```bash
pip install pyinstaller
```

### 2. Navegue até o Diretório do Seu Script

Abra o terminal ou prompt de comando e navegue até o diretório onde está localizado o seu script Python (`screen_viewer.py`).

```bash
cd caminho/para/seu/diretório
```

### Execute o PyInstaller para criar o executável. Use o comando abaixo para gerar o .exe:

``` bash
pyinstaller --onefile --noconsole screen_viewer.py
```

- --onefile: Cria um único arquivo .exe em vez de uma pasta com vários arquivos.
- --noconsole: (Opcional) Remove a janela do console, útil para aplicativos GUI que não precisam de um console de comando.

##  4. Encontre o Executável
Após a execução do PyInstaller, você encontrará o arquivo .exe na pasta dist dentro do diretório onde seu script está localizado.
