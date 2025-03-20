import time
from datetime import datetime
from typing import Dict

import requests
import pandas as pd

from predictoor_data.constants import SUBGRAPH_URL, TIMEFRAME_TO_SECONDS
from predictoor_data.subgraph.contract_address import get_contract_id
from predictoor_data.subgraph.query import _query_subgraph




def _get_predict_slots(
    start_time: datetime,
    end_time: datetime,
    contract_id: str = None,
    batch_size: int = 1000,
) -> Dict[str, dict]:
    """
    Query PredictSlots within a given time range with pagination.

    Args:
        start_time (datetime): Start of the time range
        end_time (datetime): End of the time range
        contract_id (str): Filter by specific predict contract
        batch_size (int): Number of results per query, max 1000

    Returns:
        Dict[str, dict]: The merged query results containing all PredictSlots data
    """
    all_slots = []
    skip = 0

    while True:
        where_conditions = [
            f"slot_gte: {int(start_time.timestamp())}",
            f"slot_lte: {int(end_time.timestamp())}",
            f'predictContract: "{contract_id}"',
            'status: "Paying"',
        ]

        where_clause = ", ".join(where_conditions)

        query = """
        {
            predictSlots(
                where: { %s }
                first: %d
                skip: %d
                orderBy: slot
                orderDirection: asc
            ) {
                id
                slot
                roundSumStakesUp
                roundSumStakes
                predictContract {
                    id
                }
            }
        }
        """ % (
            where_clause,
            batch_size,
            skip,
        )

        result = _query_subgraph(SUBGRAPH_URL, query)

        if not result.get("data", {}).get("predictSlots"):
            break

        slots = result["data"]["predictSlots"]
        all_slots.extend(slots)

        if len(slots) < batch_size:
            break

        skip += batch_size

    return {"data": {"predictSlots": all_slots}}


def get_predict_slots_df(
    start_time: datetime,
    end_time: datetime,
    timeframe: str,
    pair: str,
) -> pd.DataFrame:
    """
    Query PredictSlots within a given time.

    Args:
        start_time (datetime): Start of the time range
        end_time (datetime): End of the time range
        timeframe (str): Timeframe e.g. "5m", "1h"
        pair (str): Pair name e.g. "BTC/USDT"

    Returns:
        df (pd.DataFrame): DataFrame containing the PredictSlots data
    """
    batch_size = 1000
    contract_id = get_contract_id(pair, timeframe)
    result = _get_predict_slots(start_time, end_time, contract_id, batch_size)
    data = []

    seconds_per_epoch = TIMEFRAME_TO_SECONDS[timeframe]

    for slot in result["data"]["predictSlots"]:
        roundSumStakesUp = float(slot["roundSumStakesUp"])
        roundSumStakes = float(slot["roundSumStakes"])
        roundSumStakesDown = roundSumStakes - roundSumStakesUp
        direction = 1 if roundSumStakesUp > roundSumStakesDown else 0
        data.append(
            {
                "slot_start": slot["slot"] - seconds_per_epoch,
                "slot_target": slot["slot"],
                "stake_up": roundSumStakesUp,
                "stake_down": roundSumStakesDown,
                "direction": direction,
            }
        )

    df = pd.DataFrame(data)
    return df