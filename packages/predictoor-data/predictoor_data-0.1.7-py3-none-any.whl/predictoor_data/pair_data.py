from predictoor_data.exceptions import InvalidPairError


PAIR_TIMEFRAME_TO_ADDRESS = {
    "ADA/USDT": {
        "5m": "0x18f54cc21b7a2fdd011bea06bba7801b280e3151",
        "1h": "0xa2d9dbbdf21c30bb3e63d16ba75f644ac11a0cf0"
    },
    "XRP/USDT": {
        "1h": "0x2d8e2267779d27c2b3ed5408408ff15d9f3a3152",
        "5m": "0x55c6c33514f80b51a1f1b63c8ba229feb132cedb"
    },
    "ETH/USDT": {
        "5m": "0x30f1c55e72fe105e4a1fbecdff3145fc14177695",
        "1h": "0xaa6515c138183303b89b98aea756b54f711710c5"
    },
    "BNB/USDT": {
        "5m": "0x31fabe1fc9887af45b77c7d1e13c5133444ebfbd",
        "1h": "0xd41ffee162905b45b65fa6b6e4468599f0490065"
    },
    "SOL/USDT": {
        "5m": "0x3fb744c3702ff2237fc65f261046ead36656f3bc",
        "1h": "0x74a61f733bd9a2ce40d2e39738fe4912925c06dd"
    },
    "BTC/USDT": {
        "1h": "0x8165caab33131a4ddbf7dc79f0a8a4920b0b2553",
        "5m": "0xe66421fd29fc2d27d0724f161f01b8cbdcd69690"
    },
    "DOT/USDT": {
        "1h": "0x93f9d558ccde9ea371a20d36bd3ba58c7218b48f",
        "5m": "0x9c4a2406e5aa0f908d6e816e5318b9fc8a507e1f"
    },
    "LTC/USDT": {
        "5m": "0xb1c55346023dee4d8b0d7b10049f0c8854823766",
        "1h": "0xfa69b2c1224cebb3b6a36fb5b8c3c419afab08dd"
    },
    "DOGE/USDT": {
        "5m": "0xbe09c6e3f2341a79f74898b8d68c4b5818a2d434",
        "1h": "0xf8c34175fc1f1d373ec67c4fd1f1ce57c69c3fb3"
    },
    "TRX/USDT": {
        "1h": "0xd49cbfd694f4556c00023ddd3559c36af3ae0a80",
        "5m": "0xf28c94c55d8c5e1d70ca3a82744225a4f7570b30"
    }
}

def get_pair_address(pair: str, timeframe: str) -> str:
    try:
        return PAIR_TIMEFRAME_TO_ADDRESS[pair][timeframe]
    except KeyError:
        raise InvalidPairError(f"Invalid pair/timeframe combination: {pair}/{timeframe}")