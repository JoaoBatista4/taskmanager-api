# Task Manager API

API REST para gerenciamento de tarefas com autenticação JWT, criada com FastAPI + SQLAlchemy.

## Stack

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy** (ORM)
- **SQLite** (desenvolvimento) / PostgreSQL (produção)
- **JWT** (python-jose + bcrypt)

## Setup Local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API fica em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```env
DATABASE_URL=sqlite:///./taskmanager.db
JWT_SECRET_KEY=taskmanager-super-secret-key-change-in-production-2026
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## Endpoints

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Cadastro (name, email, password) |
| POST | `/auth/login` | Login → retorna token JWT + user |

### Tasks (requer Bearer token)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/tasks` | Listar tarefas do usuário (`?status=&search=`) |
| GET | `/tasks/all` | Listar tarefas de **todos os usuários** |
| GET | `/tasks/deleted` | Listar tarefas soft-deletadas do usuário |
| GET | `/tasks/{id}` | Obter tarefa por ID |
| POST | `/tasks` | Criar tarefa |
| PUT | `/tasks/{id}` | Editar tarefa |
| DELETE | `/tasks/{id}` | Excluir tarefa permanentemente |
| PATCH | `/tasks/{id}/soft-delete` | Soft delete (marca `deleted_at`) |
| PATCH | `/tasks/{id}/status` | Alterar status |

### Categories (requer Bearer token)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/categories` | Listar categorias do usuário |
| GET | `/categories/all` | Listar categorias de **todos os usuários** |
| GET | `/categories/deleted` | Listar categorias soft-deletadas do usuário |
| POST | `/categories` | Criar categoria |
| PUT | `/categories/{id}` | Editar categoria |
| DELETE | `/categories/{id}` | Excluir categoria permanentemente |
| PATCH | `/categories/{id}/soft-delete` | Soft delete (marca `deleted_at`) |

### Dashboard (requer Bearer token)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard/stats` | Estatísticas (total, pendentes, andamento, concluídas, atrasadas) |

## Status da Tarefa

- `pendente`
- `andamento`
- `concluida`
- `atrasado`

## Prioridade

- `baixa`
- `media`
- `alta`

## Deploy no Render

1. Crie um repositório no GitHub com este código
2. No [Render Dashboard](https://dashboard.render.com), clique "New +" → "Blueprint"
3. Conecte o repositório
4. O Render detecta o `render.yaml` e cria o serviço automaticamente

Para usar PostgreSQL em vez de SQLite, crie um banco PostgreSQL no Render e altere a variável `DATABASE_URL`.

## Docker (opcional)

```bash
docker build -t taskmanager-api .
docker run -p 8000:8000 taskmanager-api
```

Ou com docker-compose:

```bash
docker-compose up --build
```
