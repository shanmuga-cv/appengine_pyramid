from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def form():
    return "sample web app for autocomplete"
