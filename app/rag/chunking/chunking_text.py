import re
import json
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Document_Chunking")


def split_into_pages(text):
    return [p.strip() for p in text.split("\n---\n") if p.strip()]

def split_into_paragraphs(text):
    parts = re.split(r'\n\n+', text.strip())
    return [p.strip() for p in parts if p.strip() and not p.strip().isdigit()]

def split_long_text(text, max_words):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    
    for sentence in sentences:
        if len((current + " " + sentence).split()) > max_words and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current += " " + sentence
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks

def process_buffer(lines, title, subtitle, page, chunk_id, max_words):
    text = "\n".join(lines).strip()
    chunks = []
    
    if not text or text.isdigit():
        return chunks, chunk_id
    
    paragraphs = split_into_paragraphs(text)
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        
        if para.endswith(":"):
            while i + 1 < len(paragraphs):
                next_para = paragraphs[i + 1]
                if len(next_para.split()) > 15:
                    break
                para += "\n" + next_para
                i += 1
        
        if len(para.split()) > max_words:
            parts = split_long_text(para, max_words)
        else:
            parts = [para]
        
        for part in parts:
            chunks.append({
                "chunk_id": chunk_id,
                "title": title,
                "subtitle": subtitle,
                "content": part,
                "page": page
            })
            chunk_id += 1
        
        i += 1
    
    return chunks, chunk_id

def chunk_markdown(text, max_words=220):
    pages = split_into_pages(text)
    all_chunks = []
    chunk_id = 1
    
    for page_num, page in enumerate(pages, start=1):
        lines = page.split("\n")
        title = ""
        subtitle = ""
        buffer = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("## "):
                new_chunks, chunk_id = process_buffer(buffer, title, subtitle, page_num, chunk_id, max_words)
                all_chunks.extend(new_chunks)
                title = line[3:].strip()
                subtitle = ""
                buffer = []
            
            elif line.startswith("### "):
                new_chunks, chunk_id = process_buffer(buffer, title, subtitle, page_num, chunk_id, max_words)
                all_chunks.extend(new_chunks)
                subtitle = line[4:].strip()
                buffer = []
            
            else:
                buffer.append(line)
        
        new_chunks, chunk_id = process_buffer(buffer, title, subtitle, page_num, chunk_id, max_words)
        all_chunks.extend(new_chunks)
    
    return all_chunks

with mlflow.start_run(run_name="chunking_markdown"):
    max_words = 220
    mlflow.log_param("max_words", max_words)
    
    with open("data/output2.md", "r", encoding="utf-8") as f:
        text = f.read()
    
    chunks = chunk_markdown(text, max_words=max_words)
    
    num_chunks = len(chunks)
    num_pages = len(set(c["page"] for c in chunks))
    avg_words_per_chunk = sum(len(c["content"].split()) for c in chunks) / num_chunks
    
    mlflow.log_param("num_chunks", num_chunks)
    mlflow.log_param("num_pages", num_pages)
    mlflow.log_param("avg_words_per_chunk", avg_words_per_chunk)
    
    chunks_file = "data/chunks.json"
    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    mlflow.log_artifact(chunks_file)

print("Done")
