from numpy import NAN
from get_hero_data import *
import requests
import psycopg2
import json
import os
from datetime import datetime
from web3 import Web3
ABI = """
    [
        {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"auctionId","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"AuctionCancelled","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"auctionId","type":"uint256"},{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"startingPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endingPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"duration","type":"uint256"},{"indexed":false,"internalType":"address","name":"winner","type":"address"}],"name":"AuctionCreated","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"auctionId","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalPrice","type":"uint256"},{"indexed":false,"internalType":"address","name":"winner","type":"address"}],"name":"AuctionSuccessful","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},
        {"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},
        {"inputs":[],"name":"BIDDER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"ERC721","outputs":[{"internalType":"contract IERC721Upgradeable","name":"","type":"address"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"MODERATOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"auctionIdOffset","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"auctions","outputs":[{"internalType":"address","name":"seller","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"startingPrice","type":"uint128"},{"internalType":"uint128","name":"endingPrice","type":"uint128"},{"internalType":"uint64","name":"duration","type":"uint64"},{"internalType":"uint64","name":"startedAt","type":"uint64"},{"internalType":"address","name":"winner","type":"address"},{"internalType":"bool","name":"open","type":"bool"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"uint256","name":"_bidAmount","type":"uint256"}],"name":"bid","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"address","name":"_bidder","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"uint256","name":"_bidAmount","type":"uint256"}],"name":"bidFor","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"cancelAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"cancelAuctionWhenPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"uint128","name":"_startingPrice","type":"uint128"},{"internalType":"uint128","name":"_endingPrice","type":"uint128"},{"internalType":"uint64","name":"_duration","type":"uint64"},{"internalType":"address","name":"_winner","type":"address"}],"name":"createAuction","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"getAuction","outputs":[{"components":[{"internalType":"address","name":"seller","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"startingPrice","type":"uint128"},{"internalType":"uint128","name":"endingPrice","type":"uint128"},{"internalType":"uint64","name":"duration","type":"uint64"},{"internalType":"uint64","name":"startedAt","type":"uint64"},{"internalType":"address","name":"winner","type":"address"},{"internalType":"bool","name":"open","type":"bool"}],"internalType":"struct ERC721AuctionBase.Auction","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"getAuctions","outputs":[{"components":[{"internalType":"address","name":"seller","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"startingPrice","type":"uint128"},{"internalType":"uint128","name":"endingPrice","type":"uint128"},{"internalType":"uint64","name":"duration","type":"uint64"},{"internalType":"uint64","name":"startedAt","type":"uint64"},{"internalType":"address","name":"winner","type":"address"},{"internalType":"bool","name":"open","type":"bool"}],"internalType":"struct ERC721AuctionBase.Auction[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"getCurrentPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getUserAuctions","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"address","name":"_landCoreAddress","type":"address"},{"internalType":"address","name":"_jewelTokenAddress","type":"address"},{"internalType":"uint256","name":"_cut","type":"uint256"},{"internalType":"uint256","name":"_auctionIdOffset","type":"uint256"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"isOnAuction","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"jewelToken","outputs":[{"internalType":"contract IJewelToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"maxPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"minPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},
        {"inputs":[],"name":"ownerCut","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"address[]","name":"_feeAddresses","type":"address[]"},{"internalType":"uint256[]","name":"_feePercents","type":"uint256[]"}],"name":"setFees","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"uint256","name":"_min","type":"uint256"},{"internalType":"uint256","name":"_max","type":"uint256"}],"name":"setLimits","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"totalAuctions","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"view","type":"function"},
        {"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"userAuctions","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}
    ]
    
    """
rpc_server = 'https://api.harmony.one'
SALE_AUCTIONS_CONTRACT_ADDRESS = '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892'

def total_auctions(auction_address, rpc_address):
    w3 = Web3(Web3.HTTPProvider(rpc_address))

    auction_contract_address = Web3.toChecksumAddress(auction_address)
    sales_auction_contract = w3.eth.contract(auction_contract_address, abi=ABI)
    return sales_auction_contract.functions.totalAuctions().call()
