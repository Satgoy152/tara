__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import os
import streamlit as st
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from tools import get_tools


class LMMentorBot:

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def __init__(self):

        print("Starting Tara Assisstant -----------------------------------###")

        os.environ["LANGCHAIN_TRACING_V2"] = "false"

        os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_KEY"]
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_KEY"]
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_KEY"]
        
        print("Initializing LLM")
        
        

        with open("prompts/audit_summary_prompt.txt", "r") as f:
            audit_summary_prompt = f.read()

        with open("prompts/tara_prompt.txt", "r") as f:
            tara_prompt = f.read()
        
        
        audit_summary_template = ChatPromptTemplate.from_template(audit_summary_prompt)
        audit_summary_llm = ChatAnthropic(temperature=0.7, model="claude-3-5-sonnet-20240620", api_key=st.secrets["ANTHROPIC_KEY"])
        
        self.audit_summary_chain = audit_summary_template | audit_summary_llm

        checkpointer = InMemorySaver()

        self.llm = init_chat_model(
            model="google_genai:gemini-2.5-flash",
            temperature=0.7,
        )

        self.agent = create_react_agent(
            model=self.llm,
            tools=get_tools(),  
            prompt= tara_prompt,
            checkpointer=checkpointer,
        )

        self.config = {"configurable": {"thread_id": "1"}}


    def upload_degree_audit(self, text: str):
        print("Uploading degree audit")
        audit_summary = self.audit_summary_chain.invoke({"audit": text})
        print("Finished summarizing audit")
        print("Audit summary: ", audit_summary.content)
        for token, metadata in self.agent.stream(
            {"messages": [{"role": "user", "content": audit_summary.content}]},
            config=self.config,
            stream_mode = "messages",
        ):
            if metadata["langgraph_node"] == "agent":
                yield token.content
            elif metadata["langgraph_node"] == "tools":
                if token.name == "get_rag_documents":
                    yield "Searching for relevant data... 🔍 \n\n"
            else:
                continue
  

    
    def chat_stream(self, text: str):
        print("Chatting with Tara")
        for token, metadata in self.agent.stream(
            {"messages": [{"role": "user", "content": text}]},
            config=self.config,
            stream_mode = "messages",
        ):
            # if metadata["langgraph_node"] == "agent" and (text := step.text()):
            #     print(text, end="")
            
            if metadata["langgraph_node"] == "agent":
                yield token.content
            elif metadata["langgraph_node"] == "tools":
                if token.name == "get_rag_documents":
                    yield " 🔍 Searching for relevant data...  \n\n"
                elif token.name == "tavily_search":
                    yield " 🌐 Searching the web for relevant information... \n\n"
                    # print("Tool call to: ", token.name)
            
            else:
                continue
