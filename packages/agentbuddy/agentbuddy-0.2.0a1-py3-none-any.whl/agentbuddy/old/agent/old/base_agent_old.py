import os
import json
from letta_client import Letta, MessageCreate, AssistantMessage, EmbeddingConfig
from letta_client import LlmConfig as LLMConfig
# from letta import ChatMemory
from agentbuddy.session.client import ManagedSessionServiceClient

class BaseAgent():

    def __init__(self,
                 session_id:str,
                 agent_type:str,
                 human:str,  
                 persona:str,
                 tools:list,
                 memory_human:str = "",
                 memory_persona:str = "",
                 ) -> None:
        
        self._tools = tools

        self._client = self._get_letta_client()

        self._session_id = session_id
        
        self._session = ManagedSessionServiceClient(base_url=os.getenv("SESSION_BASE_URL", default="http://localhost:8002"),session_id=session_id)

        #TODO move into twin
        if agent_type == "digital-twin":
            memory_human = f"""
            Name: {self._session.get_session_data("name")}
            {self._session.get_session_data("short-description")}
            """
            memory_persona="""
            Name: agentBuddy
            When the user asks a question use the function get_help if your knowledge is limited about the question. 
            The function can explain better about multiple domains. 
            Do not ask the user any questions until you have first consulted the get_help function.
            """

        self._agent_id = self._session.get_agent_id(agent_type)
        if not self._agent_id:
            self._persona = persona
            self._human = human
            self._agent_id = self._create_agent(human=memory_human,persona=memory_persona)
            self._session.put_agent_id(agent_type,self._agent_id)

    def get_agent_id(self):    
        return self._agent_id

    def _get_letta_client(self):
        client = Letta(
            base_url=os.getenv("LETTA_BASE_URL", default="http://localhost:8283"),
        )
        return client
    
    def _create_agent(self,human:str="",persona:str=""):
        tools = []
        llmconfig=LLMConfig(
            model=os.getenv("LLM_MODEL", default="letta-free"),
            model_endpoint_type=os.getenv("LLM_MODEL_TYPE", default="letta"),
            # model_endpoint="https://inference.memgpt.ai",
            context_window= 16000,
            # put_inner_thoughts_in_kwargs= True,
            # handle="letta/letta-free",
            # temperature= 0.7,
        )
        embeddingconfig = EmbeddingConfig(
            embedding_endpoint_type = os.getenv("LLM_EMB_MODEL_TYPE", default="letta"),
            # embedding_endpoint = "https://embeddings.memgpt.ai",
            embedding_model =os.getenv("LLM_EMB_MODEL", default="letta-free"),
            # embedding_dim = 1024,
            # embedding_chunk_size = 300,
            # handle = "letta/letta-free",
            # azure_endpoint = None,
            # azure_version = None,
            # azure_deployment = None,
        )
        # for tool in self._tools:
        #     try:
        #         t = self._client.create_tool(tool, tags=["extras"])
        #         tools.append(t.name)
        #     except Exception as e:
        #         print("WARN: ", e)

        # chatmemory = ChatMemory(
        #     human=human,
        #     persona=persona,
        # )
        
        #chatmemory.core_memory_append("human","")
        #chatmemory.core_memory_append("persona",f"your session_id is: {self._session_id}")

        _agent_client = self._client.agents.create(
            memory_blocks=[],
            tools=tools,
            llm_config=llmconfig,
            embedding_config=embeddingconfig,    
            # from_template="", TODO da creare template
            #memory = chatmemory,
            # metadata = {"human:": self._human, "persona": self._persona},
        )
        return _agent_client.id
    
    def send_message(self, question):
        response = self._client.agents.messages.create(
            agent_id=self._agent_id,
            messages=[
            MessageCreate(
                role="user",
                content=question,
            )
            ],
        )
        return list(map(lambda msg: msg.model_dump(), response.messages)), response.usage

        
    
    def _handle_message(self,messages):
        response = None
        for message in messages:
            if isinstance(message,AssistantMessage):
                return message.content
            # if 'internal_monologue' in message:
            #     print("Internal Monologue:", message['internal_monologue'])
            # elif 'function_call' in message:
            #     try:
            #         function_arguments = json.loads(message['function_call']['arguments'])
            #         print(f"Function Call ({message['function_call']['name']}):", function_arguments)
            #         if message['function_call']['name'] == 'send_message':
            #             response = function_arguments['message']
            #     except json.JSONDecodeError:
            #         print("Function Call:", message['function_call'])
            # elif 'function_return' in message:
            #     print("Function Return:", message['function_return'])
            # else:
            #     print("Message:", message)
            #     # TODO warning
            #     return message
        return ""
    
    def notify(self, news):
        # TODO problem, la risposta non arriva sempre nella function call.
        message, usage = self.send_message(news)
        return message
    
    def ask(self, question):
        # TODO problem, la risposta non arriva sempre nella function call.
        request =f"without more question about it, search in your archival memory and give an accurate response to the question: {question}. give me the response always in the function call with the send_message. respond without any comment or disclaimer."
        message, usage = self.send_message(request)
        response = self._handle_message(message)
        return str(response)
    
    def request(self, agents,request):
        # TODO problem, la risposta non arriva sempre nella function call.
        instructions = f"""You are the coordinator of these agents which you can call with the function ask_to: {str(agents)}. 
        The user has made the following request: {request}. 
        Break down the request into steps and for each part, try to use at least one agent. 
        Then try to response to the quesiton.
        If you need more information from the user, you can request it from the digital twin.
        To ask the digital twin, you can use the ask_to function at the address digital-twin:8005
        """
        # Provide in JSON format, without commenting, the following structure: 
        # {{'observation': 'observation', 'questions': [('question', 'agent_name')]}}
        # In the observation field, insert a description of what you have decided."""
        message, usage = self.send_message(instructions)
        response = self._handle_message(message)
        return str(response)
    
    def create_source(self, name):
        source = self._client.create_source(name=name)
        return source.id
    
    def add_file_to_source(self, source_id, filename):
        self._client.load_file_into_source(filename=filename, source_id=source_id)
        self._client.attach_source_to_agent(source_id=source_id, agent_id=self._agent_client)
        