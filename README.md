# Gerenciador de Lembretes

Aplicação simples em Python para gerenciamento de lembretes, com suporte a cadastro e autenticação de usuários, utilizando banco de dados SQLite para persistência das informações.

O projeto foi desenvolvido com foco em organização, simplicidade e aprendizado de boas práticas em Python, banco de dados e versionamento com Git/GitHub.

---

## Funcionalidades

- Cadastro de usuários com senha criptografada (SHA-256)
- Autenticação de usuários
- Criação e gerenciamento de lembretes
- Armazenamento local utilizando SQLite
- Estrutura modular separando lógica de banco e aplicação

---

## Tecnologias Utilizadas

- Python 3
- SQLite3
- hashlib (para criptografia de senha)
- Git e GitHub

---

## Estrutura do Projeto

gerenciador-lembretes/
│
├── main.py # Arquivo principal da aplicação
├── database.py # Funções de acesso ao banco de dados
├── icone.ico # Ícone do aplicativo
├── .gitignore # Arquivos ignorados pelo Git
└── README.md # Documentação do projeto

yaml
Copiar código

---

## Como Executar o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/Lukas-math-ven/gerenciador-lembretes.git
Acesse a pasta do projeto:

bash
Copiar código
cd gerenciador-lembretes
Execute o programa:

bash
Copiar código
python main.py
O banco de dados (lembretes.db) será criado automaticamente na primeira execução.

Observações Importantes
O banco de dados não é versionado no GitHub por boas práticas.

Pastas como venv/ e __pycache__/ são ignoradas via .gitignore.

O projeto pode ser facilmente expandido para interface gráfica ou notificações.

Autor
Desenvolvido por Lukas Matheus Venancio
GitHub: https://github.com/Lukas-math-ven