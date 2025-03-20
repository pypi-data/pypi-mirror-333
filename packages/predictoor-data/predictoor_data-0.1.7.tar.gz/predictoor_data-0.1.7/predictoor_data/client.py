from datetime import datetime
import os
import time
from typing import Tuple, Union, Dict
import pandas as pd

from predictoor_data.contract.feed_contract import FeedContract
from predictoor_data.pair_data import get_pair_address
from predictoor_data.subgraph.historical_data import get_predict_slots_df
from predictoor_data.w3_config.w3_config import get_web3_config
from .exceptions import PredictoorError


class PredictoorClient:
    def __init__(self, private_key: str = None):
        private_key = os.getenv("PREDICTOOR_PRIVATE_KEY", private_key)
        if private_key is not None:
            self.web3_config = get_web3_config(private_key)

    def fetch_historical(
        self,
        start_date: datetime,
        end_date: datetime,
        pair: str,
        timeframe: str
    ) -> pd.DataFrame:
        """
        Fetch historical price data for a trading pair.
        
        Args:
            start_date: Start date for historical data
            end_date: End date for historical data
            pair: Trading pair (e.g., "BTC/USDT")
            timeframe: Time interval (e.g., "5m", "1h", "1d")
        
        Returns:
            DataFrame with historical data
        """
        return get_predict_slots_df(start_date, end_date, timeframe, pair)


    def get_closest_slot(self, timeframe: str) -> int:
        # given a timeframe for example 5m or 1h, return the closest next slot
        # 16:01, 1h -> 17:00 - 13:03, 5m -> 13:05
        timeframe_to_seconds = {
            "5m": 300,
            "1h": 3600,
            "1d": 86400
        }
        current_time = time.time()
        current_time = current_time - current_time % timeframe_to_seconds[timeframe]
        return int(current_time + timeframe_to_seconds[timeframe])

    def _get_prediction_data(
        self,
        pair: str,
        timeframe: str,
        auto_subscribe: bool = False
    ) -> Tuple[int, int]:
        if hasattr(self, "web3_config") is False:
            raise PredictoorError("Private key is not set")
        contract_address = get_pair_address(pair, timeframe)
        feed_contract = FeedContract(self.web3_config, contract_address)

        if not feed_contract.is_valid_subscription():
            if auto_subscribe:
                feed_contract.buy_and_start_subscription(gasLimit=9_000_000)
            else:
                raise PredictoorError("Subscription is not active")

        closest_slot = self.get_closest_slot(timeframe)
        stakeUp, stakeTotal = feed_contract.get_agg_predval(closest_slot)
        stakeUpWei = stakeUp.amt_wei
        stakeDown = (stakeTotal - stakeUp).amt_wei
        return stakeUpWei, stakeDown

    def get_prediction(
        self,
        pair: str,
        timeframe: str
    ) -> Tuple[int, int]:
        """
        Get current prediction for a trading pair.
        
        Args:
            pair: Trading pair (e.g., "BTC/USDT")
            timeframe: Time interval (e.g., "5m", "1h")
        
        Returns:
            Tuple containing:
              0: Amount of OCEAN staked on "up" prediction
              1: Amount of OCEAN staked on "down" prediction
        """
        return self._get_prediction_data(pair, timeframe)
    
    def subscribe_and_get_prediction(
        self,
        pair: str,
        timeframe: str
    ) -> Tuple[int, int]:
        """
        Subscribe to a trading pair and get current prediction.
        
        Args:
            pair: Trading pair (e.g., "BTC/USDT")
            timeframe: Time interval (e.g., "5m", "1h")
        
        Returns:
            Tuple containing:
              0: Amount of OCEAN staked on "up" prediction
              1: Amount of OCEAN staked on "down" prediction
        """
        return self._get_prediction_data(pair, timeframe, auto_subscribe=True)

