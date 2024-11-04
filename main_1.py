from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
import nltk
from nltk.corpus import wordnet
import io
import json

app = FastAPI()

# HTML template with radio buttons and file upload
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>File Upload and Processing</title>
    <style>
        .box {
            border: 1px solid black;
            padding: 10px;
            margin: 10px;
            min-height: 200px;
        }
    </style>
</head>
<body>
    <h2>Select File Type:</h2>
    <input type="radio" name="filetype" value="TEXT" checked> TEXT
    <input type="radio" name="filetype" value="IMAGE"> IMAGE 
    <input type="radio" name="filetype" value="AUDIO"> AUDIO
    <input type="radio" name="filetype" value="3D"> 3D
    
    <br><br>
    <input type="file" id="fileUpload">
    <button onclick="uploadFile()">Upload</button>
    
    <div id="textProcessingOptions" style="display:none">
        <h3>Text Processing Options:</h3>
        <input type="radio" name="textprocess" value="tokens"> Get Tokens
        <input type="radio" name="textprocess" value="synonyms"> Replace Synonyms
    </div>
    
    <div class="box" id="inputBox">
        <h3>Input File Content:</h3>
        <div id="inputContent"></div>
    </div>
    
    <div class="box" id="outputBox">
        <h3>Processed Output:</h3>
        <div id="outputContent"></div>
    </div>

    <script>
        // Show text processing options only when TEXT is selected
        document.getElementsByName('filetype').forEach(radio => {
            radio.addEventListener('change', (e) => {
                document.getElementById('textProcessingOptions').style.display = 
                    e.target.value === 'TEXT' ? 'block' : 'none';
            });
        });

        async function uploadFile() {
            const fileInput = document.getElementById('fileUpload');
            const file = fileInput.files[0];
            const fileType = document.querySelector('input[name="filetype"]:checked').value;
            
            if (!file) {
                alert('Please select a file');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);
            formData.append('filetype', fileType);

            if (fileType === 'TEXT') {
                const processType = document.querySelector('input[name="textprocess"]:checked').value;
                formData.append('processtype', processType);
            }

            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            document.getElementById('inputContent').textContent = result.input_content;
            document.getElementById('outputContent').textContent = result.processed_content;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    return html_content

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    filetype: str = Form(...),
    processtype: str = Form(None)
):
    content = await file.read()
    
    if filetype == "TEXT":
        text_content = content.decode()
        
        # Initialize the tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        model = AutoModelForMaskedLM.from_pretrained('bert-base-uncased')
        
        if processtype == "tokens":
            # Tokenize the text
            tokens = tokenizer.tokenize(text_content)
            processed_content = json.dumps(tokens)
            
        elif processtype == "synonyms":
            # Replace some words with synonyms
            nltk.download('wordnet')
            words = text_content.split()
            processed_words = []
            
            for word in words:
                synsets = wordnet.synsets(word)
                if synsets:
                    # Get the first synonym if available
                    lemmas = synsets[0].lemmas()
                    if len(lemmas) > 1:
                        # Use a different synonym than the original word
                        synonym = next((l.name() for l in lemmas if l.name() != word), word)
                        processed_words.append(synonym)
                    else:
                        processed_words.append(word)
                else:
                    processed_words.append(word)
                    
            processed_content = ' '.join(processed_words)
        
        return {
            "input_content": text_content,
            "processed_content": processed_content
        }
        
    else:
        return {
            "input_content": "File uploaded successfully",
            "processed_content": f"Processing for {filetype} files not implemented yet"
        }
