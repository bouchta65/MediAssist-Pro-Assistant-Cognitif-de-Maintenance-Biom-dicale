

pdf_path = r"../../data/manuel-d-entretien-et-de-maintenance-des-appareils-de-laboratoire-who-13-69-697e8ecc8fee5375731004.pdf"
md_output = r"../../data/manuel_laboratoire2.md"



from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-UCb0UQ3WUpwZ9IeMLCuAOMnUxGrFEs5MjBiRHeIlBA9RPG3Z",
    result_type="markdown",
    language="fr",
    verbose=True,
    premium_mode=True,
)

documents = parser.load_data(pdf_path)

with open("output.md", "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc.text)  
        f.write("\n\n---\n\n")  

print("Markdown saved to output.md")