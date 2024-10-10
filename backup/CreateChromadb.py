import chromadb

# Create bank of data and collection artigo, like a table on sql, to save embeedings
chroma_client =  chromadb.Client()
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_or_create_collection(name="artigo")

# Function to separate edital in many words like embeddins
def quebra_texto(texto, pedaco_tamanho=1000, sobrepor=200):
     if pedaco_tamanho <= sobrepor:
          raise ValueError("Pedaco need to be more greather than sobrepor")
     
     pedacos = []
     inicio = 0
     while inicio < len(texto):
          final = inicio + pedaco_tamanho
          pedacos.append(texto[inicio:final])
          if final >= len(texto):
               inicio = len(texto)
          else:
               inicio += pedaco_tamanho - sobrepor

     return pedacos

# Load file edital.txt
with open("edital.txt", "r", encoding= "utf-8") as file:
     texto = file.read()

pedacos = quebra_texto(texto=texto)

for i, pedaco in enumerate(pedacos):
     print(f"pedaco {i+1}:")
     print(pedaco)
     print(len(pedaco))
     print()

     collection.add(documents=pedaco, ids=[str(i)])