# 🤖 Agent Task Manager

Um agente inteligente desenvolvido em Python capaz de interagir com o Trello via comandos de texto, permitindo gerenciar tarefas de forma simples e automatizada.

## 🚀 Funcionalidades

- 📋 Listar cards de um board do Trello  
- ➕ Criar novos cards  
- 🔄 Mover cards entre listas (status)  
- 💬 Interação via chat com linguagem natural  

## 🧠 Como funciona

O agente utiliza integração com IA para interpretar comandos em linguagem natural e executar ações diretamente na API do Trello.

Exemplo de fluxo:

- "Liste minhas tarefas"
- "Crie uma tarefa chamada Estudar IA"
- "Mova a tarefa Estudar IA para Andamento"
- "Marque a tarefa como concluída"

Tudo isso sem precisar acessar o Trello manualmente.

## 🔗 Integrações

### Trello API
Para comunicação com o Trello, foram utilizadas as seguintes credenciais:

- API Key  
- Token  
- Secret  

Essas credenciais permitem que o agente:

- Consulte boards e listas  
- Crie e atualize cards  
- Movimente tarefas entre status  

### Google AI Studio
O agente utiliza uma chave de API do Google AI Studio para interpretar comandos em linguagem natural e transformar em ações estruturadas.

## 📦 Estrutura do Projeto
