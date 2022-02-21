from aiohttp import request
from flask import Flask, render_template, request, url_for, flash, redirect
from get_hero_data import *
k
app = Flask(__name__)
if __name__ == "__main__":
        app.run()
@app.route('/')
def init():
    return render_template('index.html')

@app.route('/ID', methods=['POST'])
def find_genes():
    hero_ID_1 = request.form['hero_ID_1']
    hero_ID_2 = request.form['hero_ID_2']
    gene_prob_1, gene_details_1 = get_gene_prob(get_contract(int(hero_ID_1),rpc_add))
    gene_prob_2, gene_details_2 = get_gene_prob(get_contract(int(hero_ID_2),rpc_add))
    summon_result = calc_likelyhood(gene_prob_1, gene_prob_2)   
    print(summon_result) 
    return render_template('index.html', hero_ID_1=hero_ID_1, hero_ID_2=hero_ID_2, summon_result=summon_result, gene_details_1=gene_details_1, gene_details_2=gene_details_2)
g