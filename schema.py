# This file defines the graph schema for the LLM to understand the structure.

GRAPH_SCHEMA = """
Nodes:
- Element: {symbol: string, name: string}
- Reaction: {equation: string}
- Compound: {name: string, formula: string}
- Drug: {name: string}
- Disease: {name: string}
- Organism: {type: string}

Relationships:
- (:Element)-[:REACTANT {ratio: string}]->(:Reaction)
- (:Reaction)-[:PRODUCT]->(:Compound)
- (:Compound)-[:USED_IN]->(:Drug)
- (:Drug)-[:TREATS]->(:Disease)
- (:Disease)-[:AFFECTS]->(:Organism)

Example Relationship Logic:
- Elements are reactants in a Reaction.
- Reactions produce Compounds.
- Compounds are used in Drugs.
- Drugs treat Diseases.
- Diseases affect Organisms.
"""
