import re
import json


def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_section_title(section: str) -> str:
    match = re.match(r'^## (.+?)$', section, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown"


def extract_subsection_title(section: str) -> str:
    match = re.search(r'^### (.+?)$', section, re.MULTILINE)
    return match.group(1).strip() if match else ""


def get_table_lines(section: str) -> list[str]:
    return [line for line in section.split('\n') if line.strip().startswith('|')]


def get_headers(header_line: str) -> list[str]:
    return [h.strip() for h in header_line.split('|') if h.strip()]


def get_cells(line: str) -> list[str]:
    return [c.strip() for c in line.split('|')[1:-1]]


def is_image_row(cells: list[str]) -> bool:
    return all(re.match(r'!\[.*\]\(.*\)', cell) or not cell for cell in cells)


def is_troubleshooting_table(headers: list[str]) -> bool:
    return len(headers) >= 3 and any(h in ['PROBLÈME', 'CAUSE PROBABLE', 'SOLUTION'] for h in headers)


def create_troubleshooting_chunk(chunk_id: int, section: str, subsection: str, problem: str, cause: str, solution: str) -> dict:
    return {
        "id": f"table_chunk_{chunk_id}",
        "type": "troubleshooting",
        "section": section,
        "subsection": subsection,
        "problem": problem,
        "cause": cause,
        "solution": solution,
        "content": f"Problème: {problem}\nCause probable: {cause}\nSolution: {solution}",
        "metadata": {"source": "tables.md", "category": "dépannage"}
    }


def create_info_chunk(chunk_id: int, section: str, subsection: str, headers: list[str], col1: str, col2: str) -> dict:
    return {
        "id": f"table_chunk_{chunk_id}",
        "type": "info",
        "section": section,
        "subsection": subsection,
        "content": f"{headers[0]}: {col1}\n{headers[1]}: {col2}",
        "metadata": {"source": "tables.md"}
    }


def parse_tables_md(file_path: str) -> list[dict]:
    content = read_file(file_path)
    chunks = []
    chunk_id = 0
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        section_title = extract_section_title(section)
        subsection_title = extract_subsection_title(section)
        table_lines = get_table_lines(section)

        if len(table_lines) < 2:
            continue

        headers = get_headers(table_lines[0])
        data_lines = [line for line in table_lines[1:] if '---' not in line]
        current_problem = ""

        for line in data_lines:
            cells = get_cells(line)

            if len(cells) < 2 or is_image_row(cells):
                continue

            if is_troubleshooting_table(headers):
                problem = cells[0] or current_problem
                cause = cells[1] if len(cells) > 1 else ""
                solution = cells[2] if len(cells) > 2 else ""

                if cells[0]:
                    current_problem = cells[0]

                if cause or solution:
                    chunks.append(create_troubleshooting_chunk(chunk_id, section_title, subsection_title, problem, cause, solution))
                    chunk_id += 1

            elif len(headers) == 2:
                col1 = cells[0] or current_problem
                col2 = cells[1] if len(cells) > 1 else ""

                if cells[0]:
                    current_problem = cells[0]

                if col1 or col2:
                    chunks.append(create_info_chunk(chunk_id, section_title, subsection_title, headers, col1, col2))
                    chunk_id += 1

    return chunks


def save_chunks(chunks: list[dict], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(chunks)} chunks to {output_path}")


input_file = "../../../data/tables.md"
output_file = "../../../data/tables_chunks.json"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

chunks = parse_tables_md(input_file)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

