import langchain
import langgraph
from langchain.llms import OpenAI
from langgraph.graph import StateGraph
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

# Configurazione MongoDB
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "agent_db"
MONGO_COLLECTION = "messages"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Funzioni per la persistenza
def load_messages(session_id: str):
    session = collection.find_one({"session_id": session_id})
    return session["messages"] if session else []

def save_messages(session_id: str, messages: list):
    collection.update_one(
        {"session_id": session_id},
        {"$set": {"messages": messages}},
        upsert=True
    )

# Definizione dello stato dell'agente
class AgentState:
    def __init__(self, session_id: str, messages: list = None):
        self.session_id = session_id
        self.messages = messages if messages else load_messages(session_id)

# Definizione del nodo di elaborazione dell'agente
def agent_node(state: AgentState) -> AgentState:
    llm = OpenAI(model_name="gpt-3.5-turbo")  # Sostituire con il modello desiderato
    context = "\n".join(state.messages)
    response = llm(context)
    state.messages.append(response)
    save_messages(state.session_id, state.messages)
    return AgentState(session_id=state.session_id, messages=state.messages)

# Creazione del grafo dell'agente
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")

graph = workflow.compile()

# API con FastAPI
app = FastAPI()

@app.post("/chat")
def chat(session_id: str, input_message: str):
    try:
        state = AgentState(session_id=session_id, messages=load_messages(session_id))
        state.messages.append(input_message)
        final_state = graph.invoke(state)
        return {"session_id": session_id, "messages": final_state.messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
