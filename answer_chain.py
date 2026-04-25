import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM with Azure OpenAI
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    temperature=0.7
)

# 3. Results + Question -> LLM -> Final Answer
answer_generation_prompt = ChatPromptTemplate.from_template("""
You are a highly capable scientific assistant specialized in pharmacology and chemistry.
Based on the following data retrieved from a Neo4j knowledge graph, provide a clear, professional, and accurate response to the user's question.

Retrieved Data (JSON format):
{results}

User Question:
{question}

Response Guidelines:
- If the data is empty, say you don't have that information in the graph.
- Synthesize the information into natural language.
- Mention specific relationships if relevant.
- Be concise but informative.

Final Answer:
""")

def generate_final_answer(question, results):
    """
    Takes the original question and the Neo4j query results, returns a conversational answer using Azure OpenAI.
    """
    if not results or len(results) == 0:
        return "I couldn't find any relevant information in the database to answer that question."
        
    chain = answer_generation_prompt | llm
    response = chain.invoke({
        "results": results,
        "question": question
    })
    return response.content.strip()
