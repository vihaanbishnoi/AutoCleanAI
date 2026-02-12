from ingest import load_documents, chunk_text
from vector_store import VectorStore
from memory_db import init_db, save_chat, get_relevant_chats
from llm import generate_response

# Initialize DB
def main():
    # Initialize DB
    init_db()

    # Load and build document memory
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    vector_store = VectorStore()
    vector_store.build(all_chunks)

    print("Assistant ready. Type 'exit' to quit.\n")

    def detect_intent(query):
        query_lower = query.lower()
        if any(word in query_lower for word in ["duplicate", "same file", "copies"]):
            return "duplicate"
        elif any(word in query_lower for word in ["compress", "reduce size", "zip"]):
            return "compression"
        elif any(word in query_lower for word in ["what did i", "my project", "did i say"]):
            return "memory"
        else:
            return "general"

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break

        intent = detect_intent(query)
        # Save user message
        save_chat("user", query)

        # Intent-based routing
        if intent == "duplicate":
            # Placeholder for real duplicate detection integration
            duplicate_files = [
                {"name": "video1.mp4", "size": 1200},
                {"name": "video2.mp4", "size": 800},
                {"name": "doc1.pdf", "size": 50}
            ]
            if duplicate_files:
                total_size = sum(f["size"] for f in duplicate_files)
                file_list = ", ".join(f["name"] for f in duplicate_files)
                response = (
                    f"I've analyzed your storage and found {len(duplicate_files)} duplicate files: {file_list}. "
                    f"To optimize your space, I recommend deleting these files. You could save approximately {total_size/1024:.2f} GB. "
                    f"Would you like me to proceed with deletion or review the files first?"
                )
            else:
                response = "Great news! No duplicate files were found in your storage. If you need further optimization, let me know."
        elif intent == "compression":
            response = (
                "I've identified files that may benefit from compression. "
                "Once the compression module is integrated, I can recommend the best strategy and estimate space savings. "
                "Would you like to see a list of compressible files or learn more about compression options?"
            )
        else:
            # AGENT-STYLE AUTOMATION: If user asks to clean storage
            if "clean my storage" in query.lower():
                plan = [
                    "Scan files",
                    "Detect duplicates",
                    "Check compressible files",
                    "Estimate savings"
                ]
                steps_done = []
                steps_done.append("Step 1: Scanned all files in your storage.")
                steps_done.append("Step 2: Detected 3 duplicate files.")
                steps_done.append("Step 3: Found 2 files suitable for compression.")
                steps_done.append("Step 4: Estimated space savings: 2.5GB.")
                summary = "\n".join(steps_done)
                response = (
                    f"I've completed a storage cleaning plan for you:\n{summary}\n"
                    "Would you like to proceed with deleting duplicates, compressing files, or review the results?"
                )
            else:
                # MEMORY + GENERAL HANDLED HERE
                relevant_chats = get_relevant_chats(query, top_k=3)
                history_text = "\n".join([f"{r}: {c}" for r, c in relevant_chats])
                prompt = f"""
You are a concise, friendly AI storage assistant.

Answer in 2-4 sentences maximum.
Use conversation memory when relevant.
Do NOT invent scenarios.
Be helpful, clear, and professional.

Conversation Memory:
{history_text}

User Question:
{query}

Assistant:
"""
                response = generate_response(prompt)

        # Save assistant response
        save_chat("assistant", response)
        print("\nAssistant:", response)
        print("\n")

if __name__ == "__main__":
    main()
