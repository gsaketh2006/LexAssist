import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# load environment variables from .env
load_dotenv()

# API key are read securely from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# initialize embedding model (
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# load FAISS vector database
vectorstore = FAISS.load_local(
    "legal_faiss_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=256
)

# similarity distance cutoff for accepting answers
SIMILARITY_THRESHOLD = 2.3


# prompt to rewrite short or vague legal queries
rewrite_prompt = ChatPromptTemplate.from_template(
    """
You are preparing a search query for legal documents.

Rules:
- Expand acronyms and vague phrases into formal legal language.
- Do NOT invent laws.
- Do NOT answer the question.
- Output only a rewritten search query.

User question:
{question}
"""
)

rewrite_chain = rewrite_prompt | llm | StrOutputParser()


# prompt to dynamically decide how many chunks to retrieve
k_prompt = ChatPromptTemplate.from_template(
    """
Decide how many document chunks are needed to answer the question well.

Question:
{question}

Return ONLY an integer.
"""
)

k_chain = k_prompt | llm | StrOutputParser()


# strict answering prompt to prevent hallucination
answer_prompt = ChatPromptTemplate.from_template(
    """
Use ONLY the provided context.
If the answer is NOT explicitly present, respond EXACTLY with:
I don't know

Context:
{context}

Question:
{question}
"""
)


def run_query(user_question: str):

    # rewrite query only if it is short or vague
    if len(user_question.split()) <= 4:
        retrieval_query = rewrite_chain.invoke(
            {"question": user_question}
        ).strip()
    else:
        retrieval_query = user_question

    # decide how many chunks are required
    try:
        k = int(k_chain.invoke({"question": retrieval_query}).strip())
    except ValueError:
        k = 5

    # keep k within safe bounds
    k = max(1, min(k, 20))

    # retrieve similar chunks from FAISS
    results = vectorstore.similarity_search_with_score(
        retrieval_query,
        k=k
    )

    # if nothing is retrieved, return no answer
    if not results:
        return "I don't know"

    # check similarity scores
    scores = [score for _, score in results]
    if min(scores) > SIMILARITY_THRESHOLD:
        return "I don't know"

    # extracting text from Document objects
    context = "\n\n".join(doc.page_content for doc, _ in results)

    # generating answer using only retrieved context
    rag_chain = (
        {
            "context": lambda _: context,
            "question": RunnablePassthrough()
        }
        | answer_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(user_question)


print("Ask your questions (type 'exit' to quit)\n")

while True:
    q = input(">> ").strip()

    if q.lower() == "exit":
        print("Goodbye 👋")
        break

    if not q:
        continue

    answer = run_query(q)
    print("\nAnswer:\n")
    print(answer)
    print()
