from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import re
# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, google_api_key=API_KEY)

prompt = PromptTemplate(
    input_variables=["idea"],
    template="""
You are a startup analyst AI. Analyze the following startup idea and provide your response using clear section titles without any markdown symbols like ** or ##. Just use plain text formatting. Cover the following points:

Summary of the Idea
Target Market
Competitive Landscape
Strengths
Weaknesses
Probability of Success (in %)

Startup Idea:
{idea}
"""
)
def evaluate_idea(idea):
    formatted_prompt = prompt.format(idea=idea)
    response = llm.invoke(formatted_prompt)
    
    # Clean the response to remove any unwanted markdown symbols (* or **)
    clean_response = re.sub(r'(\*{1,2})|(\*{1,2}\s)|(\s\*{1,2})', '', response.content)
    
    return clean_response
