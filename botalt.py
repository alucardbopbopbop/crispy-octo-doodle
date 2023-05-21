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
#^^^for doc search section^^^

os.environ["OPENAI_API_KEY"] = "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"

openai_engines = ["text-davinci-003", "code-davinci-002", "text-curie-001"]
prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, "\
         "and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"


def openai_completion(
                      prompt, 
                      openai_token = None, 
                      engine = "text-davinci-003",
                      #temperature = 0.9, 
                      #max_tokens = 150, 
                      #top_p = 1,
                      #frequency_penalty = 0, 
                      #presence_penalty = 0.6, 
                      stop = [" Human:", " AI:"]):
    
    openai.api_key = openai_token
    #^^^if we want the user to use their own key#
    response = openai.Completion.create(
        engine = engine, 
        prompt = prompt, 
        #temperature = temperature,
        #max_tokens = max_tokens, 
        #top_p = top_p, 
        #frequency_penalty s= frequency_penalty,
        #presence_penalty = presence_penalty, 
        stop = stop)
    return response.choices[0].text


def chatgpt3(
        prompt, 
        history, 
        openai_token,
        #engine, 
        #temperature, 
        #max_tokens, 
        #top_p, 
        #frequency_penalty, 
        #presence_penalty,
        ):

    history = history or []
    history_prompt = list(sum(history, ()))
    history_prompt.append(f"\nHuman: {prompt}")
    inp = " ".join(history_prompt)

    # keep the prompt length limited to ~2000 tokens
    inp = " ".join(inp.split()[-2000:])

    # remove duplicate sentences
    sentences = nltk.sent_tokenize(inp)
    sentence_dict = {}
    for i, s in enumerate(sentences):
        if s not in sentence_dict:
            sentence_dict[s] = i

    unique_sentences = [sentences[i] for i in sorted(sentence_dict.values())]
    inp = " ".join(unique_sentences)

    # create the output with openai
    out = openai_completion(
        inp,
        openai_token,
        #engine,
        #temperature,
        #max_tokens,
        #top_p,
        #frequency_penalty,
        #presence_penalty,
    )

    #langchain stuff here
    embeddings = OpenAIEmbeddings() 
    chain = load_qa_chain(ChatOpenAI(model_name = "gpt-3.5-turbo", temperature = 0.4), chain_type = "stuff")

    text_splitter = CharacterTextSplitter(        
                separator = "\n",
                chunk_size = 1000,
                chunk_overlap = 200,
                length_function = len,)

    pdf_directory = "/Users/sevancoe/data_sets/test copy"
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
            
    loaders = [] 
    for pdf_name in pdf_files: file_path = "{}/{}".format(pdf_directory, pdf_name) 
    loader = PyPDFLoader(file_path) 
    loaders.append(loader)

    docs = [] 
    for loader in loaders: docs.extend(loader.load()) 
    documents = text_splitter.split_documents(docs) 
    docsearch = FAISS.from_documents(documents, embeddings)
            
    user_input = f"{out}"

         #prompt = ["The year is 2023. You are an assistant that answers questions about the codes, permits, regulations, policies, and laws of the city of Seattle."]      
            
    query = user_input
    input_documents = docsearch.similarity_search(query) 
    answer = chain.run(input_documents = input_documents, question = query)

    history.append((inp, answer))
    return history, history, ""


with gr.Blocks(title = "Chat with Seattle housing regulations") as block:
    gr.Markdown("## Chat with (INSERT TITLE)")
    with gr.Row():
        with gr.Column(scale = 1):
            openai_token = gr.Textbox(label="OpenAI API Key", value=os.getenv("OPENAI_API_KEY"))
            engine = gr.Dropdown(
                label = "GPT3 Engine",
                choices = openai_engines,
                value = "text-davinci-003",
            )
            #temperature = gr.Slider(label="Temperature", minimum=0, maximum=1, step=0.1, value=0.9)
            #max_tokens = gr.Slider(label="Max Tokens", minimum=10, maximum=400, step=10, value=150)
            #top_p = gr.Slider(label="Top P", minimum=0, maximum=1, step=0.1, value=1)
            #frequency_penalty = gr.Slider(
            #     label = "Frequency Penalty",
            #     minimum = 0,
            #     maximum = 1,
            #     step = 0.1,
            #     value = 0,
            # )
            # presence_penalty = gr.Slider(
            #     label = "Presence Penalty",
            #     minimum = 0,
            #     maximum = 1,
            #     step = 0.1,
            #     value = 0.6,
            #)

        with gr.Column(scale = 4):
            chatbot = gr.Chatbot()
            message = gr.Textbox(placeholder = prompt, label = "Type your question here:")
            state = gr.State()
            
            clear = gr.Button("Clear")
            clear.click(
                chatgpt3,
                inputs=[
                    message,
                    state,
                    openai_token,
                    #engine,
                    #temperature,
                    #max_tokens,
                    #top_p,
                    #frequency_penalty,
                    #presence_penalty,
                ],
                outputs=[chatbot, state, message],
            )
            
            message.submit(
                fn = chatgpt3,
                #^^^langchain here^^^#
                inputs = [
                    message,
                    state,
                    openai_token,
                    #engine,
                    #temperature,
                    #max_tokens,
                    #top_p,
                    #frequency_penalty,
                    #presence_penalty,
                ],
                outputs=[chatbot, state, message],
            )
            submit = gr.Button("Submit")
            submit.click(
                chatgpt3,
                inputs=[
                    message,
                    state,
                    openai_token,
                    #engine,
                    #temperature,
                    #max_tokens,
                    #top_p,
                    #frequency_penalty,
                    #presence_penalty,
                ],
                outputs=[chatbot, state, message],
            )

if __name__ == "__main__":
    block.launch(debug = True)

# embeddings = OpenAIEmbeddings() 
#        chain = load_qa_chain(ChatOpenAI(model_name = "gpt-3.5-turbo", temperature = 0.4), chain_type = "stuff")

#        text_splitter = CharacterTextSplitter(        
#            separator = "\n",
#            chunk_size = 1000,
#            chunk_overlap = 200,
#            length_function = len,)

#         pdf_directory = "/Users/sevancoe/data_sets/sea_bld_tips"
#         pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
            
#         loaders = [] 
#         for pdf_name in pdf_files: file_path = "{}/{}".format(pdf_directory, pdf_name) 
#         loader = PyPDFLoader(file_path) 
#         loaders.append(loader)

#         docs = [] 
#         for loader in loaders: docs.extend(loader.load()) 
#         documents = text_splitter.split_documents(docs) 
#         docsearch = FAISS.from_documents(documents, embeddings)
            
#         user_input = f"{user('', )}"

#         #prompt = ["The year is 2023. You are an assistant that answers questions about the codes, permits, regulations, policies, and laws of the city of Seattle."]      
            
#         query = user_input
#         input_documents = docsearch.similarity_search(query) 
#         answer = chain.run(input_documents = input_documents, question = query)