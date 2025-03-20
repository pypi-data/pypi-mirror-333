import os
import json
import logging
from typing import Dict, List, Optional, Union, Any

import requests

# Setup module-level logger with a default handler if none exists.
logger = logging.getLogger(__name__)
if not logger.handlers:
  handler = logging.StreamHandler()
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

class WizzerClient:
  """
  A Python SDK for connecting to the Wizzer's REST API.

  Attributes:
    base_url (str): Base URL of the Wizzer's API server.
    token (str): JWT token for authentication.
    log_level (str): Logging level. Options: "error", "info", "debug".
  """

  def __init__(
    self,
    base_url: Optional[str] = None,
    token: Optional[str] = None,
    log_level: str = "error"  # default only errors
  ):
    # Configure logger based on log_level.
    valid_levels = {"error": logging.ERROR, "info": logging.INFO, "debug": logging.DEBUG}
    if log_level not in valid_levels:
      raise ValueError(f"log_level must be one of {list(valid_levels.keys())}")
    logger.setLevel(valid_levels[log_level])

    self.log_level = log_level
    # System env vars take precedence over .env
    self.base_url = base_url or os.environ.get("WZ__API_BASE_URL")
    self.token = token or os.environ.get("WZ__TOKEN")
    if not self.token:
      raise ValueError("JWT token must be provided as an argument or in .env (WZ__TOKEN)")
    if not self.base_url:
      raise ValueError("Base URL must be provided as an argument or in .env (WZ__API_BASE_URL)")

    # Prepare the authorization header
    self.headers = {
      "Authorization": f"Bearer {self.token}",
      "Content-Type": "application/json"
    }

    logger.debug("Initialized WizzerClient with URL: %s", self.base_url)

  def get_indices(self, trading_symbol: Optional[str] = None, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get list of indices available on the exchange.

    Args:
      trading_symbol (Optional[str]): Filter by specific index symbol.
      exchange (Optional[str]): Filter by specific exchange (NSE, BSE).

    Returns:
      List[Dict[str, Any]]: List of index information.
    """
    endpoint = "/datahub/indices"
    params = {}
    
    if trading_symbol:
      params["tradingSymbol"] = trading_symbol
    if exchange:
      params["exchange"] = exchange

    logger.debug("Fetching indices with params: %s", params)
    response = self._make_request("GET", endpoint, params=params)
    return response

  def get_index_components(self, trading_symbol: str, exchange: str) -> List[Dict[str, Any]]:
    """
    Get list of components (stocks) for a specific index.

    Args:
      trading_symbol (str): Index symbol (e.g., "NIFTY 50").
      exchange (str): Exchange name (NSE, BSE).

    Returns:
       List[Dict[str, Any]]: List of component stocks in the index.
    """
    endpoint = "/datahub/index/components"
    params = {
      "tradingSymbol": trading_symbol,
      "exchange": exchange
    }

    logger.debug("Fetching index components with params: %s", params)
    response = self._make_request("GET", endpoint, params=params)
    return response

  def get_historical_ohlcv(
    self, 
    instruments: List[str], 
    start_date: str, 
    end_date: str, 
    ohlcv: List[str]
  ) -> List[Dict[str, Any]]:
    """
    Get historical OHLCV data for specified instruments.

    Args:
      instruments (List[str]): List of instrument identifiers (e.g., ["NSE:SBIN:3045"]).
      start_date (str): Start date in YYYY-MM-DD format.
      end_date (str): End date in YYYY-MM-DD format.
      ohlcv (List[str]): List of OHLCV fields to retrieve (open, high, low, close, volume).

    Returns:
      List[Dict[str, Any]]: Historical data for requested instruments.
    """
    endpoint = "/datahub/historical/ohlcv"
    data = {
      "instruments": instruments,
      "startDate": start_date,
      "endDate": end_date,
      "ohlcv": ohlcv
    }

    logger.debug("Fetching historical OHLCV with data: %s", data)
    response = self._make_request("POST", endpoint, json=data)
    return response

  def _make_request(
    self, 
    method: str, 
    endpoint: str, 
    params: Optional[Dict[str, str]] = None, 
    json: Optional[Dict[str, Any]] = None
  ) -> Any:
    """
    Make an HTTP request to the DataHub API.

    Args:
      method (str): HTTP method (GET, POST, etc.)
      endpoint (str): API endpoint path.
      params (Optional[Dict[str, str]]): Query parameters for GET requests.
      json (Optional[Dict[str, Any]]): JSON payload for POST requests.

    Returns:
      Any: Parsed JSON response.

    Raises:
      requests.RequestException: If the request fails.
    """
    url = f"{self.base_url}{endpoint}"
    
    try:
      logger.debug("%s request to %s", method, url)
      response = requests.request(
        method=method,
        url=url,
        headers=self.headers,
        params=params,
        json=json
      )
      response.raise_for_status()
      return response.json()
    except requests.RequestException as e:
      logger.error("API request failed: %s", e, exc_info=True)
      if hasattr(e.response, 'text'):
        logger.error("Response content: %s", e.response.text)
      raise