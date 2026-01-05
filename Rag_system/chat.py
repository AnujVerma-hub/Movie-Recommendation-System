from rag_pipeline import rag_answer
from SRC.orchestrator import hybrid_recommend


print("Movie RAG Assistant (type 'exit' to quit)\n")

while True:
    query = input("You: ").lower()
    if query == "exit":
        break 

    if "recommend for me" in query:
        user_id = int(input("Enter user id:"))
        movies, explanation = hybrid_recommend("user", user_id)
        print("\n Recommended Movies:")
        for m in movies[:10]:
            print("-", m)

        print("\n Assistant:", explanation)

    elif "movies like" in query:
        movie = input("Enter movie this: ")
        movies, explanation = hybrid_recommend("item", movie)
        print("\n Similar Movies:")
        for m in movies[:10]:
            print("-", m)

        print("\n Assistant:", explanation)


    else:
        print("\n Assistant:", rag_answer(query))





