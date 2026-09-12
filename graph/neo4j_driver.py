"""Owns the Neo4j driver connection. Nothing LLM-related lives here."""
import os
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not NEO4J_PASSWORD:
            raise RuntimeError(
                "NEO4J_PASSWORD is not set. Add it to your .env file."
            )
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return _driver


def verify_connection():
    """Raises a clear error if Neo4j is unreachable or credentials are wrong."""
    try:
        driver = get_driver()
        driver.verify_connectivity()
        return True
    except AuthError as e:
        raise RuntimeError(
            "Neo4j rejected the username/password. Check NEO4J_USERNAME and "
            "NEO4J_PASSWORD in .env against the credentials shown in Neo4j Desktop."
        ) from e
    except ServiceUnavailable as e:
        raise RuntimeError(
            f"Could not reach Neo4j at {NEO4J_URI}. Make sure the KJGPT instance "
            "in Neo4j Desktop is started (status RUNNING)."
        ) from e


def run_query(query: str, parameters: dict | None = None):
    """Run a Cypher query with parameters and return a list of dict records."""
    driver = get_driver()
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]


def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
