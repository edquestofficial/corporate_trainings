import gradio as gr
import requests

# Ollama Server Configuration
OLLAMA_SERVER = "http://16.171.237.183:11434"

# Payload template
payload = {
    "model": "llama3:8b",
    "prompt": "",
    "stream": False
}

# Direct LLaMA model call 
def call_llama_direct(prompt):
    payload['prompt'] = prompt
    try:
        response = requests.post(
            f"{OLLAMA_SERVER}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        if "response" in result:
            return result["response"].strip()
        else:
            print("Unexpected LLaMA API response:", result)
            return "Error: Unexpected response format from model server."
    except requests.exceptions.RequestException as e:
        print("Error connecting to Ollama server:", e)
        return "Error: Could not connect to model server."

# Prompt LLaMA to return ONLY a valid Solr query
def get_solr_query_from_llama(user_question):
    prompt = f"""You are a system that converts natural language into valid Apache Solr query strings to fetch the data from Solr database.\n
    Respond with ONLY the valid Solr query. Don't try to give me random response. I need only Solar Query\n
    Use correct field:value syntax, range queries like field:[min TO max], and logical operators (AND, OR).\n
    if user asking for above a cartain score take 100 as max and for below a cartain marks take 0 as min.\n
    if someone it typing Mathematics, Maths, maths, mathematics so you have to treat it as a Math\n
    Same way if someone is typing science, sci, scin, Scin, Sci and For history, his, HIS, History, HISTORY treat it Science, History\n
    Example:\n
    User question: Who scored more than 80 in Science?\n
    Response: subject:Science AND score:[81 TO *]\n
    Do NOT include any explanations, labels, or extra formatting.\n
    DO NOT include any explanations, lables, or extar formatting.\n
    User question: {user_question}"""
    return call_llama_direct(prompt)

# Format Solr result into a clean sentence

def format_solr_result(docs, original_question=""):
    try:
        subject  = docs[0]['subject'][0]
        names = [doc["name"][0] for doc in docs if "name" in doc]
        if not names:
            return "No students found matching your query."

        joined_names = ", ".join(names[:-1]) + f" and {names[-1]}" if len(names) > 1 else names[0]
        return f"{joined_names}."
    except Exception as e:
        print("Error formatting Solr result:", e)
        return "Error while formatting the response."

# LLaMA chat pipeline

def ask_llama(message, history=None):
    try:
        solr_query = get_solr_query_from_llama(message)
        print("Generated Solr Query:", solr_query)

        # Optionally validate query format
        if ":" not in solr_query or len(solr_query.strip()) < 5:
            return "Invalid query generated. Please rephrase your question."

        solr_docs = search_solr("http://localhost:8983/solr/students", solr_query)
        if not solr_docs:
            return "No data found for your query."

        formatted_response = format_solr_result(solr_docs, message)
        print("Formatted Response:", formatted_response)

        return formatted_response
    except Exception as e:
        print("Error in chat pipeline:", e)
        return "An error occurred while processing your question."

# Solr document updater
def update_student_score(solr_url, student_id, name, subject, score):
    doc = {
        "id": student_id,
        "name": name,
        "subject": subject,
        "score": score
    }
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(f"{solr_url}/update?commit=true", json=[doc], headers=headers)
        print("SOLR update response:", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        print("Error updating Solr:", e)

# Solr search function
def search_solr(solr_url, query):
    try:
        r = requests.get(f"{solr_url}/select", params={"q": query, "wt": "json"})
        r.raise_for_status()
        result = r.json()
        if "response" in result and "docs" in result["response"]:
            return result["response"]["docs"]
        else:
            print("Unexpected Solr response format:", result)
            return []
    except Exception as e:
        print("Solr search error:", e)
        return []

# # Sample data entry(This code neeeds to be execute only one time)
# update_student_score("http://localhost:8983/solr/students", "s123", "Alice", "Math", 88)
# update_student_score("http://localhost:8983/solr/students", "s124", "Jalaj", "Math", 92)
# update_student_score("http://localhost:8983/solr/students", "s125", "Yogesh", "Science", 98)
# update_student_score("http://localhost:8983/solr/students", "s126", "Pankaj", "Math", 95)
# update_student_score("http://localhost:8983/solr/students", "s127", "Manjeet", "Science", 91)
# update_student_score("http://localhost:8983/solr/students", "s128", "Frank", "History", 78)
# update_student_score("http://localhost:8983/solr/students", "s129", "Grace", "Math", 89)
# update_student_score("http://localhost:8983/solr/students", "s130", "bhatt", "Math", 89)


# Main Gradio UI
def main():
    print("Hello from 001-amogh!")
    demo = gr.ChatInterface(
        fn=ask_llama,
        type="messages",
        examples=["Who scored 90 or more in Science?", "List top students in Math."],
        title="LLama Bot!!"
    )
    demo.launch()

if __name__ == "__main__":
    main()

