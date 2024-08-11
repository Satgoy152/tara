# TARA

**Tailored Academic and Resource Assistant Description**

**Overview**

Tailored Academic and Resource Assistant, or TARA for short, is an app designed to assist students at the University of Michigan in planning and navigating their academic journeys. Leveraging advanced technologies such as a Large Language Model (LLM) backbone and Retrieval-Augmented Generation (RAG), Tara provides personalized and real-time guidance tailored to each student’s unique career and academic goals. The app serves as a complementary tool to existing counseling services, offering on-demand support with domain expertise and cross-departmental insights.

**Usage**:

Create and activate conda environment:

```
conda create -n "myenv" python=3.9.19 ipython
conda activate myenv
```

Download required dependencies

```
pip install -r requirements.txt
```

API Keys store
```
mkdir .streamlit
touch .streamlit/secrets.toml
```
Add API Keys and add to `.gitignore`

Start streamlit

```
streamlit run dashboard.py  --server.enableXsrfProtection false
```
**Purpose**
The primary objective of Tara is to bridge the gap between students’ personal career aspirations and
their academic goals. Traditional counseling services often face limitations, such as time constraints,
lack of specific domain knowledge, and insufficient cross-departmental information. Tara addresses
these challenges by providing continuous, personalized guidance, ensuring that students are
well-informed about relevant courses, clubs, and opportunities that align with their interests and
career objectives.
**Note:** Tara is neither designed nor intended to replace University-provided services or support. It is
an on-demand tool designed to aid students and counselors in their planning.
**Key Features**

1. **Personalized Academic Guidance** : Utilizes student data (Student provided Degree
Audit information) and preferences to recommend courses, clubs, and extracurricular
activities.
2. **Real-Time Information** : Integrated up-to-date information on course offerings,
requirements, course scheduling, and industry trends.
3. **Domain Expertise** : Offers detailed knowledge about various fields, helping students
make informed decisions about their career paths.
4. **On-Demand Support** : Available anytime, providing immediate assistance and
assisting counselors during heavy scheduling times.
5. **Career and Academic Planning** : Assists in aligning academic pursuits with career
goals, helping students navigate their educational journey more eff actively.

**How It Works**
1. **Data Integration** : Tara integrates with UMich Course and scheduling data to access
real-time data on courses, student records, and club offerings.
2. **LLM and RAG** : The app uses a Large Language Model and Retrieval-Augmented
Generation to provide accurate and contextually relevant responses.
3. **User Interaction** : Students interact with the chatbot, asking questions and receiving
tailored guidance based on their profiles and goals.
4. **Feedback Loop** : Continuously learns from interactions and user feedback to
improve recommendations and provide more precise guidance over time.

**High-Level Diagram**
1. **User Interface** : Web portal where students interact with Tara.
2. **Data Layer** : Based on student requests and chat history, the relevant information is
retrieved from a local database. Students can also submit a pdf for further context (Degree
Audit)
3. **LLM Engine** : Processes user queries with contextual information and generates
responses using the LLM backbone.
4. **Further Interaction** : As the student responds to the assistant the LLM learns more
contextual information to provide better responses
5. **Analytics and Feedback** : Collects and analyzes data to refi ne recommendations and
improve the system.

**Data Handling and Transparency**
1. **Data Collection** : Public data from Umich websites have been gathered and parsed,
all other information is provided by the user via the chat interface.
2. **Data Storage** : No user data is stored on servers. Once a chat session ends, all user
data is removed.
3. **Data Usage** : Data is used solely for providing personalized guidance and improving
the app’s recommendations.
4. **Feedback** : Feedback data is voluntary and anonymized on retrieval.

**Benefits**
- **Enhanced Student Experience** : Provides timely and relevant guidance, enhancing the
overall student experience.
- **Informed Decision-Making** : Empowers students with the information needed to make
informed academic and career decisions.
- **Supplementary Support** : Acts as an additional resource to traditional counseling,
particularly during high-demand periods.

**Conclusion**
Tara aims to revolutionize the way students at the University of Michigan plan their academic and
career journeys. By leveraging advanced technologies and integrating with university systems, Tara
offers a comprehensive and personalized support system that aligns students’ academic pursuits
with their career goals, ultimately enhancing their educational experience.
This detailed project description covers the essential aspects of Tara, from its purpose and key
features to data handling and benefi ts, making it suitable for presentations, high-level diagrams, and
transparency documents.

**
