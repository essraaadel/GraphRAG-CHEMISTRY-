from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DB = os.getenv("NEO4J_DATABASE", "neo4j") # Default to 'neo4j' if not set

class Neo4jDatabase:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        # Specifying the database instance here
        with self.driver.session(database=NEO4J_DB) as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def seed_data(self):
        cypher_blocks = [
            'CREATE (:Element {symbol:"C", name:"Carbon"})',
            'CREATE (:Element {symbol:"H", name:"Hydrogen"})',
            'CREATE (:Element {symbol:"O", name:"Oxygen"})',
            'CREATE (:Reaction {equation:"C + 4H -> CH4"})',
            'CREATE (:Compound {name:"Methane", formula:"CH4"})',
            'CREATE (:Reaction {equation:"C + O2 -> CO2"})',
            'CREATE (:Compound {name:"Carbon Dioxide", formula:"CO2"})',
            'MATCH (c:Element {symbol:"C"}), (h:Element {symbol:"H"}), (r:Reaction {equation:"C + 4H -> CH4"}), (m:Compound {formula:"CH4"}) CREATE (c)-[:REACTANT {ratio:"1"}]->(r), (h)-[:REACTANT {ratio:"4"}]->(r), (r)-[:PRODUCT]->(m)',
            'MATCH (c:Element {symbol:"C"}), (o:Element {symbol:"O"}), (r:Reaction {equation:"C + O2 -> CO2"}), (co2:Compound {formula:"CO2"}) CREATE (c)-[:REACTANT {ratio:"1"}]->(r), (o)-[:REACTANT {ratio:"2"}]->(r), (r)-[:PRODUCT]->(co2)',
            'CREATE (:Drug {name:"Paracetamol"})',
            'CREATE (:Drug {name:"ASpirin"})',
            'MATCH(m:Compound {formula:"CH4"}), (p:Drug {name: "Paracetamol"}) CREATE (m)-[:USED_IN]->(p)',
            'MATCH (co2:Compound {formula:"CO2"}), (a:Drug {name: "ASpirin"}) CREATE (co2)-[:USED_IN]->(a)',
            'CREATE (:Disease {name:"Fever"})',
            'CREATE (:Disease {name:"Headache"})',
            'MATCH (p:Drug {name:"Paracetamol"}), (d:Disease {name:"Fever"}) CREATE (p)-[:TREATS]->(d)',
            'MATCH (p:Drug {name:"ASpirin"}), (d:Disease {name:"Headache"}) CREATE (p)-[:TREATS]->(d)',
            'CREATE (:Organism {type:"Human"})',
            'CREATE (:Organism {type:"Mouse"})',
            'MATCH (d:Disease {name:"Fever"}), (h:Organism {type:"Human"}) CREATE (d)-[:AFFECTS]->(h)',
            'MATCH (d:Disease {name:"Headache"}), (h:Organism {type:"Mouse"}) CREATE (d)-[:AFFECTS]->(h)',
            'MATCH (d:Disease {name:"Headache"}), (h:Organism {type:"Human"}) CREATE (d)-[:AFFECTS]->(h)'
        ]
        
        with self.driver.session(database=NEO4J_DB) as session:
            # Clear existing data in the targeted database
            session.run("MATCH (n) DETACH DELETE n")
            # Run each block
            for query in cypher_blocks:
                session.run(query)
        print(f"Database '{NEO4J_DB}' seeded successfully!")

# Singleton instance
db = Neo4jDatabase()