#print(total_auctions(SALE_AUCTIONS_CONTRACT_ADDRESS,rpc_server))

def is_on_auction(token_id, rpc_address):
    w3 = Web3(Web3.HTTPProvider(rpc_address))

    sales_auction_contract_address = Web3.toChecksumAddress(SALE_AUCTIONS_CONTRACT_ADDRESS)
    sales_auction_contract = w3.eth.contract(sales_auction_contract_address, abi=ABI)
    return sales_auction_contract.functions.isOnAuction(token_id).call()

#for i in range(1, 100000):
#  print(is_on_auction(i,rpc_server))



AUCTIONS_TOKEN_IDS_GRAPHQL_QUERY_FAST = """
                        query {
                          saleAuctions(orderBy: startedAt, orderDirection: desc, where: {open: true, tokenId_in: %s }) {
                            id
                            tokenId {
                              id
                              maxSummons
                            }
                            startingPrice
                            endingPrice
                            open
                          }
                        }
                        """
AUCTIONS_OPEN_GRAPHQL_QUERY_FAST = """
                        query {
                          saleAuctions(first: %d, skip: %d, orderBy: startedAt, orderDirection: asc, where: {open: true}) {
                            id
                            tokenId {
                              id
                              maxSummons
                              statGenes
                              level
                              summons
                              generation
                              rarity
                              mainClass
                              subClass
                              level
                              }
                            startingPrice
                            endingPrice
                            open
                          }
                        }
                        """

AUCTIONS_OPEN_GRAPHQL_QUERY_FAST_rent = """
                        query {
                          assistingAuctions(first: %d, skip: %d, orderBy: startedAt, orderDirection: asc, where: {open: true}) {
                            id
                            tokenId {
                              id
                              maxSummons
                              statGenes
                              level
                              summons
                              generation
                              rarity
                              mainClass
                              subClass
                              level
                              }
                            startingPrice
                            endingPrice
                            open
                          }
                        }
                        """  
graphql = 'https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql'
SALE_AUCTIONS_CONTRACT_ADDRESS = '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892'
def get_open_auctions(graphql_address, GRAPHQL, TYPE, count, skip):

    r = requests.post(graphql_address, json={'query': GRAPHQL % (count, skip)})

    if r.status_code != 200:
        raise Exception("HTTP error " + str(r.status_code) + ": " + r.text)
    data = r.json()
    
    return data['data'][TYPE]

def get_open_rent_auctions(graphql_address, count, skip):

    r = requests.post(graphql_address, json={'query': AUCTIONS_OPEN_GRAPHQL_QUERY_FAST_rent % (count, skip)})
    if r.status_code != 200:
        raise Exception("HTTP error " + str(r.status_code) + ": " + r.text)
    data = r.json()
    return data['data']['assistingAuctions']


def convert_int(in_str):
  if str(in_str).isnumeric():
    return int(in_str)
  else:
    return 0

def manual_auction_pull(TYPE, index, rpc_address):
    if TYPE == "'saleAuctions'":
      auction_address = SALE_AUCTIONS_CONTRACT_ADDRESS
    else:
      auction_address = SALE_AUCTIONS_CONTRACT_ADDRESS
    w3 = Web3(Web3.HTTPProvider(rpc_address))
    auction_contract_address = Web3.toChecksumAddress(auction_address)
    auction_contract = w3.eth.contract(auction_contract_address, abi=ABI)
    return auction_contract.functions.auctions(int(index)).call()

