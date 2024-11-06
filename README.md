# Pre-processing Application

This application provides a web interface for uploading and pre-processing files of various types, specifically designed to handle `TEXT` input with options for pre-processing, tokenization, and augmentation.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [Usage](#usage)
7. [Notes](#notes)

---

## Project Overview

This project consists of a FastAPI backend (`main.py`) and an HTML frontend (`index.html`) that allows users to:
- Upload text files.
- Apply different pre-processing options such as **pre-process**, **tokenize**, and **augment**.
- View the processed results directly on the web interface.

## Features

- **File Upload**: Supports uploading text files (TXT).
- **Pre-Processing Options**: Select different options for handling the text data.
- **Live Results Display**: Shows processed output directly in the browser.

## Prerequisites

- **Python 3.7+**: Ensure Python is installed on your system.
- **FastAPI**: Backend framework to handle the API requests.
- **Uvicorn**: ASGI server to run the FastAPI application.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pre-processing-app.git
   cd pre-processing-app

2. **Install dependencies**:
  -It’s recommended to use a virtual environment.
  ```bash
  python -m venv env
  source env/bin/activate  

- Install required packages.
  ```bash
   pip install fastapi uvicorn

3. **Running the Application**
  ***Start the FastAPI server:***
  ```bash
  uvicorn main:app --reload
***Access the Frontend***  
     -Open the index.html file in your web browser (drag it to the browser or open via file:// URL).
-The frontend connects to the backend API to handle file uploads and display pre-processed results.



