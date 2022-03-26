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

def pull_auction_str(cur, GRAPHQL, TYPE):
  auction_dict  = {}
  for i in range(1, 10000, 1000):
    auct_dict = get_open_auctions(graphql, GRAPHQL, TYPE, 1000, i)
    print(len(auct_dict))
    #print(auct_dict)
    if(len(auct_dict) == 0):
      break
    for auction in auct_dict:
      max_Summons = int(auction['tokenId']['maxSummons'])
      summons_left = max_Summons - int(auction['tokenId']['summons'])
      if (summons_left != 0):
        hero_id = auction['tokenId']['id']
        #print(auction['tokenId'])
        gene_prob, __ = calc_prob(convert_int(auction['tokenId']['statGenes']))
        generation = convert_int(auction['tokenId']['generation'])
        c_rarity = rarity[int(auction['tokenId']['rarity'])]
        mainClass = auction['tokenId']['mainClass']
        subClass = auction['tokenId']['subClass']
        level = int(auction['tokenId']['level'])
        price = float(auction['startingPrice']) / 1000000000000000000
        #match_data = get_other_hero_data(get_contract(int(hero_id), rpc_add))
        auction_dict[hero_id] = [hero_id,  max_Summons, summons_left, generation, price, gene_prob.tolist(), mainClass, subClass, level, c_rarity]
    print(len(auction_dict))
  
  
  auct_str = b', ' .join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in auction_dict.values()) 
  #print(auct_str)
  #print(cur.mogrify("(-1, null, null, null, null, null, " + datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
  auct_str = auct_str + cur.mogrify(", ('-1', null, null, null, null, null, '" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "', null, null, null)")
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
  print(len(auction_str))
  SQL = cur.mogrify('INSERT INTO heroes (id,  maxsummons, summonsleft, generation, price, gene, mainclass, subclass, level, rarity) VALUES ')  
  SQL = SQL + auction_str
  #print(SQL)
  #SQL = cur.mogrify('Select * From heroes')
  cur.execute(SQL)
  #data = cur.fetchall()
  #print(data)
  conn.commit()
  conn.close()
  return None
#update_pg_auction()


def pull_pg_auction(hero_gene, DATABASE_URL, TYPE, search_space, hero_details):
  generation = hero_details['generation']
  maxsummons = hero_details['maxsummons']
  summonsleft = maxsummons - hero_details['summons']
  print(DATABASE_URL)
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  #conn = psycopg2.connect(
  #      host="localhost",
  #      database="Heroes_all",
  #      user="postgres",
  #      password="asdqwe123")
  cur = conn.cursor()
  search_space_txt = ''
  for i in search_space:
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] >= 0.75:
          search_space_txt += ', gene[%s][%s]' % (i+1, complement_gene[j]+1)
  sql_str = 'SELECT id, mainclass, subclass, rarity, generation, maxsummons, summonsleft, level, price' + search_space_txt + ' FROM Heroes Where ('
  #print(sql_str)
  SQL = cur.mogrify(sql_str)
  for i in search_space:
    #print(hero_gene[i])
    for j in range(0,len(hero_gene[i])):
        if hero_gene[i][j] >= 0.75:
          SQL = SQL + cur.mogrify('gene[%s][%s] >= 0.75', (i+1, complement_gene[j]+1)) + b' OR '
  SQL = SQL[:len(SQL)-3]
  SQL = SQL + cur.mogrify(') AND generation = %s AND maxsummons >= %s AND summonsleft >= %s', (generation, maxsummons, summonsleft ))
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
    attributes= ['ID', 'Class', 'Sub Class', 'Rarity', 'Generation', 'Max Summons', 'Summons Left', 'level', TYPE]
    dict_attri = {attributes[i]: match[i] for i in range(0, 9)}
    dict_attri[O_TYPE] = 'N/A'
    comb_score = 0
    tot_score = 0
    j = 0
    for i in search_space:
      if i == 0:
        tot_score += match[j+9]
        dict_attri[stat_traits[i] + ' Score'] = match[i+9]
      elif (i >= 3) and (i <= 6):
        comb_score += match[j+9]
      dict_attri['Attrib Score'] = comb_score / 4
      if dict_attri['Summons Left'] < 0:
        dict_attri['Summons'] = "N/A Gen 0"
      else:
        dict_attri['Summons'] = str(dict_attri['Summons Left']) + "/" + str(dict_attri['Max Summons']) 
      dict_attri['Total Score'] = tot_score + comb_score / 4 
      j += 1
    matches.append(dict_attri)
  #print(matches)
  #found_data["data"] = matches
  current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  return matches, last_update, current_time


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
