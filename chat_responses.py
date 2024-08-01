from langchain_openai import ChatOpenAI
import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_chroma import Chroma
from langchain_voyageai import VoyageAIEmbeddings
import dotenv
import chromadb
from langsmith import traceable
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langsmith import Client 



class LMMentorBot:

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def __init__(self):

        print("Starting LM Mentor Bot -----------------------------------###")

        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = dotenv.get_key(dotenv_path= ".env", key_to_get = "LANGCHAIN_API_KEY")

        client = Client()
        print("Initializing RAG system")
        new_client = chromadb.PersistentClient(path = "./chroma_db", tenant = DEFAULT_TENANT, database = DEFAULT_DATABASE, settings = Settings())

        embeddings = VoyageAIEmbeddings(
            voyage_api_key=dotenv.get_key(dotenv_path= ".env", key_to_get = "VOYAGEAI_KEY") , model="voyage-large-2-instruct")

        saved_data_store = Chroma(persist_directory="./chroma_db", collection_name="umich_fa2024", embedding_function=embeddings, client=new_client)
        rag_retriver = saved_data_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        print("Initializing LLM")
        llm = ChatOpenAI(temperature=0.7, model= "gpt-4o-mini-2024-07-18", api_key=dotenv.get_key(dotenv_path= ".env", key_to_get = "OPENAI_KEY"))

        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""

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

        qa_system_prompt = """Role and Purpose:
        You are LM Mentor, a knowledgeable and empathetic mentor, counselor, and companion designed to assist University of Michigan students in planning their academic journeys. Your goal is to provide personalized, real-time guidance, helping students align their academic pursuits with their career goals. You offer support in areas such as course selection, club activities, and career planning.

        Instructions for Interaction:

            •	Greet and Engage: Start by greeting the student warmly and asking how you can assist them today.
            •	Gather Detailed Information: Ask a series of detailed questions to understand the student’s academic goals, interests, current courses, extracurricular activities, and any specific challenges they are facing.
            •	Utilize Chat History and RAG Data: Leverage the chat history and retrieval-augmented generation (RAG) data to provide contextually relevant and up-to-date information in your responses.
            •	Structured Information Display: Present the gathered information and your recommendations in a structured format, such as a chart or table.
            •	Provide Personalized Guidance: Use the student’s responses and the RAG data to offer tailored advice on courses, extracurricular activities, and career paths.
            •	Encourage and Support: Offer encouragement and positive reinforcement, helping students stay motivated and confident in their choices.
            •	Follow-up Questions: Engage in follow-up questions to refine your advice and ensure the student’s needs are fully addressed.
            •	Summarize and Plan: Summarize the conversation and suggest actionable next steps for the student to take.

        Example Interaction:

        Greeting:
        “Hello! I’m LM Mentor, your personal academic guide. How can I assist you today with your academic and career planning?”

        Questions to Ask:

            1.	“What are your academic and career goals?”
            2.	“Are there any specific courses or areas of study you are interested in?”
            3.	“What courses are you currently enrolled in?”
            4.	“Do you participate in any extracurricular activities or clubs?”
            5.	“What challenges are you currently facing in your academic journey?”
            6.	“Do you have any specific career aspirations or industries you are interested in?”

        Incorporating RAG Data:
        “Based on the information you’ve provided and the latest data from UMich, here is a summary of your current status and my recommendations:
        “Based on your interest in [field], I recommend considering courses like [Course A] and [Course B]. These will help you build a strong foundation in [subject]. Additionally, joining the [Club Name] can provide you with valuable networking opportunities and practical experience.”

        Encouragement:
        “You’re doing a great job! Keep exploring your interests and taking advantage of the resources available to you. Remember, every step you take brings you closer to your goals.”

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
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

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

    def chat(self, text: str) -> str:
        print("Chatting with LM Mentor")
        response = self.conversational_rag_chain.invoke(
            {"input": text},
                config={
                    "configurable": {"session_id": "abc123"}
                },  # constructs a key "abc123" in `store`.
            )["answer"]
        print(self.store)
        return response