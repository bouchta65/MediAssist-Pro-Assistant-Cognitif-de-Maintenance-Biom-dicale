
def is_unwanted_table(table_text):
    return ("GMDN Code" in table_text or "Code GMDN" in table_text) and \
           ("ECRI Code" in table_text or "Code ECRI" in table_text) and \
           "Dénomination" in table_text


def extract_tables(md_lines):
    result = []
    subtitle = ""
    title = ""
    table = []
    
    for line in md_lines:
        s = line.strip()
        
        if s.startswith("## "):
            subtitle = s[3:].strip()
        elif s.startswith("### "):
            title = s[4:].strip()
        elif s.startswith("|"):
            table.append(s)
        elif table:
            text = "\n".join(table)
            if not is_unwanted_table(text):
                result.append(f"## {subtitle}\n")
                result.append(f"### {title}\n")
                result.extend([t + "\n" for t in table])
                result.append("\n")
            table = []
    
    if table:
        text = "\n".join(table)
        if not is_unwanted_table(text):
            result.append(f"## {subtitle}\n")
            result.append(f"### {title}\n")
            result.extend([t + "\n" for t in table])
    
    return result


input_file = "../../../data/output.md"
output_file = "../../../data/tables.md"

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

tables = extract_tables(lines)

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(tables)

print(f"Extracted tables saved to {output_file}")
