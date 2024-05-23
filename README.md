# Test-Uipath

## Configuração do Ambiente

### 1. Configuração do Ambiente Virtual (venv):

    Antes de começar, é recomendado criar um ambiente virtual Python para isolar as dependências do projeto. Isso garante que as bibliotecas necessárias não interfiram com outros projetos ou com o Python do sistema.

    Para criar um ambiente virtual, execute o seguinte comando no terminal:
        python -m venv nome_do_ambiente

    Em seguida, ative o ambiente virtual:
        No Windows:
            nome_do_ambiente\Scripts\Activate.ps1
        No Linux/macOS:
            source nome_do_ambiente/bin/activate
    
### 2. Instalação das Dependências:

    Após ativar o ambiente virtual, instale as dependências do projeto utilizando o arquivo requirements.txt. Isso pode ser feito com o seguinte comando:
        pip install -r requirements.txt

    Este comando irá instalar todas as bibliotecas listadas no arquivo requirements.txt, garantindo que todas as dependências necessárias estejam disponíveis para o projeto.

## Variáveis de Ambiente

    O arquivo `.env` deve conter as seguintes variáveis de ambiente:

    - `PWD`: Senha do Usuário.
    - `USER`: Usuário do sistema.
    - `SEND_EMAIL_LIST`: Lista de e-mails para envio.
    - `EMAIL_PORT`: Porta do servidor de e-mail.
    - `EMAIL_PWD`: Senha do e-mail para autenticação.
    - `EMAIL_SERVER`: Servidor de e-mail.

    Certifique-se de preencher corretamente os valores para cada variável de acordo com sua configuração.


##  Como executar o projeto

### Clonar o Repositório

    $ git clone https://github.com/abneerh/test-T2Group.git

### Configuar ambiente e instalar dependências

    Passos 1 e 2.

### Executar arquivo

    python handler.py