def pull_auction_str(cur, GRAPHQL, TYPE):
  auction_dict  = {}
  print("Getting auction from " + TYPE)
  for i in range(1, 10000, 1000):
    auct_dict = get_open_auctions(graphql, GRAPHQL, TYPE, 1000, i)
    #print(len(auct_dict))
    #print(auct_dict)
    if(len(auct_dict) == 0):
      break
    for auction in auct_dict:
      #print(auction)
      if auction['tokenId'] == None:
        print(auction['id'])
      else: 
        if (int(auction['id']) > 10000000000000):
          auction_in = "Crystal(CV)"
        else:
          auction_in = "Jewel(SD)"
        max_Summons = int(auction['tokenId']['maxSummons']) 
        summons_left = max_Summons - int(auction['tokenId']['summons'])
        if (summons_left != 0):
          hero_id = auction['tokenId']['id']
          if (int(hero_id) >= 1000000000000):
            hero_id = str(int(hero_id) - 1000000000000)
            summoned_from = "CV"
          else:
            summoned_from = "SD"
        #print(auction['tokenId'])
          gene_string = auction['tokenId']['statGenes']
          gene_prob, g_s, filter_string = calc_prob(convert_int(gene_string))
          generation = convert_int(auction['tokenId']['generation'])
          c_rarity = rarity[int(auction['tokenId']['rarity'])]
          mainClass = auction['tokenId']['mainClass']
          subClass = auction['tokenId']['subClass']
          level = int(auction['tokenId']['level'])
          price = float(auction['startingPrice']) / 1000000000000000000
          price = int(price)
          #match_data = get_other_hero_data(get_contract(int(hero_id), rpc_add))
          auction_dict[hero_id] = [hero_id,  max_Summons, summons_left, generation, price, gene_prob.tolist(), mainClass, subClass, level, c_rarity, summoned_from, auction_in, json.dumps(g_s), str(filter_string)]
  #print("Total Auctions " + len(auction_dict))
  auct_str = b', ' .join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in auction_dict.values()) 
  #print(auct_str)
  #print(cur.mogrify("(-1, null, null, null, null, null, " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
  auct_str = auct_str + cur.mogrify(", ('-1', null, null, null, null, null, '" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "', null, null, null, null, null, null, null)")
  return auct_str

#DATABASE_URL = os.environ['DATABASE_URL']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#cur = conn.cursor()
#pull_auction_str(cur)
def auctions(auction_address, index, rpc_address):
    w3 = Web3(Web3.HTTPProvider(rpc_address))

    auction_contract_address = Web3.toChecksumAddress(auction_address)
    sales_auction_contract = w3.eth.contract(auction_contract_address, abi=ABI)
    return sales_auction_contract.functions.auctions(index)

#print(auctions(SALE_AUCTIONS_CONTRACT_ADDRESS, 1, rpc_add))


def update_pg_auction(DATABASE_URL, GRAPHQL, TYPE):
  print(DATABASE_URL)
  #conn = psycopg2.connect(
  #      host="localhost",
  ##      database="Heroes_all",
   #     user="postgres",
   #     password="asdqwe123")
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  cur = conn.cursor()
  auction_str = pull_auction_str(cur, GRAPHQL, TYPE)
  SQL = cur.mogrify('DELETE From heroes')
  cur.execute(SQL)
  conn.commit()
  #print(len(auction_str))
  SQL = cur.mogrify('INSERT INTO heroes (id,  maxsummons, summonsleft, generation, price, gene, mainclass, subclass, level, rarity, summoned_from, auction_in, gene_string, filter_string) VALUES ')  
  SQL = SQL + auction_str
  #print(SQL)
  #SQL = cur.mogrify('Select * From heroes')
  cur.execute(SQL)
  #data = cur.fetchall()
  #print(data)
  conn.commit()
  conn.close()
  return None

