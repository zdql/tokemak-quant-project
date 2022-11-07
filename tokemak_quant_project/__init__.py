import os
import sys
from dotenv import load_dotenv
from web3 import Web3
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv


# https://github.com/ethers-io/ethers.js/blob/master/packages/providers/src.ts/alchemy-provider.ts#L16-L21
# NOTE: likely to get rate limited
default_provider_url = "https://eth-mainnet.g.alchemy.com/v2/_gg7wSSi0KMBsdKnGVfHDueq6xMB9EkC"
abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

linkabi = '[{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"},{"internalType":"address","name":"_accessController","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"int256","name":"current","type":"int256"},{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"updatedAt","type":"uint256"}],"name":"AnswerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":true,"internalType":"address","name":"startedBy","type":"address"},{"indexed":false,"internalType":"uint256","name":"startedAt","type":"uint256"}],"name":"NewRound","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"accessController","outputs":[{"internalType":"contract AccessControllerInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"aggregator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"}],"name":"confirmAggregator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRound","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"phaseAggregators","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"phaseId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"}],"name":"proposeAggregator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proposedAggregator","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"proposedGetRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proposedLatestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_accessController","type":"address"}],"name":"setController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def transmute_pools(pools):
    ret = []
    for pool in pools:
        obj = [pool[0], pool[1], pool[2], pool[3], pool[4]]
        ret.append(obj)
    return ret


def cleanDF(data):
    df = pd.DataFrame(data)
    df['ethPriceUSD'] = df['ethPriceUSD'] / 10 ** 8
    df['reserve0'] = df['reserve0'] / 10 ** 18
    df['reserve1'] = df['reserve1'] / 10 ** 18
    df['asset1PriceInEth'] = df['reserve1'] / df['reserve0']
    df['assetPriceUSD'] = df['reserve0'] / \
        df['reserve1'] * df['ethPriceUSD']
    df['reserve0USD'] = df['reserve0'] * df['ethPriceUSD']
    df['reserve1USD'] = df['reserve1'] * (df['assetPriceUSD'])
    df['cumulative_swap0_volume'] = df['cumulative_swap0_volume'] / 10 ** 18
    df['cumulative_swap1_volume'] = df['cumulative_swap1_volume'] / 10 ** 18
    df['cumulative_swap0_volumeUSD'] = df['cumulative_swap0_volume'] * \
        df['ethPriceUSD']
    df['cumulative_swap1_volumeUSD'] = df['cumulative_swap1_volume'] * \
        df['assetPriceUSD']
    df['trade_volumeUSD'] = df['cumulative_swap0_volumeUSD'].diff()
    df['TVLUSD'] = df['reserve0USD'] + df['reserve1USD']
    return df

    # Metrics assumes that you invest at the first entry of the df and withdraw at the last entry


def calculate_metrics(df):

    eth_start_price_USD = df['ethPriceUSD'].iloc[0]
    eth_end_price_USD = df['ethPriceUSD'].iloc[-1]

    reserve0_start = df['reserve0'].iloc[0]
    reserve0_end = df['reserve0'].iloc[-1]
    reserve1_start = df['reserve1'].iloc[0]
    reserve1_end = df['reserve1'].iloc[-1]

    constant_product_start = reserve0_start * reserve1_start
    constant_product_end = reserve0_end * reserve1_end

    start_liquidity_eth = np.sqrt(
        constant_product_start / eth_start_price_USD)
    start_liquidity_asset = np.sqrt(
        constant_product_start * eth_start_price_USD)

    end_liquidity_eth = np.sqrt(constant_product_end / eth_end_price_USD)
    end_liquidity_asset = np.sqrt(constant_product_end * eth_end_price_USD)

    impermanent_loss_eth = 2 * np.sqrt(start_liquidity_eth / end_liquidity_eth) / (
        1+start_liquidity_eth / end_liquidity_eth) - 1
    impermanent_loss_asset = 2 * np.sqrt(start_liquidity_asset / end_liquidity_asset) / (
        1+start_liquidity_asset / end_liquidity_asset) - 1
    impermanent_loss = (impermanent_loss_eth + impermanent_loss_asset) / 2
    total_fee_returns = 0.03 * (df['cumulative_swap0_volumeUSD'].iloc[-1])

    eth_price_vol = df['ethPriceUSD'].pct_change().std()

    asset_price_vol = df['assetPriceUSD'].pct_change().std()

    average_swap_size = np.mean(df['trade_volumeUSD'])

    pct_change_in_TVL = (df['TVLUSD'].iloc[-1] -
                         df['TVLUSD'].iloc[0]) / df['TVLUSD'].iloc[0]

    return total_fee_returns, -impermanent_loss, -eth_price_vol, -asset_price_vol, average_swap_size, pct_change_in_TVL


