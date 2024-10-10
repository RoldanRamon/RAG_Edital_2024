from chromadb.config import Settings
import chromadb
import os

chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="chroma")
colecoes = chroma_client.list_collections()

# Mostrar os nomes das coleções
if colecoes:
    print("Coleções encontradas:")
    for colecao in colecoes:
        print(colecao.name)
else:
    print("Nenhuma coleção encontrada.")