def pull_pg_auction(hero_gene, DATABASE_URL, TYPE, search_space, hero_details, options):
  generation = hero_details['generation']
  maxsummons = hero_details['maxsummons']
  summonsleft = maxsummons - hero_details['summons']
  #print(DATABASE_URL)
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  #conn = psycopg2.connect(
  #      host="localhost",
  #      database="Heroes_all",
  #      user="postgres",
  #      password="asdqwe123")
  cur = conn.cursor()
  search_space_txt = ''
  for i in search_space:
    search_space_txt += ', ('
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] > 0.0:
          search_space_txt += '+ gene[%s][%s] * %s * %s' % (i+1, complement_gene[j]+1, hero_gene[i][j], upgrade_chances(j))
    search_space_txt += ')'
  sql_str = 'SELECT id, mainclass, subclass, rarity, generation, maxsummons, summonsleft, level, price, summoned_from, auction_in, gene_string' + search_space_txt + ' FROM Heroes Where ('
  #print(sql_str)
  SQL = cur.mogrify(sql_str)
  for i in search_space:
    #print(hero_gene[i])
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] >= 0.75:
          SQL = SQL + cur.mogrify('gene[%s][%s] >= 0.75', (i+1, complement_gene[j]+1)) + b' OR '
  SQL = SQL[:len(SQL)-3]
  opt = cur.mogrify(") ")
  if options['bool_gen']:
    opt = opt + cur.mogrify('AND generation = %s ', (str(generation)))
  if options['bool_summons']:
    if generation > 0:
      opt = opt + cur.mogrify('AND maxsummons >= %s AND summonsleft >= %s' , (maxsummons, summonsleft))
  #SQL = SQL + cur.mogrify(') AND generation = %s AND maxsummons >= %s AND summonsleft >= %s', (generation, maxsummons, summonsleft ))
  #print(opt)
  SQL = SQL + opt
  cur.execute(SQL)
  data = cur.fetchall()
  #print(data)
  #print(data[1])
  conn.commit()
  SQL = """SELECT mainClass FROM Heroes Where id=-1"""
  cur.execute(SQL)
  last_update = cur.fetchall()
  conn.close()
  if TYPE == 'Sale':
    O_TYPE = 'Rent'
  else:
    O_TYPE = 'Sale'
  matches = []
  #print(len(data))
  for match in data:
    #match_data = get_other_hero_data(get_contract(match[0], rpc_add))
    attributes= ['ID', 'Class', 'Sub Class', 'Rarity', 'Generation', 'Max Summons', 'Summons Left', 'level', TYPE, 'summoned_from', 'auction_in', 'gene_string']
    dict_attri = {attributes[i]: match[i] for i in range(0, 12)}
    dict_attri[O_TYPE] = 'N/A'
    tot_score = 0
    j = 0
    for i in search_space:
      tot_score += match[j+12]
      dict_attri[stat_traits[i] + ' Score'] = round(match[j+12]*100, 2) 
      j += 1
    if dict_attri['Generation'] == 0:
      dict_attri['Summons'] = "N/A Gen 0"
    else:
      dict_attri['Summons'] = str(dict_attri['Summons Left']) + "/" + str(dict_attri['Max Summons']) 
    dict_attri['Average Score'] = round((tot_score) * 100, 2 )
      
    matches.append(dict_attri)
  #print(matches)
  #found_data["data"] = matches
  current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  return matches, last_update, current_time


