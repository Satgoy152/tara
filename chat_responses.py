# __import__('pysqlite3')
import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.output_parsers import StrOutputParser
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain.chains import create_history_aware_retriever
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langsmith import Client 
import streamlit as st
from retrieval import Retriever
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver



class LMMentorBot:

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def __init__(self):

        print("Starting Tara Assisstant -----------------------------------###")

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
        os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_KEY"]
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_KEY"]
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_KEY"]

        client = Client()

        print("Initializing RAG system")
        retriever = Retriever()

        # create retrievers for audit(dummy) and chat(rag)
        rag_retriver = retriever.retriver_sim
        

        print("Initializing LLM")
        
        audit_summary_llm = ChatAnthropic(temperature=0.7, model="claude-3-5-sonnet-20240620", api_key=st.secrets["ANTHROPIC_KEY"])
       

        # 
        with open("prompts/retriever_prompt.txt", "r") as f:
            retriever_prompt = f.read()

        with open("prompts/audit_summary_prompt.txt", "r") as f:
            audit_summary_prompt = f.read()

        with open("prompts/tara_prompt.txt", "r") as f:
            tara_prompt = f.read()
        
        
        audit_summary_template = ChatPromptTemplate.from_template(audit_summary_prompt)

        
        self.audit_summary_chain = audit_summary_template | audit_summary_llm


        ############ LEGACY CODE ############
        # dummy_retriever = retriever.retriever_dummy

        # llm = ChatOpenAI(temperature=0.7, model= "gpt-4o-mini-2024-07-18", api_key=st.secrets["OPENAI_KEY"], streaming=True)
        # dummy_llm = ChatOpenAI(temperature=0.7, model= "gpt-4o-mini-2024-07-18", api_key=st.secrets["OPENAI_KEY"], max_tokens=1)

        # retriever_template = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", retriever_prompt),
        #         MessagesPlaceholder("chat_history"),
        #         ("human", "{input}"),
        #     ]
        # )

        # tara_prompt_template = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", tara_prompt),
        #         MessagesPlaceholder("chat_history"),
        #         ("human", "{input}"),
        #     ]
        # )
        # history_aware_retriever = create_history_aware_retriever(
        #     audit_summary_llm, rag_retriver, retriever_template
        # )

        # audit_retrevier = create_history_aware_retriever(
        #     dummy_llm, dummy_retriever, retriever_template
        # )

        # print("Creating RAG chain")
        
        # #create chain to insert documents for context (rag documents)
        # tara_chain = create_stuff_documents_chain(llm, tara_prompt_template)

        # chain that retrieves documents and then passes them to the question_answer_chain

        # audit_text_chain2 = (
        #     {"input": audit_summary_chain},
        # )

        # rag_chain = create_retrieval_chain(history_aware_retriever, tara_chain)
        # audit_text_chain = create_retrieval_chain(audit_retrevier, tara_chain)

        # print("Creating chat history")
        # self.store = {}

        # def get_session_history(session_id: str) -> BaseChatMessageHistory:
        #     if session_id not in self.store:
        #         print("Creating new chat history for session_id", session_id)
        #         self.store[session_id] = ChatMessageHistory()
        #     return self.store[session_id]


        # self.conversational_rag_chain = RunnableWithMessageHistory(
        #     rag_chain,
        #     get_session_history,
        #     input_messages_key="input",
        #     history_messages_key="chat_history",
        #     output_messages_key="answer",
        # )

        # self.conversational_chain_no_rag = RunnableWithMessageHistory(
        #     audit_text_chain,
        #     get_session_history,
        #     input_messages_key="input",
        #     history_messages_key="chat_history",
        #     output_messages_key="answer",
        # )

        ######################################



        def get_rag_documents(query: str) -> str:  
            """Query a vector database of University of Michigan course documents. Write a precise query to retrieve relevant documents.
                    THIS IS YOUR PRIMARY TOOL CALL IT OFTEN WHEN GIVING ADVICE ON CIRRICLUM AND CLUBS FOR UMICH, DEFAULT TO THIS."""
            return f"Docuemnts: {str(rag_retriver.invoke(query))}"

        search_tool = TavilySearch(
            max_results=5,
            topic="general",)
        

        checkpointer = InMemorySaver()

        self.agent = create_react_agent(
            model="google_genai:gemini-2.0-flash",  
            tools=[get_rag_documents, search_tool],  
            prompt= tara_prompt,
            checkpointer=checkpointer,
        )

        self.config = {"configurable": {"thread_id": "1"}}


        # for token, metadata in self.agent.stream(
        #     {"messages": [{"role": "user", "content": 'Search the web for relevant information about University of Michigan courses.'}]},
        #     config=self.config,
        #     stream_mode = ["messages",]
        # ):
        #     # if metadata["langgraph_node"] == "agent" and (text := step.text()):
        #     #     print(text, end="")
            
        #     if metadata["langgraph_node"] == "agent":
        #         yield token.content
        #     elif metadata["langgraph_node"] == "tools":
        #         if token.name == "get_rag_documents":
        #             yield "Searching for relevant data... 🔍 \n\n"
        #             # print("Tool call to: ", token.name)
        #         elif token.name == "tavily_search":
        #             yield "Searching the web for relevant information... 🌐 \n\n"
        #             # print("Tool call to: ", token.name)

    def upload_degree_audit(self, text: str):
        print("Uploading degree audit")
        audit_summary = self.audit_summary_chain.invoke({"audit": text})
        print("Finished summarizing audit")
        for token, metadata in self.agent.stream(
            {"messages": [{"role": "user", "content": audit_summary.content}]},
            config=self.config,
            stream_mode = "messages",
        ):
            # if metadata["langgraph_node"] == "agent" and (text := step.text()):
            #     print(text, end="")
            
            if metadata["langgraph_node"] == "agent":
                yield token.content
            elif metadata["langgraph_node"] == "tools":
                if token.name == "get_rag_documents":
                    yield "Searching for relevant data... 🔍 \n\n"
                    # print("Tool call to: ", token.name)
            else:
                continue
  

    # def chat(self, text: str) -> str:
        
    #     print("Chatting with Tara")
    #     response = self.conversational_rag_chain.invoke(
    #         {"input": text},
    #             config={
    #                 "configurable": {"session_id": "abc123"}
    #             },  # constructs a key "abc123" in `store`.
    #         )["answer"]
    #     print(self.store["abc123"])
    #     return response
    
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
                    yield "Searching for relevant data... 🔍 \n\n"
                    # print("Tool call to: ", token.name)
                elif token.name == "tavily_search":
                    yield "Searching the web for relevant information... 🌐 \n\n"
                    # print("Tool call to: ", token.name)
            
            else:
                continue
