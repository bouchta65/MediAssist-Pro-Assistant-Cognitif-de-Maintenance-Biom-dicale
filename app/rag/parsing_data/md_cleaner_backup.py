import unicodedata
import re


def to_lower(text: str) -> str:
    return text.lower()

def replace_apostrophes(text: str) -> str:
    return text.replace("’", "'")

def remove_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))

def normalize(text: str) -> str:
    text = to_lower(text)
    text = replace_apostrophes(text)
    text = remove_accents(text)
    return text



def is_code_fence(line: str) -> bool:
    return line.startswith(("```", "~~~"))

def is_table_line(line: str) -> bool:
    return line.strip().startswith("|")

def is_image_or_link(line: str) -> bool:
    return line.strip().startswith(("![", "["))

def is_superscript(line: str) -> bool:
    return re.match(r"^[¹²³⁴⁵⁶⁷⁸⁹⁰]", line.strip()) is not None


def is_only_number_line(line: str) -> bool:
    return re.fullmatch(r"\d+", line.strip()) is not None

def is_unwanted_header(t: str) -> bool:
    return (
        t.startswith("manuel d'entretien et de maintenance des appareils de laboratoire")
        or t.startswith("chapitre")
        or t.startswith("# chapitre")
        or t.startswith("### photographie")
        or t.startswith("### figure")
        or t.startswith("## guide de depannage")
        or t.startswith("photo")
        or t.startswith("figure ")
        or t.startswith("**figure")
        or t.startswith("la figure")
        or t.startswith("fig. ")
        or t.startswith("no_content_here")
        or t.startswith("(*)")
        or t.startswith("* ")
        or t.startswith("\*")
    )



def toggle_code_block(line: str, inside_code_block: bool) -> bool:
    if is_code_fence(line):
        return not inside_code_block
    return inside_code_block


def update_table_state(line: str, inside_table: bool, cleaned: list) -> bool:

    Handle table state:
    - Start table if line starts with |
    - End table if empty line


    if is_table_line(line):
        if cleaned:
            prev = cleaned[-1].strip()
            if prev.startswith("##") or (prev != "" and "\n" not in prev):
                cleaned.pop()
        return True

    if inside_table and line.strip() == "":
        return False

    return inside_table




def should_skip_line(raw: str, inside_code_block: bool, inside_table: bool) -> bool:
    if inside_code_block:
        return True

    if inside_table:
        return True

    if is_image_or_link(raw):
        return True

    if is_superscript(raw):
        return True

    if is_only_number_line(raw):
        return True

    t = normalize(raw.strip())
    if is_unwanted_header(t):
        return True

    return False



def clean_md_file(md_lines):
    cleaned = []
    inside_code_block = False
    inside_table = False

    for line in md_lines:
        raw = line.lstrip()

        inside_code_block = toggle_code_block(raw, inside_code_block)
        if is_code_fence(raw):
            continue

        inside_table = update_table_state(raw, inside_table, cleaned)
        if is_table_line(raw):
            continue

        if should_skip_line(raw, inside_code_block, inside_table):
            continue

        cleaned.append(line)

    return cleaned



def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def write_file(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)



input_file = "../../../data/output2.md"
output_file = "../../../data/output3.md"

md_lines = read_file(input_file)
cleaned_content = clean_md_file(md_lines)
write_file(output_file, cleaned_content)

