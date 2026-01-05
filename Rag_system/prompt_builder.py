import requests


OLLAMA_URL = "http://localhost:11434/api/generate"





def Prompt_build(query, context):

    system_prompt = """
You are an explanation engine.

IMPORTANT RULES:
- You MUST NOT recommend new movies.
- You MUST NOT judge the quality of recommendations.
- You MUST NOT say the movies are unrelated.
- You MUST ONLY explain why EACH GIVEN movie could appeal to the user.


Assume the recommender system is correct.
Your job is explanation ONLY.

Explain using this format ONLY:

Movie: <title>
Reason: <explanation>

DO NOT add extra text.

"""

    

    prompt = f"""


{system_prompt}

Context:
{context}

Movies selected by the recommendation system:
{query}

Explain, one by one, why these movies may appeal to the user.
"""
    
    return prompt


def format_context(docs):
    chunks = []

    for d in docs:

        if not isinstance(d,dict):
            continue
        chunk = (
            "Title: " + str(d.get("title","N\A")) + "\n"
            "Genres: " + str(d.get("genre","N\A")) + "\n"
            "IMDB Rating: " + str(d.get("imdb_rating","N\A")) + "\n"
            "Available on: " + str(d.get("where_to_watch","N\A")) + "\n"
            "Over-view: " + str(d.get("overview","N\A"))

        )

            
        chunks.append(chunk)

    return "\n\n---\n\n".join(chunks)