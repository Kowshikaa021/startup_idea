from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, google_api_key=API_KEY)

prompt = PromptTemplate(
    input_variables=["idea"],
    template="""
You are a startup analyst AI. Analyze the following startup idea and provide:
- A summary of the idea
- Target market
- Competitive landscape
- Strengths
- Weaknesses
- Probability of success (in %)

Startup Idea:
{idea}
"""
)

def evaluate_idea(idea):
    formatted_prompt = prompt.format(idea=idea)
    response = llm.invoke(formatted_prompt)
    return response.content

