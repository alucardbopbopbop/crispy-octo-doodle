import os
import gradio as gr
import nltk
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import OnlinePDFLoader

os.environ["OPENAI_API_KEY"] = "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"

#online pdf loader section
OnlinePDFLoader.__name__ = "nomnom"
loader = OnlinePDFLoader("https://www.seattle.gov/DPD/Publications/CAM/cam100.pdf")
data = loader.load()
seattle_text = data[0].page_content
seattle_text.format(filename = "cam100.pdf", page_number = 1)


#loaders = []


#transformer section
with open(seattle_text) as f:
    text = f.read()
    seattle_text = f.read()

text_splitter = CharacterTextSplitter(
    separator = "\\n",
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function = len,)
seattle_text = ['name', seattle_text]
texts = text_splitter.create_documents(seattle_text)
texts[0].name = "temp"

print(texts[0])

#search section
embeddings = OpenAIEmbeddings()
chain = load_qa_chain(ChatOpenAI(model_name = "gpt-3.5-turbo",
                                 temperature = 0.4),
                                 chain_type = "stuff")



pdf_directory = f"{data}"
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

loaders = []
for pdf_name in pdf_files: file_path = "{}/{}".format(pdf_directory, pdf_name)
loader = PyPDFLoader(file_path)
loaders.append(loader)

docs = []
for loader in loaders: docs.extend(loader.load())
documents = text_splitter.split_documents(docs)
docsearch = FAISS.from_documents(documents, embeddings)

user_input = ""

#prompt = ["The year is 2023. You are an assistant that answers questions about the codes, permits, regulations, policies, and laws of the city of Seattle."]

query = user_input
input_documents = docsearch.similarity_search(query)
answer = chain.run(input_documents = input_documents, question = query)