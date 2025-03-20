from predictoor_data.constants import SUBGRAPH_URL, TIMEFRAME_TO_SECONDS
from predictoor_data.subgraph.query import _query_subgraph


def get_contract_id(pair, timeframe) -> str:
    """
    Get the predictoor contract ID for a given pair and timeframe.
    """
    if timeframe not in TIMEFRAME_TO_SECONDS:
        raise ValueError(f"Timeframe {timeframe} not supported")
    seconds_per_epoch = TIMEFRAME_TO_SECONDS[timeframe]

    query = f"""
    {{
        predictContracts(
            where: {{
                token_: {{
                    name: "{pair}"
                }},
                secondsPerEpoch: {seconds_per_epoch}
            }},
            first: 1
        ) {{
            id,
            token {{
                name
            }}
        }}
    }}
    """

    result = _query_subgraph(SUBGRAPH_URL, query)
    if not result.get("data", {}).get("predictContracts"):
        raise ValueError(f"No contract found for {pair} and {timeframe}")
    return result["data"]["predictContracts"][0]["id"]