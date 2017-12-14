from utils import MultiExchangeClient

client = MultiExchangeClient.MultiExchangeClient(['Bittrex', 'Kraken', 'Gdax', 'Coinmarketcap'])


print(client.get_latest_price('ETHBTC'))

