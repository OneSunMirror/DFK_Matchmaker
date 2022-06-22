from asyncio import current_task
from webbrowser import get
from aiohttp import request
from flask import Flask, render_template, request, url_for, flash, redirect
from get_hero_data import *
from pull_hero_list import *
app = Flask(__name__)
if __name__ == "__main__":
        app.run()


#temp_hero = get_contract(81781, rpc_add)
#gene_prob, gene_details = get_gene_prob(temp_hero)
#hero_details = get_other_hero_data(temp_hero)
#potential_match = pull_pg_auction(gene_prob, [0], hero_details)
#print(potential_match)

@app.route('/')
def init():
    return render_template('index_new.html')
@app.route('/adv')
def adv():
    return render_template('adv.html')

@app.route('/api/update_adv', methods=['POST'])
def update_adv():
    hero_ID_1 = int(json.loads(request.get_data())['id_1'])
    options = json.loads(json.loads(request.get_data())['options'])
    print(options)
    if options['bool_zone'] == False:
        hero_ID_1 = hero_ID_1 +  1000000000000
    #hero_1_contract = get_contract(hero_ID_1, rpc_add)
    #gene_prob_1, gene_details_1 = get_gene_prob(hero_1_contract)
    gene_prob_1, gene_details_1, __ = get_gene_prob_graphql(hero_ID_1)
    if (gene_prob_1 is None):
        print("Not valid hero")
        return json.dumps({'hero_found' : False, "id" : hero_ID_1})
    #hero_1_details, desc = get_other_hero_data(hero_1_contract)
    hero_1_details, desc = get_other_hero_data_graphql(hero_ID_1)
    DATABASE_URL = os.environ['DATABASE_URL']
    sale_match, last_update, current_time, sale_count = get_pg_auction_adv(gene_prob_1, DATABASE_URL, "Sale", [0,1,3,4,5,6], hero_1_details, options)
    DATABASE_URL = os.environ['HEROKU_POSTGRESQL_YELLOW_URL']
    rent_match, last_update, current_time, rent_count = get_pg_auction_adv(gene_prob_1, DATABASE_URL, "Rent", [0,1,3,4,5,6], hero_1_details, options)
    res = {}
    res['hero_found'] = True
    res['hero1'] = gene_details_1
    res['matches'] = sale_match +  rent_match
    res['last_update'] = last_update
    res['current_time'] = current_time
    res['sale_count'] = sale_count
    res['rent_count'] = rent_count
    #print(sale_match)
    print("Finding Match for " + str(hero_ID_1))
    return json.dumps(res)


@app.route('/api/update', methods=['POST'])
def update():
    hero_ID_1 = int(json.loads(request.get_data())['id_1'])
    options = json.loads(json.loads(request.get_data())['options'])
    if options['bool_zone'] == False:
        hero_ID_1 = hero_ID_1 +  1000000000000
    #hero_1_contract = get_contract(hero_ID_1, rpc_add)
    #gene_prob_1, gene_details_1 = get_gene_prob(hero_1_contract)
    gene_prob_1, gene_details_1, __ = get_gene_prob_graphql(hero_ID_1)
    if (gene_prob_1 is None):
        print("Not valid hero")
        return json.dumps({'hero_found' : False, "id" : hero_ID_1})
    #hero_1_details, desc = get_other_hero_data(hero_1_contract)
    hero_1_details, desc = get_other_hero_data_graphql(hero_ID_1)
    DATABASE_URL = os.environ['DATABASE_URL']
    sale_match, last_update, current_time = get_pg_auction(gene_prob_1, DATABASE_URL, "Sale", [0,1,3,4,5,6], hero_1_details, options)
    DATABASE_URL = os.environ['HEROKU_POSTGRESQL_YELLOW_URL']
    rent_match, last_update, current_time = get_pg_auction(gene_prob_1, DATABASE_URL, "Rent", [0,1, 3,4,5,6], hero_1_details, options)
    res = {}
    res['hero_found'] = True
    res['hero1'] = gene_details_1
    res['matches'] = sale_match +  rent_match
    res['last_update'] = last_update
    res['current_time'] = current_time
    #print(sale_match)
    print("Finding Match for " + str(hero_ID_1))
    return json.dumps(res)

@app.route('/api/update_all', methods=['POST'])
def update_all():
    contract_add = json.loads(request.get_data())['contract_add']
    print("Getting Hereos from: ", contract_add)
    res = []
    for ids in  get_users_heroes(contract_add,rpc_add):
        __, desc = get_other_hero_data(get_contract(ids,rpc_add))
        res.append({'id' : ids, 'desc' :desc}) 
    return json.dumps(res)

@app.route('/api/match', methods=['POST'])
def data():
    #hero_ID_2 = json.load(request.get_data('data'))
    hero_IDs = json.loads(request.get_data())  
    id1 = int(hero_IDs['id_1'])
    id2 = int(hero_IDs['id_2'])
    if not hero_IDs['id_2_zone']:
        id2 = id2 + 1000000000000
    if not hero_IDs['id_1_zone']:
        id1 = id1 + 1000000000000
    #hero_2_contract = get_contract(id2, rpc_add)
    #print(hero_2_contract)
    #gene_prob_2, gene_details_2 = get_gene_prob(hero_2_contract)
    gene_prob_2, gene_details_2, __ = get_gene_prob_graphql(id2)
    gene_prob_1, gene_details_1, __ = get_gene_prob_graphql(id1)
    if (gene_prob_2 is None):
        return json.dumps({'valid' : False, "valid_txt" : "invalid Hero ID: " + str(id2)})
    if (gene_prob_1 is None):
        return json.dumps({'valid' : False, "valid_txt" : "invalid Hero ID: " + str(id1)})
    #hero2_details, hero2_text = get_other_hero_data(hero_2_contract)
    hero2_details, hero2_text = get_other_hero_data_graphql(id2)
    print("matching: " + str(id1) + " and " + str(id2))
    #hero_1_contract = get_contract(id1, rpc_add)
    #hero1_details, hero1_text = get_other_hero_data(hero_1_contract)
    hero1_details, hero1_text = get_other_hero_data_graphql(id1)
    #gene_prob_1, gene_details_1 = get_gene_prob(hero_1_contract)
    summon_result = calc_likelyhood_adv(gene_prob_1, gene_prob_2)
    rarity = calc_rarity(hero1_details['rarity_num'], hero2_details['rarity_num'])
    summon_result.append(rarity)
    #print(summon_result)
    #print(summon_result)
    #id = request.form['hero_ID_1']
    #id = request.get_data('find_id')
    #print(int(id))
    res = {}
    res['hero2'] = gene_details_2
    res['hero1'] = gene_details_1
    res['hero1_t'] = hero1_text
    res['hero2_t'] = hero2_text
    res['summon'] = summon_result
    res['valid'], res['valid_txt'] = check_same_parents(id1, hero1_details['summonerId'], hero1_details['assistantId'], id2, hero2_details['summonerId'], hero2_details['assistantId'])
    return json.dumps(res)