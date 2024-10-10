import fitz  # PyMuPDF
import os

# Caminho do arquivo PDF
caminho_pdf = r"dataprev_edital_0.pdf"

# Obter o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho do arquivo de saída no mesmo diretório do script
caminho_txt = os.path.join(script_dir, 'edital.txt')

# Abrir o arquivo PDF
doc = fitz.open(caminho_pdf)

# Abrir o arquivo de saída para escrita
with open(caminho_txt, 'w', encoding='utf-8') as f:
    # Iterar sobre as páginas do PDF e extrair texto
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Carregar a página
        text = page.get_text()  # Extrair o texto da página
        f.write(f"Texto da página {page_num + 1}:\n{text}\n\n")

print(f"Texto salvo em: {caminho_txt}")