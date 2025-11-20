import os, json
import numpy as np
import fitz
from openai import OpenAI

# CHAVE DIRETO NO CÓDIGO POR ENQUANTO 
client = OpenAI(
    api_key="MINHA CHAVE"
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "provas")
INDEX_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
EMB_PATH = os.path.join(INDEX_DIR, "embeddings.npy")
META_PATH = os.path.join(INDEX_DIR, "embeddings_meta.json")

EMB_MODEL = "text-embedding-3-small"


def _pdf_to_text(path: str) -> str:
    doc = fitz.open(path)
    texts = []
    for page in doc:
        texts.append(page.get_text("text"))
    return "\n".join(texts)


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _chunk(text: str, max_chars=1200, overlap=150):
    text = " ".join(text.split())
    chunks = []
    i = 0
    while i < len(text):
        j = min(i + max_chars, len(text))
        chunk = text[i:j]
        chunks.append(chunk)
        if j == len(text):
            break
        i = j - overlap
        if i < 0:
            i = 0
    return chunks


def _embed_texts(texts):
    # OpenAI embeddings retornam "data: [{embedding: [...]}]"
    resp = client.embeddings.create(model=EMB_MODEL, input=texts)
    return np.array([item.embedding for item in resp.data], dtype=np.float32)


def _norm(v):
    n = np.linalg.norm(v, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return v / n


def indexar_provas():
    """
    Lê todos os PDFs/TXTs em data/provas, gera embeddings
    e salva em embeddings.npy + embeddings_meta.json
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    metas = []
    vectors = []

    for fname in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.isfile(fpath):
            continue

        if fname.lower().endswith(".pdf"):
            texto = _pdf_to_text(fpath)
        elif fname.lower().endswith(".txt"):
            texto = _read_text(fpath)
        else:
            continue

        chunks = _chunk(texto)
        BATCH = 64
        for i in range(0, len(chunks), BATCH):
            batch = chunks[i:i + BATCH]
            embs = _embed_texts(batch)
            for k, emb in enumerate(embs):
                metas.append({
                    "arquivo": fname,
                    "chunk_id": i + k,
                    "texto": batch[k]
                })
            vectors.append(embs)

    if not metas:
        raise RuntimeError("Nenhum texto/chunk encontrado em data/provas.")

    M = np.vstack(vectors)
    M = _norm(M)

    np.save(EMB_PATH, M)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)

    return {"total_chunks": len(metas), "arquivos": sorted({m['arquivo'] for m in metas})}


def buscar_similares(query: str, top_k=6):
    """
    Carrega o índice salvo e retorna os chunks mais parecidos com a query.
    """
    if not (os.path.exists(EMB_PATH) and os.path.exists(META_PATH)):
        raise RuntimeError("Índice não encontrado. Rode indexar_provas() primeiro.")

    M = np.load(EMB_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metas = json.load(f)

    q_emb = _embed_texts([query])
    q = q_emb[0] / (np.linalg.norm(q_emb[0]) + 1e-9)

    sims = (M @ q)
    idx = np.argsort(-sims)[:top_k]

    resultados = [{"score": float(sims[i]), "meta": metas[i]} for i in idx]
    return resultados


# TESTE RÁPIDO PELO TERMINAL
if __name__ == "__main__":
    info = indexar_provas()
    print("Indexação concluída:")
    print(info)
