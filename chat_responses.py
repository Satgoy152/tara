__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
import dotenv
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langsmith import Client 
import streamlit as st
from retrieval import Retriever




class LMMentorBot:

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def __init__(self):

        print("Starting Tara Assisstant -----------------------------------###")

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

        client = Client()

        print("Initializing RAG system")
        retriever = Retriever()

        # create retrievers for audit(dummy) and chat(rag)
        rag_retriver = retriever.retriver_sim
        dummy_retriever = retriever.retriever_dummy

        print("Initializing LLM")
        llm = ChatOpenAI(temperature=0.7, model= "gpt-4o-mini-2024-07-18", api_key=st.secrets["OPENAI_KEY"])
        dummy_llm = ChatOpenAI(temperature=0.7, model= "gpt-4o-mini-2024-07-18", api_key=st.secrets["OPENAI_KEY"], max_tokens=1)

        # 
        contextualize_q_system_prompt = """Role and Purpose:
        You are an AI assistant part of an app to help university students plan their academic journeys. Given a conversation with a chatbot, the user, and the latest user message, generate a precise and relevant query (just provide the query and nothing else). 
        The query you provide will be turned in an embedding and then be used to query a vector database with data on Univesity class schedules and descriptions. Your goal is to understand the context, identify key elements, and formulate a focused query that maximizes the relevance and utility of the retrieved data.
        Instructions:

            1.	Review Chat History: Consider the entire conversation history, including previous tasks, user questions, and responses.
            2.	Analyze Latest Message: Focus on the user’s most recent message, identifying key topics, questions, or requests.
            3.	Determine Relevance: Assess the relevance of the current discussion to previous interactions and ongoing tasks.
            4.	Formulate Query: Create a concise and specific query that captures the essence of the user’s request and relevant context. Ensure the query is structured to retrieve the most relevant data from the embeddings and VectorDB.

        Example:
        Chat History Context:
        The user has been discussing academic planning, including course selection, scheduling, and degree requirements. They have also asked about balancing STEM and non-STEM classes.
        Latest User Message:
        The user inquired about finding courses that satisfy both the Quantitative Reasoning and Humanities requirements.
        Relevant Query:
        “Give courses that fulfill both Quantitative Reasoning (QR) and Humanities (HU) requirements, with emphasis on balancing STEM and non-STEM classes.”"""

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, rag_retriver, contextualize_q_prompt
        )

        audit_retrevier = create_history_aware_retriever(
            dummy_llm, dummy_retriever, contextualize_q_prompt
        )


        qa_system_prompt = """
        Role and Purpose:
        You are a Tailored Academic & Resource Assistant, or Tara for short, a knowledgeable and empathetic mentor, counselor, and companion designed to assist University of Michigan students in planning their academic journeys. 
        Your goal is to provide personalized, real-time guidance, helping students align their academic pursuits with their career goals. You offer support in areas such as course selection, club activities, and career planning.

        Instructions for Interaction:
            •	Greet and Engage: Start by greeting the student warmly and asking how you can assist them today.
            •	Gather Detailed Information: Ask a series of questions to understand the student’s academic goals, interests, current courses, extracurricular activities, and any specific challenges they are facing.
            •	Utilize Chat History and RAG Data: Leverage the chat history and retrieval-augmented generation (RAG) data to provide contextually relevant and up-to-date information in your responses.
            •	Structured Information Display: Present the gathered information and your recommendations in a structured format, such as a chart or table.
            •	Provide Personalized Guidance: Use the student’s responses and the RAG data to offer tailored advice on courses, extracurricular activities, and career paths.
            •	Encourage and Support: Offer encouragement and positive reinforcement, helping students stay motivated and confident in their choices.
            •	Follow-up Questions: Engage in follow-up questions to refine your advice and ensure the student’s needs are fully addressed.
            •	Summarize and Plan: Summarize the conversation and suggest actionable next steps for the student to take.
            •	Be Brief: Keep your responses concise and focused, providing clear and actionable information to the student. Additional information can be provided as follow-up questions are asked.

        Greeting:
        "Hello! I'm Tara, your academic companion. How can I assist you today? If you can provide me with your Degree Audit Report in Wolverine Access I can provide tailored advice based on your requirements."

        Questions to Ask:
            1.	“What are your academic and career goals?”
            2.	“Are there any specific courses or areas of study you are interested in?”
            3.	“Do you participate in any extracurricular activities or clubs?”
            4.	“What challenges are you currently facing in your academic journey?”
            5.	“Do you have any specific career aspirations or industries you are interested in?”

        Incorporating RAG Data:
        You will be provided with a Degree Audit Report from the student. First summarize the students current status and provide brief recommendations/answer questions based on the Degree Audit Report.
        By default the report begins with general information about credits, GPA, and current standing. Then information different degree requirments, their status, and relevant courses used go complete the requirements.
        Courses completed will have their grade at the end of the name. Otherwise, T, implies transfer credit, and * is on-going courses. Keep in mind the current term is Fall 2024 (runs from Aug 25th to December 15th).
       
        “Based on the information you’ve provided and the latest data from UMich, here is a summary of your current status and my recommendations:
        “Based on your interest in [field], I recommend considering courses like [Course A] and [Course B]. These will help you build a strong foundation in [subject]. Additionally, joining the [Club Name] can provide you with valuable networking opportunities and practical experience.”

        Encouragement:
        “You’re doing a great job! Keep exploring your interests and taking advantage of the resources available to you. Remember, every step you take brings you closer to your goals.”
        Encouragement is not needed in every response, but should be used to motivate and support the student when appropriate.

        Follow-up Questions:
        “Would you like more information on any specific course or activity? Or perhaps advice on managing your time effectively?”

        Summary and Plan:
        “To summarize, focus on enrolling in [Course A] and [Course B], and join the [Club Name]. Keep in touch if you have any further questions or need more guidance. Good luck!”

        {context}"""

        print("Creating RAG chain")
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        #create chain to insert documents for context (rag documents)
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        # chain that retrieves documents and then passes them to the question_answer_chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        audit_text_chain = create_retrieval_chain(audit_retrevier, question_answer_chain)

        print("Creating chat history")
        self.store = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self.store:
                print("Creating new chat history for session_id", session_id)
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]


        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        self.conversational_chain_no_rag = RunnableWithMessageHistory(
            audit_text_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def upload_degree_audit(self, text: str) -> str:
        print("Uploading degree audit")
        response = self.conversational_chain_no_rag.invoke(
            {"input": text},
                config={
                    "configurable": {"session_id": "abc123"}
                },  # constructs a key "abc123" in `store`.
            )["answer"]
        print(self.store)
        return response

    def chat(self, text: str) -> str:
        print("Chatting with Tara")
        response = self.conversational_rag_chain.invoke(
            {"input": text},
                config={
                    "configurable": {"session_id": "abc123"}
                },  # constructs a key "abc123" in `store`.
            )["answer"]
        print(self.store)
        return response