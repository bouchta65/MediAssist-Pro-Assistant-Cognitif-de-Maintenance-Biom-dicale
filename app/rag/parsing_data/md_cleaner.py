import unicodedata
import re


def normalize(text):
    text = text.lower().replace("'", "'")
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def is_skip_line(line):
    s = line.strip()
    t = normalize(s)
    
    if s.startswith(("```", "~~~")):
        return True
    if s.startswith(("![", "[")):
        return True
    if re.match(r"^[¹²³⁴⁵⁶⁷⁸⁹⁰]", s):
        return True
    if re.fullmatch(r"\d+", s):
        return True
    
    unwanted = [
        "manuel d'entretien", "chapitre", "# chapitre", "### photographie",
        "### figure", "## guide de depannage", "photo", "figure ", "**figure",
        "la figure", "fig. ", "no_content_here", "(*)", "* ", "\\*",
        "## tableau", "### tableau"
    ]
    for u in unwanted:
        if t.startswith(u):
            return True
    
    return False


def clean_md_file(md_lines):
    cleaned = []
    inside_table = False
    
    for line in md_lines:
        raw = line.lstrip()
        s = raw.strip()
        
        if s.startswith("|"):
            if not inside_table:
                inside_table = True
                while cleaned:
                    prev = cleaned[-1].strip()
                    if prev == "":
                        cleaned.pop()
                    elif prev.startswith("#"):
                        cleaned.pop()
                        break
                    else:
                        cleaned.pop()
                        break
            continue
        
        if inside_table:
            if s == "":
                inside_table = False
            continue
        
        if is_skip_line(raw):
            continue
        
        cleaned.append(line)
    
    return cleaned


input_file = "../../../data/output2.md"
output_file = "../../../data/output3.md"

with open(input_file, "r", encoding="utf-8") as f:
    md_lines = f.readlines()

cleaned = clean_md_file(md_lines)

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(cleaned)
