# Kompose

## Erros e correções aplicadas

---
**Código com erro:**  

```sh
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

**Erro:** O app "songs" não está declarado em INSTALLED_APPS  

**O que ele causa:** O Django não consegue identificar as informações desse app para executá-lo.  

**Como corrigir:** Incluir a linha com o nome do app "songs" dentro de INSTALLED_APPS, fazendo com que ele seja reconhecido pelo Django.  

**Código corrigido:**

```sh
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "songs"
]
```

---

**Código com erro:**  

```sh
DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgres", 
            "NAME": os.getenv("DB"),
            "USER": os.getenv("USER"),
            "PASSWORD": os.getenv("PASSWORD"),
            "HOST": "database", 
            "PORT": 5432,
        }
}
```

**Erro:** A linha que especifica o tipo de conexão com o Banco está incorreta e as Variáveis de Ambiente não estão no padrão que o Postgres espera.

**O que ele causa:** A aplicação não consegue se conectar ao Banco de Dados.

**Como corrigir:** Colocar "postgresql" ao invés de "postgres" no campo "ENGINE" e alterar o nome das Variáveis de Ambiente.

**Código corrigido:**

```sh
DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": "db",
            "PORT": 5432,
        }
}
```

---

**Código com erro:**  

```sh
FROM python:3.9

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

WORKDIR /code
COPY . /code/

```

**Erro:** A instalação das dependências através do "requirements.txt" está sendo executada antes do arquivo ser copiado para o Container.

**O que ele causa:** A instalação dos pacotes necessários para a execução da aplicação falha por não existir o arquivo.

**Como corrigir:** Executar o comando após os arquivos do projeto serem copiados para o Container.

**Código corrigido:**

```sh
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY . /code/

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

RUN pip install -r requirements.txt

```

---

**Código com erro:**  

```sh
web:
        env_file: envs/dev.env
        command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py runserver 0.0.0.0:8000'

        stdin_open: true
        tty: true
        volumes:
            - .:/code

        ports:
            - 8000:8001

        depends_on:
            - db
            - migration
```

**Erro:** Não está sendo especificado para o serviço sobre qual imagem executar e a ponte entre as portas está direcionando para uma porta não utilizada pela aplicação.

**O que ele causa:** O serviço não é iniciado por não ter uma imagem para executar e a aplicação não recebe requisições porque não está expondo a porta correta.

**Como corrigir:** Especificar sobre qual imagem o serviço irá rodar e expor a porta que está sendo utilizada pela aplicação.

**Código corrigido:**

```sh
web:
        image: kompose_image
        env_file: envs/dev.env
        command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; python manage.py runserver 0.0.0.0:8000'

        stdin_open: true
        tty: true
        volumes:
            - .:/code

        ports:
            - 8000:8000

        depends_on:
            - db
            - migration
```

---
