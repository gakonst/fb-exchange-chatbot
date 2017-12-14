import itertools
from ast import literal_eval as parse

# Exchange APIs
import krakenex
import gdax as gdax_api
from pykrakenapi import KrakenAPI
from coinmarketcap import Market
from bittrex import Bittrex

class MultiExchangeClient(object):
    def __init__(self, exchanges):
        '''exchanges = comma separated list of exchanges you want to monitor'''
        self.exchanges = [e.lower() for e in exchanges]

        # Depending on which exchanges got included, connect to APIs
        if 'kraken' in self.exchanges:
            self.kraken_api = krakenex.API()
            self.kraken = KrakenAPI(self.kraken_api)
        if 'gdax' in self.exchanges:
            self.gdax = gdax_api.PublicClient()
        if 'bittrex' in self.exchanges:
            self.bittrex = Bittrex(None, None)
        if 'coinmarketcap' in self.exchanges:
            self.coinmarketcap = Market()

    def get_latest_price(self, pair, show_arbitrage=True):
        '''Gief keypair & exchanges, get prices'''
        responses = dict()
        if 'bittrex' in self.exchanges:
            formatted_pair = self._pair_formatter(pair, 'bittrex')
            pair_bittrex = self.bittrex.get_marketsummary(formatted_pair)['result'][0]['Last']
            responses['bittrex'] = pair_bittrex
        if 'gdax' in self.exchanges:
            formatted_pair = self._pair_formatter(pair, 'gdax')
            pair_gdax = parse(self.gdax.get_product_ticker(formatted_pair)['price'])
            responses['gdax'] = pair_gdax
        if 'kraken' in self.exchanges:
            formatted_pair = self._pair_formatter(pair, 'kraken')
            # eth_kraken  = parse(kraken_api.query_public('Ticker?pair=ETHXBT')['result']['XETHXXBT']['a'][0])
            # responses['kraken'] = pair_kraken
        if 'coinmarketcap' in self.exchanges:
            formatted_pair = self._pair_formatter(pair, 'coinmarketcap')
            pair_cmcap = parse(self.coinmarketcap.ticker(formatted_pair)[0]['price_btc'])
            responses['coinmarketcap'] = pair_cmcap

        if show_arbitrage:
            self.arbitrage(responses)
        return responses

    def arbitrage(self, combination_dict):
        result_list = list(map(dict, itertools.combinations( # get all combinations
            combination_dict.items(), 2)))
        max_arbitrage = 0 
        for pair in result_list:
            a,b = pair.values()
            diff = a-b # find differences between each pair
            e1, e2 = list(pair.keys())
            print ('{} has {} BTC arbitrage over {}'.format(e1, diff, e2))


    def _pair_formatter(self, pair, exchange):
        '''Normalizes the pair to match the expected format by the selected exchange API'''
        ETH_BTC = ['BTCETH', 'ETHBTC', 'XBT-ETH', 'BTC-ETH', 'ETH-BTC']
        if pair in ETH_BTC:
            if exchange.lower() == 'bittrex':
                return 'BTC-ETH'
            elif exchange.lower() == 'gdax':
                return 'ETH-BTC'
            elif exchange.lower() == 'kraken':
                return 'ETHXBT'
            elif exchange.lower() == 'coinmarketcap':
                return 'Ethereum'
            else:
                raise ValueError('Exchange not supported')
        else:
            raise ValueError('Pair not supported')


if __name__ == '__main__':
    client = MultiExchangeClient(['Bittrex', 'Kraken', 'Gdax', 'Coinmarketcap'])
    print(client.get_latest_price('ETHBTC'))
