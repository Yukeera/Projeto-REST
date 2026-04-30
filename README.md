# 🚚 Projeto REST - Sistema de Gestão de Frota e Entregas

Este projeto é uma aplicação fullstack para gerenciamento de **entregas, veículos e motoristas**, composta por:

* 🔙 **Backend**: API REST desenvolvida com Django + Django REST Framework
* 🔜 **Frontend**: Interface web em Angular
* 🔗 Comunicação via HTTP (API REST)

---

## 📌 Funcionalidades

### Backend (API REST)

* Cadastro e gerenciamento de:

  * 🚚 Veículos
  * 👨‍✈️ Motoristas (drivers)
  * 📦 Entregas (deliveries)
* Serialização de dados com Django REST Framework
* Estrutura modular (apps separadas)

### Frontend (Angular)

* Interface amigável para:

  * Listar entregas, veículos e motoristas
  * Navegação via menu
* Consumo da API REST via serviços (gateway)

---

## 🏗️ Estrutura do Projeto

```
Projeto-REST-main/
│
├── core/               # Configurações principais do Django
├── deliveries/         # App de entregas
├── vehicles/           # App de veículos
├── gateway/            # (Possível integração/API gateway)
│
├── fleet-client/       # Frontend Angular
│   ├── src/app/
│   │   ├── components/
│   │   │   ├── deliveries/
│   │   │   ├── drivers/
│   │   │   ├── vehicles/
│   │   │   └── navbar/
│   │   └── services/
│
├── manage.py
└── requirements.txt
```

---

## ⚙️ Tecnologias Utilizadas

### Backend

* Python
* Django
* Django REST Framework

### Frontend

* Angular
* TypeScript
* HTML/CSS

---

## 🚀 Como Executar o Projeto

### 🔹 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Projeto-REST-main
```

---

### 🔹 2. Configurar o Backend (Django)

#### Criar ambiente virtual

```bash
python -m venv venv
```

#### Ativar ambiente

* Windows:

```bash
venv\Scripts\activate
```

* Linux/Mac:

```bash
source venv/bin/activate
```

#### Instalar dependências

```bash
pip install -r requirements.txt
```

#### Rodar migrações

```bash
python manage.py migrate
```

#### Iniciar servidor

```bash
python manage.py runserver
```

📍 Backend disponível em:

```
http://127.0.0.1:8000/
```

---

### 🔹 3. Configurar o Frontend (Angular)

```bash
cd fleet-client
npm install
```

#### Rodar aplicação

```bash
ng serve
```

📍 Frontend disponível em:

```
http://localhost:4200/
```

---

## 🔌 Integração Frontend ↔ Backend

O frontend se comunica com o backend através de um **service (gateway.service.ts)**, responsável por:

* Fazer requisições HTTP
* Centralizar chamadas da API
* Facilitar manutenção

---

## 📂 Principais Componentes

| Componente | Descrição                   |
| ---------- | --------------------------- |
| deliveries | Gerenciamento de entregas   |
| drivers    | Gerenciamento de motoristas |
| vehicles   | Gerenciamento de veículos   |
| navbar     | Navegação da aplicação      |

---

## 🧠 Organização do Backend

Cada entidade segue o padrão:

* `models.py` → estrutura do banco
* `serializers.py` → conversão para JSON
* `admin.py` → painel administrativo

---

## 📈 Possíveis Melhorias

* Autenticação (JWT ou Session)
* Paginação na API
* Filtros e buscas
* Dashboard com métricas
* Deploy (Docker / Cloud)

---

## 👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos e aprendizado de arquitetura fullstack com APIs REST.

---

## 📜 Licença

Este projeto está livre para uso educacional.
