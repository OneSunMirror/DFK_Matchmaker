from aiohttp import request
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def find_genes():
    request.form[hero_ID]        
    return render_template('index.html')