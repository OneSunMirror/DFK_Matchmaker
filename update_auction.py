from pull_hero_list import *
SALE_DATABASE_URL = os.environ['DATABASE_URL']
update_pg_auction(SALE_DATABASE_URL, AUCTIONS_OPEN_GRAPHQL_QUERY_FAST, 'saleAuctions')
RENT_DATABASE_URL = os.environ['HEROKU_POSTGRESQL_YELLOW']
update_pg_auction(RENT_DATABASE_URL, AUCTIONS_OPEN_GRAPHQL_QUERY_FAST_rent, 'assistingAuctions')
