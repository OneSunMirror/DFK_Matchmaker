from asyncio import current_task
from webbrowser import get
from aiohttp import request
from flask import Flask, render_template, request, url_for, flash, redirect
from get_hero_data import *
from pull_hero_list import *
app = Flask(__name__)
if __name__ == "__main__":
        app.run()


temp_hero = get_contract(81781, rpc_add)
gene_prob, gene_details = get_gene_prob(temp_hero)
hero_details = get_other_hero_data(temp_hero)
potential_match = pull_pg_auction(gene_prob, [0], hero_details)
#print(potential_match)

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/ID', methods=['POST'])
def find_genes():
    hero_ID_1 = request.form['hero_ID_1']
    hero_ID_2 = request.form['hero_ID_2']
    hero_1_contract = get_contract(int(hero_ID_1), rpc_add)
    hero_2_contract = get_contract(int(hero_ID_2), rpc_add)
    gene_prob_1, gene_details_1 = get_gene_prob(hero_1_contract)
    gene_prob_2, gene_details_2 = get_gene_prob(hero_2_contract)
    summon_result = calc_likelyhood(gene_prob_1, gene_prob_2)   
    hero_1_details = get_other_hero_data(hero_1_contract)
    potential_match = pull_pg_auction(gene_prob_1, [0], hero_1_details)
    print(summon_result) 
    attributes= ['ID', 'Class', 'Sub Class', 'Rarity', 'Generation', 'Max Summons', 'Summons Left', 'level', 'Price']
    return render_template('index.html', attributes=attributes, hero_ID_1=hero_ID_1, hero_ID_2=hero_ID_2, summon_result=summon_result, gene_details_1=gene_details_1, gene_details_2=gene_details_2)


@app.route('/api/update', methods=['POST'])
def update():
    hero_ID_1 = request.form['hero_ID_1']
    hero_1_contract = get_contract(int(hero_ID_1), rpc_add)
    gene_prob_1, gene_details_1 = get_gene_prob(hero_1_contract)
    hero_1_details = get_other_hero_data(hero_1_contract)
    potential_match, last_update, current_time = pull_pg_auction(gene_prob_1, [0,3,4,5,6], hero_1_details)
    #print(potential_match)
    #print("update")
    res = {}
    res['hero1'] = gene_details_1
    res['matches'] = potential_match
    res['last_update'] = last_update
    res['current_time'] = current_time
    #print(json.dumps(gene_1))
    print(res['hero1'])
    return json.dumps(res)

@app.route('/api/match', methods=['POST'])
def data():
    #hero_ID_2 = json.load(request.get_data('data'))
    hero_IDs = json.loads(request.get_data())  
    hero_2_contract = get_contract(int(hero_IDs['id_2']), rpc_add)
    gene_prob_2, gene_details_2 = get_gene_prob(hero_2_contract)
    hero_1_contract = get_contract(int(hero_IDs['id_1']), rpc_add)
    gene_prob_1, gene_details_1 = get_gene_prob(hero_1_contract)
    summon_result = calc_likelyhood(gene_prob_1, gene_prob_2)
    #print(summon_result)
    #id = request.form['hero_ID_1']
    #id = request.get_data('find_id')
    #print(int(id))
    res = {}
    res['hero2'] = gene_details_2
    res['summon'] = summon_result
    return json.dumps(res)