def get_pg_auction(hero_gene, DATABASE_URL, TYPE, search_space, hero_details, options):
  generation = hero_details['generation']
  maxsummons = hero_details['maxsummons']
  summonsleft = maxsummons - hero_details['summons']
  #print(DATABASE_URL)
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  #conn = psycopg2.connect(
  #      host="localhost",
  #      database="Heroes_all",
  #      user="postgres",
  #      password="asdqwe123")
  cur = conn.cursor()
  search_space_txt = ''
  for i in search_space:
    search_space_txt += ', ('
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] > 0.0:
          search_space_txt += '+ gene[%s][%s] * %s * %s' % (i+1, complement_gene[j]+1, hero_gene[i][j], upgrade_chances(j))
    search_space_txt += ')'
  sql_str = 'SELECT id, mainclass, subclass, rarity, generation, maxsummons, summonsleft, level, price, summoned_from, auction_in, gene_string' + search_space_txt + ' FROM Heroes Where ('
  #print(sql_str)
  SQL = cur.mogrify(sql_str)
  for i in search_space:
    #print(hero_gene[i])
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] >= 0.75:
          SQL = SQL + cur.mogrify('gene[%s][%s] >= 0.75', (i+1, complement_gene[j]+1)) + b' OR '
  SQL = SQL[:len(SQL)-3]
  opt = cur.mogrify(") ")
  if options['bool_gen']:
    opt = opt + cur.mogrify('AND generation = %s ', (str(generation)))
  if options['bool_summons']:
    if generation > 0:
      opt = opt + cur.mogrify('AND maxsummons >= %s AND summonsleft >= %s' , (maxsummons, summonsleft))
  #SQL = SQL + cur.mogrify(') AND generation = %s AND maxsummons >= %s AND summonsleft >= %s', (generation, maxsummons, summonsleft ))
  #print(opt)
  SQL = SQL + opt
  cur.execute(SQL)
  data = cur.fetchall()
  #print(data)
  #print(data[1])
  conn.commit()
  SQL = """SELECT mainClass FROM Heroes Where id=-1"""
  cur.execute(SQL)
  last_update = cur.fetchall()
  conn.close()
  if TYPE == 'Sale':
    O_TYPE = 'Rent'
  else:
    O_TYPE = 'Sale'
  matches = []
  #print(len(data))
  for match in data:
    #match_data = get_other_hero_data(get_contract(match[0], rpc_add))
    attributes= ['ID', 'Class', 'Sub Class', 'Rarity', 'Generation', 'Max Summons', 'Summons Left', 'level', TYPE, 'summoned_from', 'auction_in', 'gene_string']
    dict_attri = {attributes[i]: match[i] for i in range(0, 12)}
    dict_attri[O_TYPE] = 'N/A'
    tot_score = 0
    j = 0
    for i in search_space:
      tot_score += match[j+12]
      dict_attri[stat_traits[i] + ' Score'] = round(match[j+12]*100, 2) 
      j += 1
    if dict_attri['Generation'] == 0:
      dict_attri['Summons'] = "N/A Gen 0"
    else:
      dict_attri['Summons'] = str(dict_attri['Summons Left']) + "/" + str(dict_attri['Max Summons']) 
    dict_attri['Average Score'] = round((tot_score) * 100, 2 )
      
    matches.append(dict_attri)
  #print(matches)
  #found_data["data"] = matches
  current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  return matches, last_update, current_time

