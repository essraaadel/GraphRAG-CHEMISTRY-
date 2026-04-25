from database import db
from chain import generate_cypher
from answer_chain import generate_final_answer

def chat_with_graph(question):
    print(f"\n--- Process Flow ---")
    
    # 1. Generate Cypher
    print(f"[1] Generating Cypher query...")
    cypher_query = generate_cypher(question)
    print(f"    Cypher: {cypher_query}")
    
    # 2. Execute Query
    print(f"[2] Executing query in Neo4j...")
    try:
        results = db.run_query(cypher_query)
        print(f"    Results: {results}")
    except Exception as e:
        print(f"    Error executing query: {e}")
        return "I encountered an error while searching the graph database."

    # 3. Generate Final Answer
    print(f"[3] Formatting final answer...")
    final_answer = generate_final_answer(question, results)
    
    return final_answer

if __name__ == "__main__":
    # First, seed the database with the user's data if needed
    user_input = input("Do you want to seed/reset the database with the chemical & drug data? (y/n): ")
    if user_input.lower() == 'y':
        db.seed_data()
        
    print("\nGraphRAG Chat System is ready! (Type 'exit' to quit)")
    while True:
        question = input("\nAsk a question about the graph (e.g., 'What drugs treat Fever?'): ")
        if question.lower() in ['exit', 'quit']:
            break
            
        answer = chat_with_graph(question)
        print(f"\nFINAL ANSWER:\n{answer}")
