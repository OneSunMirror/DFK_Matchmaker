from get_hero_data import *
import requests
from web3 import Web3
AUCTIONS_TOKEN_IDS_GRAPHQL_QUERY_FAST = """
                        query {
                          saleAuctions(orderBy: startedAt, orderDirection: desc, where: {open: true, tokenId_in: %s }) {
                            id
                            tokenId {
                              id
                              generation
                              rarity
                              summons
                              maxSummons
                              summonerId {
                                id
                              }
                              assistantId {
                                id
                              }
                            }
                            startingPrice
                            endingPrice
                            open
                          }
                        }
                        """
AUCTIONS_TOKEN_IDS_GRAPHQL_QUERY = """
                        query {
                          saleAuctions(orderBy: startedAt, orderDirection: desc, where: {open: true, tokenId_in: %s }) {
                            id
                            seller {
                                name
                            }
                            tokenId {
                              id
                              owner {
                                owner
                              }
                              
                              statGenes
                              generation
                              rarity
                              mainClass
                              subClass
                              summons
                              maxSummons
                              summonerId {
                                id
                              }
                              assistantId {
                                id
                              }
                            }
                            startingPrice
                            endingPrice
                            startedAt
                            duration
                            winner {
                              id
                              name
                            }
                            open
                          }
                        }
                        """
AUCTIONS_OPEN_GRAPHQL_QUERY_FAST = """
                        query {
                          saleAuctions(skip: %d, first: %d, orderBy: startedAt, orderDirection: desc, where: {open: true}) {
                            id
                            tokenId {
                              id
                              }
                            open
                          }
                        }
                        """

    
graphql = 'http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5'
SALE_AUCTIONS_CONTRACT_ADDRESS = '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892'
def get_open_auctions(graphql_address, skip=0, count=1000):

    r = requests.post(graphql_address, json={'query': AUCTIONS_OPEN_GRAPHQL_QUERY_FAST % (skip, count)})

    if r.status_code != 200:
        raise Exception("HTTP error " + str(r.status_code) + ": " + r.text)
    data = r.json()
    return data['data']['saleAuctions']

print(get_open_auctions(graphql))