def get_pg_auction_adv(hero_gene, DATABASE_URL, TYPE, search_space, hero_details, options):
  generation = hero_details['generation']
  maxsummons = hero_details['maxsummons']
  summonsleft = maxsummons - hero_details['summons']
  #print(DATABASE_URL)
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  #conn = psycopg2.connect(
  #      host="localhost",
  #      database="Heroes_all",
  #      user="postgres",
  #      password="asdqwe123")
  cur = conn.cursor()
  search_space_txt = ''
  for i in search_space:
    search_space_txt += ', ('
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] > 0.0:
          search_space_txt += '+ gene[%s][%s] * %s * %s' % (i+1, complement_gene[j]+1, hero_gene[i][j], upgrade_chances(j))
    search_space_txt += ')'
  sql_str = 'SELECT id, mainclass, subclass, rarity, generation, maxsummons, summonsleft, level, price, summoned_from, auction_in, gene_string, filter_string' + search_space_txt + ' FROM Heroes Where ('
  #print(sql_str)
  SQL = cur.mogrify(sql_str)
  for i in search_space:
    #print(hero_gene[i])
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] >= 0.75:
          SQL = SQL + cur.mogrify('gene[%s][%s] >= 0.75', (i+1, complement_gene[j]+1)) + b' OR '
  SQL = SQL[:len(SQL)-3]
  opt = cur.mogrify(") ")
  if options['bool_gen']:
    opt = opt + cur.mogrify('AND generation = %s ', (str(generation)))
  else:
    opt = opt + cur.mogrify('AND generation BETWEEN %s AND %s ', (str(options['gen_range'][0]),str(options['gen_range'][1])))

  if options['bool_summons']:
    if generation > 0:
      opt = opt + cur.mogrify('AND maxsummons >= %s AND summonsleft >= %s' , (maxsummons, summonsleft))
  else:
    opt = opt + cur.mogrify('AND summonsleft BETWEEN %s AND %s ', (str(options['summon_range'][0]),str(options['summon_range'][1])))
  #SQL = SQL + cur.mogrify(') AND generation = %s AND maxsummons >= %s AND summonsleft >= %s', (generation, maxsummons, summonsleft ))
  #print(opt)
  SQL = SQL + opt
  cur.execute(SQL)
  data = cur.fetchall()
  #print(data)
  #print(data[1])
  conn.commit()
  SQL = """SELECT mainClass FROM Heroes Where id=-1"""
  print("querying DB...")
  cur.execute(SQL)
  print("results returned")
  last_update = cur.fetchall()
  conn.close()
  if TYPE == 'Sale':
    O_TYPE = 'Rent'
  else:
    O_TYPE = 'Sale'
  matches = []
  #print(len(data))
  for match in data:
    #match_data = get_other_hero_data(get_contract(match[0], rpc_add))
    attributes= ['ID', 'Class', 'Sub Class', 'Rarity', 'Generation', 'Max Summons', 'Summons Left', 'level', TYPE, 'summoned_from', 'auction_in', 'gene_string', 'filter_string']
    dict_attri = {attributes[i]: match[i] for i in range(0, 13)}
    dict_attri[O_TYPE] = 'N/A'
    tot_score = 0
    j = 0
    for i in search_space:
      tot_score += match[j+13]
      dict_attri[stat_traits[i] + ' Score'] = round(match[j+13]*100, 2) 
      j += 1
    if dict_attri['Generation'] == 0:
      dict_attri['Summons'] = "N/A Gen 0"
    else:
      dict_attri['Summons'] = str(dict_attri['Summons Left']) + "/" + str(dict_attri['Max Summons']) 
    dict_attri['Average Score'] = round((tot_score) * 100, 2 )
      
    matches.append(dict_attri)
  #print(matches)
  #found_data["data"] = matches
  current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  return matches, last_update, current_time, len(data)



temp_add = "0xA5aed0dA6d7Ae07815b044702179192eAe5e3984"
print(get_users_heroes(temp_add, rpc_add))
#update_pg_auction('postgres://vefofuiocxcndo:45f6fc2db6c7858a26c57daf1a3667cf33c98fbd4f4e95c74a41560fc98ace42@ec2-34-199-200-115.compute-1.amazonaws.com:5432/d8r59mr19penn2'
#, AUCTIONS_OPEN_GRAPHQL_QUERY_FAST, 'saleAuctions')
#update_pg_auction('postgres://jhbxotgrodncau:19489d0f1099927d1ee179fd23b56c8ebf43dfc133e7729479d5ef8051bfb60a@ec2-18-215-96-22.compute-1.amazonaws.com:5432/deknqa8o27d58f'
# , AUCTIONS_OPEN_GRAPHQL_QUERY_FAST_rent, 'assistingAuctions')

#  SQL = cur.mogrify('SELECT * FROM Heroes Where gene[1][1] >= 0.75')
#  cur.execute(SQL)
#  data = cur.fetchall()
#  #print(data[1])
#  conn.commit()
#  conn.close()
#  return data
#contract = get_contract(125323, rpc_add)
#hero_gene, __ = get_gene_prob(contract)
#hero_1_details = get_other_hero_data(contract)
#pull_pg_auction(hero_gene, [0], hero_1_details)
