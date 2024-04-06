import os
from langchain.prompts import ChatPromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "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"

user_input = input("Human: ")

chain = load_qa_chain(ChatOpenAI(model_name = "gpt-4", temperature = 0.3), chain_type = "stuff")

pdf_directory = "/Users/sevancoe/data_sets/interview_transcripts/housing_connector"
#pdf_directory = "/Users/sevancoe/data_sets/interview_transcripts/community_partners"
#pdf_directory = "/Users/sevancoe/data_sets/interview_transcripts/property_partners"


#Prompt

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content = (
                "You are a helpful assistant who searches research interview transcript documents to answer the user's"
                "questions. If the answer is not found in the documents, inform the user that "
                "the answer is not found in the documents. When responding to queries, include the respondent's name."
                ""
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

llm = ChatOpenAI()
llm(chat_template.format_messages(text = "What did respondents say about how they navigate personal bias?"))

#Embeddings & text splitting

embeddings = OpenAIEmbeddings()

# text_splitter = SemanticChunker(
#     OpenAIEmbeddings(), breakpoint_threshold_type="percentile"
# )

text_splitter = CharacterTextSplitter(
   separator = "\n",
   chunk_size = 1000,
   chunk_overlap = 200,
   length_function = len,)

pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

#Loaders & documents

file_path = ""
loaders = []
for pdf_name in pdf_files:
    file_path = "{}/{}".format(pdf_directory, pdf_name)
loader = PyPDFLoader(file_path)
loaders.append(loader)

docs = []
for loader in loaders:
    docs.extend(loader.load())
documents = text_splitter.split_documents(docs)
docsearch = FAISS.from_documents(documents, embeddings)

#Input & output
user_input = f"{user_input}"

query = user_input
input_documents = docsearch.similarity_search(query)
answer = chain.run(input_documents = input_documents, question = query)

print(f"AI: {answer}")