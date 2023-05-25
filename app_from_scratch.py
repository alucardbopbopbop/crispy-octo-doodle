import os
import gradio as gr
import openai
import langchain
import nltk
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain 
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

os.environ["OPENAI_API_KEY"] = "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"

cities = ["Seattle", "San Francisco"]

prompt_switch = True

def clear():
    return None, None, None


def pdfsearch(user_text, history, city_inp):

    if city_inp == "Seattle":
        pdf_directory = "/Users/sevancoe/data_sets/test copy"
    elif city_inp == "San Francisco":
        pdf_directory = "/Users/sevancoe/data_sets/San_Francisco"
    else:
        pdf_directory = None

    history = history or []
    
    # history_prompt = the history of the conversation
    history_prompt = list(sum(history, ()))
    history_prompt.append(f"\nHuman: {user_text} ")
    inp = " ".join(history_prompt)

    # keep the history prompt length limited to ~2000 tokens
    inp = " ".join(inp.split()[-2000:])

    # remove duplicate sentences
    sentences = nltk.sent_tokenize(inp)
    sentence_dict = {}
    for i, s in enumerate(sentences):
        if s not in sentence_dict:
            sentence_dict[s] = i

    unique_sentences = [sentences[i] for i in sorted(sentence_dict.values())]
    inp = " ".join(unique_sentences)
    
    # document search and response generation
    embeddings = OpenAIEmbeddings() 
    chain = load_qa_chain(ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2), chain_type="stuff")

    text_splitter = CharacterTextSplitter(        
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,)

    pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

    file_path = ""
    loaders = [] 
    for pdf_name in pdf_files:
        file_path = "{}/{}".format(pdf_directory, pdf_name)
    loader = PyPDFLoader(file_path)
    loaders.append(loader)

    docs = [] 
    for loader in loaders: docs.extend(loader.load()) 
    documents = text_splitter.split_documents(docs) 
    docsearch = FAISS.from_documents(documents, embeddings)
            
    user_input = f"{inp}"

    if prompt_switch == True:
        prompt = f"You are an assistant that answers questions about the codes, permits, regulations, policies, " \
                 f"and laws of the city of {city_inp}."
    else:
        prompt = "hi yves c:"

    print(prompt)

    query = prompt + user_input
    input_documents = docsearch.similarity_search(query) 
    answer = chain.run(input_documents=input_documents, question=query)

    history.append((user_text, answer))

    prompt_switch == False

    return history, history, ""


with gr.Blocks(title = "Chat with housing regulations") as block:
    gr.Markdown("## Chat with (INSERT TITLE)")
    with gr.Row():
        with gr.Column(scale=1):
            city_inp = gr.Dropdown(
                label="City selection",
                choices=cities)

        with gr.Column(scale=5):
            chatbot = gr.Chatbot()
            message = gr.Textbox(placeholder="type pls", label="Type your question here:")
            state = gr.State()

            message.submit(fn=pdfsearch,
                           inputs=[message, state, city_inp],
                           outputs=[chatbot, state, message])
            
            submit = gr.Button("Submit")
            submit.click(fn=pdfsearch,
                         inputs=[message, state, city_inp],
                         outputs=[chatbot, state, message])
            
            clear_btn = gr.Button("Clear chat history")
            clear_btn.click(fn=clear, inputs=None, outputs=[chatbot, state, message])
        
if __name__ == "__main__":
    block.launch(debug=True, inbrowser=True)
