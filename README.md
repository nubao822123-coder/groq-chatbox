# 🚀 Chatbox sem Limites

https://files.catbox.moe/6myzkr.png

Um chatbox de ia com o groq q fiz rapido e pratico

## 🚀 Como Instalar e Rodar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

### 2. Instalação de Dependências
Clone o repositório ou baixe os arquivos e instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 3. Configuração da API
Crie um arquivo chamado `.env` na raiz do projeto e adicione a sua chave da API do Groq:

```env
GROQ_API_KEY=seu_gsk_aqui...
```

### 4. Executando o Programa
Inicie o chat com o comando:

```bash
python chatbox.py
```

## ⌨️ Comandos Disponíveis

Dentro do chat, você pode utilizar os seguintes comandos:

| Comando | Descrição | Exemplo |
| :--- | :--- | :--- |
| `/ajuda` | Mostra a lista de comandos disponíveis | `/ajuda` |
| `/novo_chat` | Inicia uma nova conversa limpa | `/novo_chat` |
| `/carregar [n]` | Carrega um chat salvo pelo número | `/carregar 1` |
| `/modelo [nome]` | Altera o modelo de IA utilizado | `/modelo llama-3.1-8b-instant` |
| `/exit` | Encerra o programa | `/exit` |

## 📂 Estrutura de Armazenamento

O programa organiza as conversas automaticamente em uma pasta chamada `conversas/`. Cada chat é salvo como um arquivo `.json` (ex: `conversa_1.json`), garantindo que você não perca o contexto da conversa mesmo após fechar o programa.

---
Desenvolvido para ser simples, rápido e sem limites! ⚡
