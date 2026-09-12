"""Seed script: inserts Vaibhav V. Vasani into Neo4j from data/vaibhav_vasani.json.

Run with:
    python -m graph.seed_vaibhav

Safe to run multiple times -- uses MERGE, so no duplicate nodes are created.
"""
import json
import os

from graph.neo4j_driver import verify_connection, close_driver
from graph.faculty import upsert_faculty_member

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "vaibhav_vasani.json")


def load_faculty_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def main():
    print("Verifying Neo4j connection...")
    verify_connection()
    print("Connected.")

    data = load_faculty_data()
    name = data["name"]
    properties = {k: v for k, v in data.items() if k != "name"}

    empty_fields = [
        k for k, v in properties.items()
        if v in ("", [], None) or v == "TODO_VERIFY"
    ]
    if empty_fields:
        print(
            "WARNING: the following fields are still empty/unverified and will "
            f"be stored as-is: {empty_fields}"
        )

    print(f"Seeding FacultyMember: {name}")
    upsert_faculty_member(name, properties)
    print("Seed complete.")

    close_driver()


if __name__ == "__main__":
    main()
