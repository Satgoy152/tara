# TARA

**Tailored Academic and Resource Assistant Description**

**Overview**

Tailored Academic and Resource Assistant, or TARA for short, is an app designed to assist students at the University of Michigan in planning and navigating their academic journeys. Leveraging advanced technologies such as a Large Language Model (LLM) backbone, Retrieval-Augmented Generation (RAG), and University of Michigan APIs, LM Mentor provides personalized and real-time guidance tailored to each student’s unique career and academic goals. The app serves as a complementary tool to existing counseling services, offering on-demand support with domain expertise and cross-departmental insights.

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

The primary objective of Tara is to bridge the gap between students’ personal career aspirations and their academic goals. Traditional counseling services often face limitations, such as time constraints, lack of specific domain knowledge, and insufficient cross-departmental information. LM Mentor addresses these challenges by providing continuous, personalized guidance, ensuring that students are well-informed about relevant courses, clubs, and opportunities that align with their interests and career objectives.

Note: LM Mentor is neither designed nor intended to replace University-provided services or support. It is an on-demand tool designed to aid students and counselors in their planning.

**Key Features**

 **1.**	Personalized Academic Guidance: Utilizes student data and preferences to recommend courses, clubs, and extracurricular activities.

 **2.** Real-Time Information: Integrates with UMich APIs to provide up-to-date information on course offerings, requirements, and industry trends.

 **3.**	Domain Expertise: Offers detailed knowledge about various fields, helping students make informed decisions about their career paths.

 **4.**	On-Demand Support: Available anytime, providing immediate assistance and reducing reliance on limited counseling sessions.

 **5.**	Career and Academic Planning: Assists in aligning academic pursuits with career goals, helping students navigate their educational journey more effectively.

**How It Works**

 **1.**	Data Integration: LM Mentor integrates with UMich APIs to access real-time data on courses, student records, and club offerings.

 **2.**	LLM and RAG: The app uses a Large Language Model and Retrieval-Augmented Generation to provide accurate and contextually relevant responses.

 **3.**	User Interaction: Students interact with the chatbot, asking questions and receiving tailored guidance based on their profiles and goals.

 **4.**	Feedback Loop: Continuously learns from interactions to improve recommendations and provide more precise guidance over time.

**High-Level Diagram**

 **1.**	User Interface: Mobile app/web portal where students interact with LM Mentor.

 **2.**	Data Layer: Integrates with UMich APIs to fetch real-time data.

 **3.**	LLM Engine: Processes user queries and generates responses using the LLM backbone.

 **4.**	RAG Module: Enhances the LLM with up-to-date and contextually relevant information.

 **5.**	Database: Stores user profiles, preferences, and interaction history.

 **6.**	Analytics and Feedback: Collects and analyzes data to refine recommendations and improve the system.

**Data Handling and Transparency**

 **1.**	Data Collection: Only essential data is collected, including academic records, preferences, and interaction history.

 **2.**	Data Storage: No data is stored on servers. Once chat data is gone

 **3.**	Data Usage: Data is used solely for providing personalized guidance and improving the app’s recommendations.

 **4.**	User Control: Students have full control over their data and can opt-out or delete their information at any time.

 **5.**	Compliance: Adheres to all relevant privacy laws and university policies to ensure ethical data handling practices.

**Benefits**

 **•**	Enhanced Student Experience: Provides timely and relevant guidance, enhancing the overall student experience.

 **•**	Informed Decision-Making: Empowers students with the information needed to make informed academic and career decisions.

 **•**	Supplementary Support: Acts as an additional resource to traditional counseling, particularly during high-demand periods.

**Conclusion**

LM Mentor aims to revolutionize the way students at the University of Michigan plan their academic and career journeys. By leveraging advanced technologies and integrating with university systems, LM Mentor offers a comprehensive and personalized support system that aligns students’ academic pursuits with their career goals, ultimately enhancing their educational experience.

This detailed project description covers the essential aspects of LM Mentor, from its purpose and key features to data handling and benefits, making it suitable for presentations, high-level diagrams, and transparency documents.

**
