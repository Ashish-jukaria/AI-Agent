import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables from the .env vault
load_dotenv()

# Read Neo4j connection variables
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def test_connection():
    print("Connecting to Neo4j database...")
    # Establish a driver connection using official Neo4j Python driver
    with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
        # Verify connectivity
        driver.verify_connectivity()
        print("Successfully connected to Neo4j!")
        
        # Run a simple test query to create a temporary test node and read it back
        with driver.session() as session:
            result = session.run("CREATE (n:TestNode {name: 'Hello Graph'}) RETURN n.name AS name")
            record = result.single()
            print(f"Database query successful! Node created with name: {record['name']}")

if __name__ == "__main__":
    test_connection()