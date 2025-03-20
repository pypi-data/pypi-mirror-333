from abc import ABC, abstractmethod
from typing import List
from fastapi import FastAPI, HTTPException
import psycopg2
import pymongo
from langchain.llms import OpenAI
import langgraph

# ====================
# Classe astratta per la persistenza
# ====================
class ShortMemory(ABC):
    def __init__(self, session_id: str):
        self.session_id = session_id

    @abstractmethod
    def load_messages(self) -> List[str]:
        """Carica i messaggi della sessione"""
        pass

    @abstractmethod
    def save_messages(self, messages: List[str]):
        """Salva i messaggi della sessione"""
        pass

# ====================
# Implementazione per MongoDB
# ====================
class ShortMongo(ShortMemory):
    MONGO_URI = "mongodb://localhost:27017"
    MONGO_DB = "agent_db"
    MONGO_COLLECTION = "sessions"

    mongo_client = pymongo.MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB]
    mongo_collection = mongo_db[MONGO_COLLECTION]

    def load_messages(self) -> List[str]:
        session = ShortMongo.mongo_collection.find_one({"session_id": self.session_id})
        return session["messages"] if session else []

    def save_messages(self, messages: List[str]):
        ShortMongo.mongo_collection.update_one(
            {"session_id": self.session_id},
            {"$set": {"messages": messages}},
            upsert=True
        )

# ====================
# Implementazione per PostgreSQL
# ====================
class ShortPostgres(ShortMemory):
    PG_HOST = "localhost"
    PG_DB = "agent_db"
    PG_USER = "user"
    PG_PASSWORD = "password"
    PG_TABLE = "messages"

    pg_conn = psycopg2.connect(host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PASSWORD)
    pg_cursor = pg_conn.cursor()

    # Creazione tabella se non esiste
    pg_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {PG_TABLE} (
            session_id TEXT PRIMARY KEY,
            messages TEXT[]
        )
    """)
    pg_conn.commit()

    def load_messages(self) -> List[str]:
        ShortPostgres.pg_cursor.execute(f"SELECT messages FROM {ShortPostgres.PG_TABLE} WHERE session_id = %s", (self.session_id,))
        result = ShortPostgres.pg_cursor.fetchone()
        return result[0] if result else []

    def save_messages(self, messages: List[str]):
        ShortPostgres.pg_cursor.execute(f"""
            INSERT INTO {ShortPostgres.PG_TABLE} (session_id, messages)
            VALUES (%s, %s)
            ON CONFLICT (session_id) DO UPDATE SET messages = EXCLUDED.messages
        """, (self.session_id, messages))
        ShortPostgres.pg_conn.commit()

# ====================
# Classe astratta per gli agenti
# ====================
class AgentBase(ABC):
    def __init__(self, session_id: str, memory: ShortMemory):
        self.session_id = session_id
        self.memory = memory
        self.messages = self.memory.load_messages()

    @abstractmethod
    def process(self, input_message: str) -> List[str]:
        """Processa un messaggio e restituisce la risposta"""
        pass

# ====================
# Agente LangGraph che estende AgentBase
# ====================
class LangGraphAgent(AgentBase):
    def __init__(self, session_id: str, memory: ShortMemory):
        super().__init__(session_id, memory)

    def add_message(self, message: str):
        self.messages.append(message)
        self.memory.save_messages(self.messages)

    def _build_workflow(self):
        workflow = langgraph.StateGraph(LangGraphAgent)
        workflow.add_node("agent", self.agent_node)
        workflow.set_entry_point("agent")
        return workflow.compile()

    def agent_node(self, agent: "LangGraphAgent") -> "LangGraphAgent":
        """Nodo dell'agente per generare una risposta"""
        llm = OpenAI(model_name="gpt-3.5-turbo")  # Sostituire con il modello desiderato
        context = "\n".join(agent.messages)
        response = llm(context)
        agent.add_message(response)
        return agent

    def process(self, input_message: str) -> List[str]:
        """Invoca il workflow LangGraph"""
        self.add_message(input_message)
        workflow = self._build_workflow()
        final_state = workflow.invoke(self)
        return final_state.messages

# ====================
# Factory per la creazione degli agenti
# ====================
class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str, session_id: str, db_type: str = "postgres") -> AgentBase:
        memory = ShortMongo(session_id) if db_type == "mongo" else ShortPostgres(session_id)
        
        if agent_type == "langgraph":
            return LangGraphAgent(session_id, memory)
        else:
            raise ValueError(f"Agente '{agent_type}' non supportato")

# ====================
# API con FastAPI
# ====================
app = FastAPI()

@app.post("/chat")
def chat(session_id: str, input_message: str, agent_type: str = "langgraph", db_type: str = "postgres"):
    try:
        agent = AgentFactory.create_agent(agent_type, session_id, db_type)
        messages = agent.process(input_message)
        return {"session_id": session_id, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
