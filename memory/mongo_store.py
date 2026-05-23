from pymongo import MongoClient
from datetime import datetime

from utils.config import get_secret

client = MongoClient(
    get_secret("MONGO_URI")
)

db = client["research_assistant"]

collection = db["research_history"]


def save_research(
    query,
    report,
    subquestions,
    search_results,
    critique
):

    document = {
        "query": query,
        "report": report,
        "subquestions": subquestions,
        "search_results": search_results,
        "critique": critique,
        "timestamp": datetime.utcnow()
    }

    collection.insert_one(document)


def get_recent_research(limit=20):

    results = collection.find().sort(
        "timestamp",
        -1
    ).limit(limit)

    return list(results)


def delete_research(research_id):

    from bson import ObjectId

    collection.delete_one({
        "_id": ObjectId(research_id)
    })