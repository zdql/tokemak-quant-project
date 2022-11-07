### Tokemak Quant Project

Submission by Ben Reilly

Metrics Used:

|                      Metric                      |
| :----------------------------------------------: |
|  Total Fee Returns Over Time Period (Maximize)   |
|   Impermanent Loss over Time Period (Minimize)   |
| Price Volatility of underlying Assets (Minimize) |
|           Average Swap Size (Maximize)           |
|  Pct. Change in TVL Over Time Period (Maximize)  |

The output table containing the top pools and their associated scores and metrics can be found in pool_results.csv. The submitted pools are over the range of the last 5319 blocks. The top 10 pools are the formal recommendation.

If you wish to re-generate the metrics from a specific starting and optional ending block, you can run the command:

`python3 __init__.py {start block} {OPTIONAL: end_block}`

This will regenerate pool_results.csv.

The methodology to select the pools is the following. Beginning with our master list of pools, we first query for all pools containing WETH, and then query for all pools containing both WETH and one of the top 100 erc20 tokens. This is done due to the computational intensity of making RPC URL calls for the entirety of the pool list, as well as the initial assumption that the top 100 ERC20 tokens minimize the risk of custodying a low-liquidity asset.

With our list of tokens, we then query the historical ethereum price from the start block until now from the Chainlink oracle. We do this initially to save the RPC calls for when examining each token individually.

Finally, the swap and sync events for each pool are examined over the determined block range. From this, the metrics are derived, and are scored based on a simple linear regression that maximizes / minimizes each metric and yields a final score. This provides a list of pools that are optimal for liquidity provision to minimize risk and impermanent loss, and maximize fee returns.

With more time, and a dedicated RPC URL, more pools would be scanned, for a longer duration of blocks. This would increase the size of the sample and increase confidence that we are actually representing the population dynamics. The script is designed in such a way that this RPC URL could be replaced and more blocks could be scanned simply by providing alternative arguments to the function.
