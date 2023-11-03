import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from bs4 import BeautifulSoup
import requests
import json
from langchain.schema import SystemMessage
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import logging
from constants import *
import time
from datetime import datetime
import pytz

# Define the Eastern Timezone (ET)
eastern_timezone = pytz.timezone("US/Eastern")

load_dotenv()
openai_key = os.getenv("OPENAI_KEY")
browserless_api_key = os.getenv("BROWSERLESS_KEY")
serper_api_key = os.getenv("SERPER_KEY")

# 1. Tool for search
def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.text


# 2. Tool for scraping
def scrape_website(objective: str, url: str):
    # scrape website, and also will summarize the content based on objective if the content is too large
    # objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url
    }

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    post_url = f"https://chrome.browserless.io/content?token={browserless_api_key}"
    response = requests.post(post_url, headers=headers, data=data_json)

    # Check the response status code
    if response.status_code == 200:
        print(f"BS4 STATUS: {response.status_code} (OK)")
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print(f"BS4 CONTENT: {text}")

        return summary(objective, text) if len(text) > MAX_TEXT_CHUNK_LEN else text
    else:
        print(f"HTTP request failed with status code {response.status_code}")


def summary(objective, content):
    llm = ChatOpenAI(openai_api_key=openai_key,
                     temperature=LLM_TEMPERATURE,
                     model=LLM_MODEL_ARCH)

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=MAX_TEXT_CHUNK_LEN, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    return summary_chain.run(input_documents=docs, objective=objective)


class ScrapeWebsiteInput(BaseModel):
    """Inputs for scrape_website"""
    objective: str = Field(
        description="The objective & task that users give to the agent")
    url: str = Field(description="The url of the website to be scraped")


class ScrapeWebsiteTool(BaseTool):
    name = "scrape_website"
    description = "useful when you need to get data from a website url, passing both url and objective to the function; DO NOT make up any url, the url should only be from the search results"
    args_schema: Type[BaseModel] = ScrapeWebsiteInput

    def _run(self, objective: str, url: str):
        return scrape_website(objective, url)

    def _arun(self, url: str):
        raise NotImplementedError("error here")


# 3. Create langchain agent with the tools above
tools = [
    Tool(
        name="Search",
        func=search,
        description="useful for when you need to answer questions about current events, data. You should ask targeted questions"
    ),
    ScrapeWebsiteTool(),
]

system_message = SystemMessage(
    content="""You are a world class researcher, who can do detailed research on any topic and produce facts based results; 
            you do not make things up, you will try as hard as possible to gather facts & data to back up the research
            
            Please make sure you complete the objective above with the following rules:
            1/ You should do enough research to gather as much information as possible about the objective
            2/ If there are url of relevant links & articles, you will scrape it to gather more information
            3/ After scraping & search, you should think "is there any new things i should search & scraping based on the data I collected to increase research quality?" If answer is yes, continue; But don't do this more than 3 iterations
            4/ You should not make things up, you should only write facts & data that you have gathered
            5/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & links to back up your research
            6/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & links to back up your research"""
)

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": system_message,
}

llm = ChatOpenAI(openai_api_key=openai_key,
                 temperature=LLM_TEMPERATURE, 
                 model=LLM_MODEL_ARCH)

memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=MAX_TOKEN_MEMORY)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

# *Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """
    Welcome route for the API.
    
    Returns:
        dict: JSON response containing a welcome message, status code, and timestamp.
    """
    # init timer
    start_time = time.time()
    current_datetime = datetime.now(eastern_timezone).strftime("%Y-%m-%d %H:%M:%S %Z")
    end_time = time.time()
    # Convert to milliseconds
    inference_time_ms = (end_time - start_time) * 1_000  
    welcome_message = {
        "output": "Hello Agent, R0D1!",
        "inference_time_ms": inference_time_ms,
        "timestamp": current_datetime,
        "status_code": 200
    }
    return make_response(jsonify(welcome_message), 200)

class Query:
    def __init__(self, query):
        self.query = query

@app.route("/query", methods=["POST"])
def research_agent():
    # init timer
    start_time = time.time()
    current_datetime = datetime.now(eastern_timezone).strftime("%Y-%m-%d %H:%M:%S %Z")
    try:
        data = request.json
        query = Query(data.get("query"))
        content = agent({"input": query.query})
        actual_content = content["output"]
        end_time = time.time()
        # Convert to milliseconds
        inference_time_ms = (end_time - start_time) * 1_000
        response_data = {
            "output": actual_content,
            "inference_time_ms": inference_time_ms,
            "timestamp": current_datetime,
            "status_code": 200
        }
        # Create a JSON response with a 200 status code
        response_data_json = jsonify(response_data)
        return make_response(response_data_json, 200)
    except Exception as e:
        # Handle errors gracefully and log them
        logger.error(f"An error occurred: {str(e)}")
        error_message = {
            "output": "An error occurred while processing the request.",
            "inference_time_ms": None,
            "timestamp": current_datetime,
            "status_code": 500
        }
        return make_response(jsonify(error_message), 500)
    
if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)