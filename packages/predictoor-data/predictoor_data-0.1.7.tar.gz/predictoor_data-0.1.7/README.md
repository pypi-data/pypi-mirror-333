# predictoor-data

Python client for accessing Predictoor data and predictions on Ocean Protocol.

## Installation

Install via pip:

```sh
pip install predictoor-data
```

Or install from source:

```sh
git clone https://github.com/oceanprotocol/predictoor-data
cd predictoor-data
pip install -e .
```

## Quick Start

```python
from predictoor_data import PredictoorClient
from datetime import datetime

# Initialize client
# private key can also be set using PREDICTOOR_PRIVATE_KEY env var
client = PredictoorClient(private_key="your-private-key")  # private_key is optional

# Get current prediction
stake_up, stake_down = client.get_prediction("BTC/USDT", "5m")
print(f"Up stake: {stake_up/1e18} OCEAN")
print(f"Down stake: {stake_down/1e18} OCEAN")

# Fetch historical data
historical_data = client.fetch_historical(
    datetime(2024, 9, 1),
    datetime(2024, 9, 30),
    "BTC/USDT",
    "5m"
)
```

## API Reference

### PredictoorClient

#### Constructor

```python
client = PredictoorClient(private_key=None)
```
- `private_key`: Optional. Your private key for authentication. Can also be set via `PREDICTOOR_PRIVATE_KEY` environment variable.

#### Methods

##### get_prediction(pair: str, timeframe: str) -> Tuple[int, int]
Get current prediction for a trading pair. If the subscription doesn't exist raises an error.

```python
stake_up, stake_down = client.get_prediction("BTC/USDT", "5m")
```

- `pair`: Trading pair (e.g., "BTC/USDT", "ETH/USDT")
- `timeframe`: Time interval ("5m", "1h")
- Returns: Tuple of (stake_up, stake_down) in wei

##### subscribe_and_get_prediction(pair: str, timeframe: str) -> Tuple[int, int]
If the subscription doesn't exist, subscribes to a trading pair and get current prediction.

```python
stake_up, stake_down = client.subscribe_and_get_prediction("BTC/USDT", "5m")
```

##### fetch_historical(start_date: datetime, end_date: datetime, pair: str, timeframe: str) -> pd.DataFrame
Fetch historical prediction data.

```python
df = client.fetch_historical(
    datetime(2023, 1, 1),
    datetime(2023, 1, 31),
    "BTC/USDT",
    "5m"
)
```

Returns DataFrame with columns:
- `slot_start`: Start time of prediction slot
- `slot_target`: Target time for prediction
- `stake_up`: Amount staked on price going up
- `stake_down`: Amount staked on price going down

## Supported Trading Pairs

Check [predictoor.ai](https://predictoor.ai)
