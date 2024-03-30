# Setting up project

Clone this project and install all requirements using "pip install requirements.txt"
Run the project using "python fast_api.py"
Test the API by going to http://127.0.0.1:8001/docs on your browser

## Functionality

This project consists of 3 API endpoints for the following functions.

  - Query the current price of a specific cryptocurrency 
  - Retrieve historical price data within a user-specified date range. Users should
specify their desired timeframe for this and statistical analyses using start and
end date parameters in their requests, in the “YYYY-MM-DD HH:MM:SS”
format
  - Perform basic statistical analyses on the stored historical data of a specified
cryptocurrency, including:
1. Average of all prices.
2. Median price.
3. Standard deviation.
4. Percentage change
