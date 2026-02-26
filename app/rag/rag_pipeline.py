import ollama
from retriever import hybrid_search
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("RAG_Pipeline")

SYSTEM_PROMPT = """Tu es MediAssist. Tu dois répondre UNIQUEMENT avec les informations du CONTEXTE ci-dessous.

RÈGLES ABSOLUES:
1. UTILISE UNIQUEMENT le texte du CONTEXTE - AUCUNE créativité, AUCUNE invention
2. NE JAMAIS ajouter d'informations qui ne sont pas dans le contexte
3. NE JAMAIS utiliser tes connaissances générales
4. CITE ou REFORMULE exactement ce qui est écrit dans le contexte
5. Si plusieurs informations sont pertinentes, LISTE-LES TOUTES
6. Si l'information n'est PAS dans le contexte: "Cette information n'est pas disponible dans ma documentation."

CONTEXTE (5 documents trouvés - utilise TOUS ceux qui sont pertinents):
{context}

Question: {question}

Tu dois répondre en utilisant UNIQUEMENT les informations présentes dans la section CONTEXTE ci-dessous.

❗ Interdiction d’utiliser tes connaissances personnelles.
❗ Interdiction d’ajouter des informations externes.
❗ Interdiction de faire des suppositions.
❗ Interdiction de compléter des informations manquantes.

La réponse doit être rédigée sous forme de texte fluide et naturel, comme si elle venait d’un assistant intelligent.

Commence toujours par :
"Bonjour 👋, voici ce que j’ai trouvé pour vous :"

Ensuite :

Reformule les informations du contexte de manière claire et structurée.

Utilise un ton professionnel et amical.

Intègre naturellement les informations au lieu de faire une simple liste brute.

Ensuite, rédige uniquement les informations disponibles dans le contexte, en copiant ou reformulant strictement ce qui est écrit.

⚠️ Ne jamais ajouter d’exemples, de causes possibles, ni de recommandations personnelles."""

LLM_CONFIG = {
    "model": "llama3",
    "temperature": 0.1,
    "top_p": 0.9,
    "top_k": 40,
    "num_predict": 200
}

def generate(question, k=5):
    chunks = hybrid_search(question, k)
    context = "\n\n---\n\n".join([c["content"] for c in chunks])
    
    with mlflow.start_run(run_name="llm_generation"):

        mlflow.log_param("query", question)
        mlflow.log_param("num_chunks", len(chunks))
        mlflow.log_param("k", k)
        
        for key, value in LLM_CONFIG.items():
            mlflow.log_param(key, value)
        
        for i, c in enumerate(chunks):
            mlflow.log_text(
                f"Score: {c['score']:.3f}\nContent:\n{c['content']}",
                f"chunk_{i+1}_id_{c['id']}.txt"
            )
        
        response = ollama.chat(
            model=LLM_CONFIG["model"],
            messages=[{"role": "user", "content": SYSTEM_PROMPT.format(context=context, question=question)}],
            options=LLM_CONFIG
        )
        
        answer = response["message"]["content"]
        
        mlflow.log_text(answer, "final_answer.txt")
    
    return answer

question = "what is my name"
print(f"Question: {question}\n")
print("Réponse:", generate(question))