def main(start_block, end_block=None):

    load_dotenv()
    w3 = Web3(Web3.HTTPProvider(
        os.getenv('PROVIDER_URL', default_provider_url)))

    if end_block is None:
        end_block = w3.eth.block_number

    pools = pd.read_csv('../data/uni_v2_sushi_pools.csv')

    top_tokens = pd.read_csv('../data/top_erc20_tokens.csv')

    top_100_tokens_set = list(top_tokens['id'])

    LINKFEED = '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'

    wethPools = pools.loc[pools.token0_symbol == 'WETH'].append(
        pools.loc[pools.token1_symbol == 'WETH'])

    wethPools = wethPools.loc[wethPools.token0_symbol.isin(top_100_tokens_set)].append(
        wethPools.loc[wethPools.token1_symbol.isin(top_100_tokens_set)])

    poolsArray = transmute_pools(np.array(wethPools))

    class PoolScan:

        def __init__(self, pool, pricefeed):
            address, token0, token0_address, token1, token1_address = pool
            self.address = address
            self.contract = w3.eth.contract(
                address=w3.toChecksumAddress(self.address), abi=abi)
            self.token0_address = token0_address
            self.token1_address = token1_address
            self.token0 = token0
            self.token1 = token1
            self.init_block_number = w3.eth.block_number
            self.pricefeed = pricefeed

        def get_chainlink_eth_feed(self, blockNumber):
            return self.pricefeed[blockNumber]

        def track_events_since_block(self, startBlock=None, endBlock=None):
            if startBlock is None:
                startBlock = self.init_block_number - 100000

            if startBlock is None:
                endBlock = startBlock+100
            swap_event_filter = self.contract.events.Swap.createFilter(
                fromBlock=startBlock, toBlock=endBlock)
            sync_event_filter = self.contract.events.Sync.createFilter(
                fromBlock=startBlock, toBlock=endBlock)
            swap_entries = swap_event_filter.get_all_entries()
            sync_entries = sync_event_filter.get_all_entries()

            # Tracked in token0
            cumulative_swap0_volume = 0
            cumulative_swap1_volume = 0

            TimeSteps = []

            for swap, sync in zip(swap_entries, sync_entries):

                cumulative_swap0_volume += swap['args']['amount0In'] + \
                    swap['args']['amount0Out']
                cumulative_swap1_volume += swap['args']['amount1In'] + \
                    swap['args']['amount1Out']

                # so that 0 is always WETH

                if self.token0 == 'WETH':
                    TimeSteps.append({
                        "amount0In": swap['args']['amount0In'],
                        "amount0Out": swap['args']['amount0Out'],
                        "amount1In": swap['args']['amount1In'],
                        "amount1Out": swap['args']['amount1Out'],
                        "cumulative_swap0_volume": cumulative_swap0_volume,
                        "cumulative_swap1_volume": cumulative_swap1_volume,
                        "reserve0": sync['args']['reserve0'],
                        "reserve1": sync['args']['reserve1'],
                        "blockNumber": sync['blockNumber'],
                        "ethPriceUSD": self.get_chainlink_eth_feed(sync['blockNumber'])
                    })
                else:
                    TimeSteps.append({
                        "amount0In": swap['args']['amount1In'],
                        "amount0Out": swap['args']['amount1Out'],
                        "amount1In": swap['args']['amount0In'],
                        "amount1Out": swap['args']['amount0Out'],
                        "cumulative_swap0_volume": cumulative_swap1_volume,
                        "cumulative_swap1_volume": cumulative_swap0_volume,
                        "reserve0": sync['args']['reserve1'],
                        "reserve1": sync['args']['reserve0'],
                        "blockNumber": int(sync['blockNumber']),
                        "ethPriceUSD": self.get_chainlink_eth_feed(sync['blockNumber'])
                    })

            return TimeSteps

    class Scanner:

        def get_token_metrics(self):

            all_timesteps = {}
            token_metrics = {}

            for token in tqdm(self.top_tokens, desc='Scanning Pools'):
                p = PoolScan(token, self.price_feed)
                tracked_events = p.track_events_since_block(
                    self.start_blockNumber, self.current_block)
                if tracked_events != []:
                    timesteps = cleanDF(tracked_events)
                    all_timesteps[(p.token0, p.token1, p.address)] = timesteps
                    token_metrics[(p.token0, p.token1, p.address)
                                  ] = calculate_metrics(timesteps)

            return all_timesteps, token_metrics

        def __init__(self, start_blockNumber, current_block, top_tokens, pricefeed):
            self.current_block = current_block
            self.start_blockNumber = start_blockNumber
            self.price_feed = pricefeed
            self.top_tokens = top_tokens
            self.top_token_timesteps, self.token_metrics = self.get_token_metrics()

    def get_pricefeed(block, current_block):
        contract = w3.eth.contract(
            address=w3.toChecksumAddress(LINKFEED), abi=linkabi)
        pricefeed = {}
        for i in tqdm(range(block, current_block+1), desc='Getting Historical ETH Price'):
            pricefeed[i] = contract.functions.latestAnswer().call(
                block_identifier=i)
        return pricefeed

    pricefeed = get_pricefeed(start_block, end_block)

    scan = Scanner(start_block, end_block, poolsArray, pricefeed)

    def calc_score(args, weights=None, num_metrics=8):
        if weights is None:
            weights = [1/num_metrics for i in range(num_metrics)]

        score = sum([weights[i]*args[i] for i in range(len(args))])
        if np.isnan(score):
            return 0
        else:
            return score

    ls = [(i, calc_score(scan.token_metrics[i]))
          for i in scan.token_metrics.keys()]

    ls.sort(key=lambda a: a[1], reverse=True)

    for i in ls:
        print(i)

    file = open('pool_results.csv', 'w+', newline='')

    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(ls)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Start block argument required")
    elif len(sys.argv) == 3:
        main(int(sys.argv[1]), int(sys.argv[2]))
    else:
        main(int(sys.argv[1]))
