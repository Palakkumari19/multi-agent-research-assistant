from memory.mongo_store import (
    save_research,
    get_recent_research
)

save_research(
    "What are AI agents?",
    "AI agents are autonomous systems."
)

results = get_recent_research()

for r in results:
    print(r)