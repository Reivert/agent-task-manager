from google.adk.agents.llm_agent import LlmAgent as Agent
from trello import TrelloClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Configurações do Trello
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_SECRET = os.getenv('TRELLO_API_SECRET')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')

def get_temporal_context():
    from datetime import datetime
    return f"Hoje é {datetime.now().strftime('%d/%m/%Y')}."

def adicionar_tarefa(nome_da_task: str, descricao_da_tarefa: str, due_data: str):
    client = TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
        token=TRELLO_TOKEN
    )
    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == 'DIO'), None)
    if not meu_board:
        raise ValueError("Board 'DIO' não encontrado no Trello.")
    
    minha_lista = next((l for l in meu_board.list_lists() if l.name.upper() in ('TO DO', 'A FAZER')), None)
    if not minha_lista:
        raise ValueError("Lista 'TO DO' ou 'A FAZER' não encontrada no board 'DIO'.")
    
    minha_lista.add_card(
        name=nome_da_task, 
        desc=descricao_da_tarefa,
        due=due_data
    )
    return f"Tarefa '{nome_da_task}' adicionada com sucesso ao Trello."

def listar_tarefas(status: str = "todas"):
    client = TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
        token=TRELLO_TOKEN
    )
    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == 'DIO'), None)
    if not meu_board:
        return []
    
    listas = meu_board.list_lists()
    
    if status.lower() == "todas":
        listas_filtradas = listas
    else:
        status_map = {
            "a fazer": ["A FAZER", "TO DO", "TO-DO"],
            "em andamento": ["EM ANDAMENTO", "IN PROGRESS"],
            "concluido": ["CONCLUÍDO", "CONCLUIDO", "CONCLUIDOS", "DONE"]
        }
        nomes_lista = status_map.get(status.lower(), [])
        listas_filtradas = [l for l in listas if l.name.upper() in [n.upper() for n in nomes_lista]]
    
    tarefas = []
    for lista in listas_filtradas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append({
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": card.due,
                "status": status
            })
    return tarefas

def mudar_status_tarefa(nome_da_task: str, novo_status: str):
    client = TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
        token=TRELLO_TOKEN
    )
    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == 'DIO'), None)
    if not meu_board:
        return "Board 'DIO' não encontrado no Trello."
    
    listas = meu_board.list_lists()

    # Mapear Status da Tarefa
    status_map = {
        "a fazer": ["A FAZER", "TO DO", "TO-DO"],
        "em andamento": ["EM ANDAMENTO", "IN PROGRESS"],
        "concluido": ["CONCLUÍDO", "CONCLUIDO", "CONCLUIDOS", "DONE"]
    }

    nome_lista_destino = status_map.get(novo_status.lower())
    if not nome_lista_destino:
        return f"Status inválido. Use 'A Fazer', 'Em Andamento' ou 'Concluído'."
    
    lista_destino = next((l for l in listas if l.name.upper() in [n.upper() for n in nome_lista_destino]), None)
    if not lista_destino:
        return f"Lista de destino '{novo_status}' não encontrada no Trello."
    
    card_encontrado = None
    lista_origem = None

    for l in listas:
        cards = l.list_cards()
        card_encontrado = next((c for c in cards if c.name.lower() == nome_da_task.lower()), None)
        if card_encontrado:
            lista_origem = l
            break
    if not card_encontrado:
        return f"Tarefa '{nome_da_task}' não encontrada."
    
    card_encontrado.change_list(lista_destino.id)
    return f"Tarefa '{nome_da_task}' movida para '{novo_status}'."

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""
        Você é um agente gerenciador de tarefas.
        Sua função é receber uma tarefa e criar um card no Trello com o nome e descrição desta tarefa.
        Você deve me perguntar quais as atividades eu tenho no meu dia-a-dia e, com base nisso, criar um card no Trello para cada atividade.
        Você inicia a conversa perguntando quais são as tarefas do dia.
        Sempre inicie a conversa perguntando quais são as tarefas do dia informando a data pela tool get_temporal_context, e depois vai perguntando
        se tem mais alguma tarefa, até que o usuário diga que não tem mais tarefas para adicionar.

        Suas funções são:
        1. Adicionar novas tarefas com nome e descrição;
        2. Listar todas as tarefas ou filtrar por status;
        3. Marcar tarefas como concluídas ou pendentes;
        4. Remover tarefas que não são mais necessárias;
        5. Mudar o status da tarefa. Ex.: "A fazer" para "Em andamento" e de "Em andamento" para "Concluído".
        6. Gerar contexto temporal (data e hora atual) para as tarefas utilizando a função get_temporal_context.
    """,
    tools=[
        adicionar_tarefa,
        listar_tarefas,
        get_temporal_context
    ]
)
