import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from schema import GRAPH_SCHEMA
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM with Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    temperature=0
)

# 1. Question + Schema -> Chain -> Cypher Query
cypher_generation_prompt = ChatPromptTemplate.from_template("""
You are an expert Neo4j developer.
Task: Generate a Cypher query to answer the user's question based on the provided schema.

Graph Schema:
{schema}

Instructions:
1. Use only the node labels and relationship types mentioned in the schema.
2. Be efficient: avoid returning entire nodes if only a specific property is needed.
3. Handle case-insensitivity if necessary using `toLower()`.
4. Return ONLY the Cypher query. Do not wrap it in markdown or triple backticks. No explanations.

Question:
{question}

Cypher Query:
""")

def generate_cypher(question):
    """
    Takes a question and returns a Cypher query string using Azure OpenAI GPT-4o.
    """
    chain = cypher_generation_prompt | llm
    response = chain.invoke({
        "schema": GRAPH_SCHEMA,
        "question": question
    })
    return response.content.strip()
