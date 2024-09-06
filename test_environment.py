import sys
import subprocess

def run_test(name, test_func):
    print(f"Testing {name}...", end=" ")
    sys.stdout.flush()
    try:
        test_func()
        print("OK")
    except Exception as e:
        print(f"FAILED: {str(e)}")

def test_crewai():
    from crewai import Agent, Task, Crew

def test_flask():
    from flask import Flask

def test_spacy():
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("This is a test sentence.")
    assert len(doc) > 0

def test_nltk():
    import nltk
    nltk.tokenize.word_tokenize("This is a test sentence.")

def test_numpy():
    import numpy as np
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6

def test_pandas():
    import pandas as pd
    df = pd.DataFrame({'A': [1, 2, 3]})
    assert len(df) == 3

def test_requests():
    import requests
    response = requests.get("https://www.example.com")
    assert response.status_code == 200

def test_openai():
    import openai

def test_docker():
    import docker

def test_psycopg2():
    import psycopg2

def test_elasticsearch():
    from elasticsearch import Elasticsearch

def test_milvus():
    from milvus import default_server

if __name__ == "__main__":
    print("Running environment tests...")
    run_test("CrewAI", test_crewai)
    run_test("Flask", test_flask)
    run_test("spaCy", test_spacy)
    run_test("NLTK", test_nltk)
    run_test("NumPy", test_numpy)
    run_test("Pandas", test_pandas)
    run_test("Requests", test_requests)
    run_test("OpenAI", test_openai)
    run_test("Docker", test_docker)
    run_test("psycopg2", test_psycopg2)
    run_test("Elasticsearch", test_elasticsearch)
    run_test("Milvus", test_milvus)
    print("Environment tests completed.")