from aiohttp import request
from flask import Flask, render_template, request, url_for, flash, redirect
from get_hero_data import *
app = Flask(__name__)

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/ID', methods=['POST'])
def find_genes():
    hero_ID = request.form['hero_ID']
    gene_prob, gene_details = get_gene_prob(get_contract(int(hero_ID),rpc_add))
    gene_types = gene_details.keys()
    row_headers = list(gene_details.keys())
    print(row_headers)
    return render_template('index.html', hero_ID=hero_ID, gene_details=gene_details, row_headers=row_headers, gene_types=gene_types)
