
# 💰 Cashflow Tracker API (Backend)

API REST desenvolvida com **Flask** e **SQLAlchemy** para auxiliar na gestão do fluxo de caixa de um restaurante de pequeno porte.  
Permite que os responsáveis pelo financeiro registrem entradas e saídas de forma prática, visualizem o histórico atualizado e acompanhem o status dos lançamentos.

> 💻 A aplicação é voltada exclusivamente para **uso em desktop**, com comunicação com um frontend SPA desenvolvido separadamente.

---

## 📌 Índice

1. [Descrição do Projeto](#-descrição-do-projeto)  
2. [Tecnologias Utilizadas](#-tecnologias-utilizadas)  
3. [Instalação e Execução](#-instalação-e-execução)  
4. [Rotas e Funcionalidades da API](#-rotas-e-funcionalidades-da-api)  
5. [Como Usar](#-como-usar)  
6. [Plano de Testes](#-plano-de-testes)

---

## 🧾 Descrição do Projeto

A Cashflow Tracker API é uma aplicação backend que gerencia lançamentos de fluxo de caixa, como vendas, despesas e retiradas em dinheiro do restaurante.

### 📌 Principais objetivos:
- Oferecer controle granular de lançamentos feitos em dinheiro
- Otimizar a conferência dos saldos entre o caixa físico e o sistema contábil principal (ERP)
- Permitir atualizações recorrentes de maneira simples e estruturada

### 📌 Público-alvo:
- Time financeiro e sócios administradores do restaurante

---

## 🔧 Tecnologias Utilizadas

- **Python 3.11**
- **Flask**
- **Flask-OpenAPI3** para documentação automática (Swagger UI)
- **SQLAlchemy** + **SQLite** para ORM e persistência
- **Flask-CORS** para integração com o frontend
- **Pydantic** para validação de schemas

---

## ⚙️ Instalação e Execução

### ✅ Pré-requisitos

- Python 3.11 ou superior
- Navegador moderno (para testes no Swagger)

### 🔄 Passo a passo

```bash
# Baixe o .zip do repositório:
https://github.com/brunacaffaro/cashflowcontrol-backend/
```

```bash
# Abra o PowerShell para criar e ativar o ambiente virtual (nome sugerido: meu-venv)
python -m venv meu-venv
.\meu-venv\Scripts\Activate.ps1
# Clicando no arquivo app.py, você deve ver no canto inferior direito a sua versão do Python ao lado de (meu-venv).
# Caso não veja, clique ali e selecione meu-venv como o "Interpreter"
```

```bash
# Se estiver rodando o terminal dentro da pasta onde se encontram os requirements, digite:
pip install -r requirements.txt
# Caso esteja em uma pasta superior, use o comando a seguir para entrar na pasta (confira o nome a depender de como fez o download):
cd .\cashflowcontrol-backend-main
```

```bash
# Execute o servidor
flask run --host 0.0.0.0 --port 5000 --reload
# Acesse a documentação com o link apresentado no terminal ou utilizando: http://localhost:5000/openapi
# Clique em Swagger para visualizar a documentação
```

---

## 🔁 Rotas e Funcionalidades da API

| Método | Rota                    | Descrição                                        |
|--------|-------------------------|--------------------------------------------------|
| GET    | `/transactions`         | Lista todos os lançamentos (ordem decrescente)   |
| POST   | `/transaction`          | Adiciona um novo lançamento                      |
| GET    | `/transaction?name=...` | Busca um lançamento pelo nome                    |
| PATCH  | `/transaction/status`   | Atualiza o status de um lançamento               |
| DELETE | `/transaction?name=...` | Remove um lançamento pelo nome                   |

### 🧠 Observações:
- O campo `status` é atualizado via checkbox no frontend.
- Os lançamentos exibidos no frontend são limitados aos **últimos 90 dias** para melhor performance.
- As datas são salvas como `DateTime` (padrão do Python/SQLAlchemy).

---

## 🧪 Como Usar

- O frontend consome essa API utilizando **fetch()** e **formulários HTML5**.
- Os testes podem ser feitos diretamente via Swagger, disponível em `/openapi`.

---

## ✅ Plano de Testes

### Ambiente de Teste

- **Dispositivo:** Desktop
- **Browser:** Chrome, Edge
- **Resoluções testadas:** a partir de 1025px 

#### 📌 Lançamentos
- ✅ Adicionar lançamento com todos os campos válidos
- ✅ Tentar adicionar lançamento com campos faltando
- ✅ Adicionar múltiplos lançamentos no mesmo dia
- ⚠️ Adicionar lançamento com valor negativo (essa restrição não existe dentro do Swagger)

#### 📌 Histórico e Status
- ✅ GET lista ordenada por data decrescente
- ✅ Lançamentos anteriores a 90 dias aparecem no database e no GET/transactions
- ✅ PATCH altera status de "Pendente" para "Lançado" e vice-versa
- ✅ DELETE remove corretamente do database

#### 📌 Validações internas
- ✅ Datas salvas corretamente como `datetime`
- ✅ Erro 404 para remoção de lançamento inexistente (Lançamento não encontrado na base)
