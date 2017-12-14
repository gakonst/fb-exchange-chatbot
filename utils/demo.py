import MassAPIBot

# from middleware import pair_formatter

client = MassAPIBot.MassAPIBot(['Bittrex', 'Kraken', 'Gdax'])

coins = client.get_latest_price('ETHBTC', exchanges=['Gdax', 'Bittrex'])
client.arbitrage(coins, 'BTC')

