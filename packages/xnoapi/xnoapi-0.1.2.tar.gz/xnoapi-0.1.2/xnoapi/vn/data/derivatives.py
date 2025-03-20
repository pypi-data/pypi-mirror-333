import requests
from xnoapi.vn.data.utils import Config

# Định nghĩa các thành phần public của module
__all__ = ["get_hist"]

# Lấy URL của Lambda function từ Config
LAMBDA_URL = Config.get_link()


def get_hist(symbol: str, frequency: str):
    """
    Get historical data of derivatives VN30F1M and VN30F2M.

    Parameters
    ----------
    symbol : str
        Derivatives symbol (e.g. "VN30F1M", "VN30F2M").
    frequency : str
        Timeframe to get data (e.g. "1D", "1H", "5M").
    Returns
    -------
    dict
        Historical data with information such as time, closing price, trading volume.

    Raises
    ------
    Exception
        If there is an error when calling the API.
    """
    api_key = Config.get_api_key()
    payload = {"symbol": symbol, "frequency": frequency}

    response = requests.post(
        f"{LAMBDA_URL}/data-derivates",
        json=payload,
        headers={"x-api-key": api_key},
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
