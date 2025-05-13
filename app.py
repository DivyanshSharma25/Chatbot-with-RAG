from flask import Flask, render_template, request, jsonify,redirect
import requests,json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from RAG_pipeline import RAG_pipeline
import ollama
import json,os,time
from werkzeug.utils import secure_filename
message_history = []
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
pipeline=None
gotFile=False
# Route for the chatbot UI
@app.route("/")
def index():
        
       
    return render_template("index.html")

# Route to handle chatbot responses
@app.route("/chat", methods=["POST"])
def chat():
   
    user_message = request.json.get("message")
    uploaded=request.json.get("uploaded")
    if not user_message:
        return jsonify({"response": "I didn't understand that. Can you rephrase?"})

    #bot_response = get_response(user_message)
    bot_response = get_response(user_message,uploaded)
    time.sleep(2)
    return jsonify({"response": bot_response})

@app.route("/uploadFile", methods=["POST"])
def uploadFile():
    global pipeline,gotFile
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)
            
            pipeline=RAG_pipeline(upload_path)
            gotFile=True
            
            return f"File {filename} uploaded successfully!"



def get_response(query,uploaded):
    message_history_copy=message_history.copy()
    message_history.append({"role": "user", "content": query})
    print("got file",gotFile)
    if uploaded:
        rag_query = pipeline.get_rag_query(query)
        print("rag_query",rag_query)
        message_history_copy.append({"role": "user", "content": "using this context: "+rag_query+"answer the question: "+query+".give answer using information given in the context only."})
        print(message_history_copy[-1])
    message_history_copy=message_history
    response= ollama.chat(
    model='llama3.1:latest',
    messages=list(message_history_copy),
    )

    print("response",response['message']['content'])
    return response['message']['content']



if __name__ == "__main__":
    pipeline=RAG_pipeline()
    app.run(debug=True)