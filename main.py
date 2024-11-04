from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from transformers import AutoTokenizer
import torch
import nltk
from nltk.corpus import wordnet
import string
import random
import os
from typing import Optional

nltk.download('wordnet')

app = FastAPI()

# Mount static files for serving HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load tokenizer for text embedding
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return f.read()

@app.post("/upload")
async def upload_file(input_type: str = Form(...), file: UploadFile = File(...)):
    if input_type == "TEXT":
        content = await file.read()
        return {"content": content.decode("utf-8")}
    
    elif input_type in ["AUDIO", "3D"]:
        file_location = f"static/uploads/{file.filename}"
        with open(file_location, "wb") as upload_file:
            upload_file.write(await file.read())
        return {"content": f"File uploaded: {file.filename}"}

    elif input_type == "IMAGE":
        file_location = f"static/uploads/{file.filename}"
        with open(file_location, "wb") as image_file:
            image_file.write(await file.read())
        return {"content": f"/static/uploads/{file.filename}"}  # Return the URL for the image

    return {"content": "Unsupported input type."}

@app.post("/preprocess")
async def preprocess(
    input_type: str = Form(...),
    input_text: str = Form(None),
    pre_process_option: str = Form(None)
):
    if input_type == "TEXT":
        if pre_process_option == "pre-process":
            # Remove unnecessary words and punctuation
            cleaned_text = ''.join([char for char in input_text if char not in string.punctuation])
            cleaned_text = ' '.join([word for word in cleaned_text.split() if len(word) > 2])  # Remove short words
            return {"output": cleaned_text}
        
        elif pre_process_option == "tokenize":
            tokens = tokenizer.tokenize(input_text)
            return {"output": tokens}
        
        elif pre_process_option == "augment":
            words = input_text.split()
            augmented_text = ' '.join(
                [random.choice([word, get_synonym(word)]) for word in words]
            )
            return {"output": augmented_text}
    
    return {"output": "Unsupported input type or processing option."}

def get_synonym(word: str) -> str:
    """Return a synonym for a given word, if available."""
    syns = wordnet.synsets(word)
    if syns:
        return syns[0].lemmas()[0].name()  # Return the first synonym found
    return word  # Return the original word if no synonym is found
