https://ambiguouserror.github.io/btc/

# BTC/USD Trading Opportunity Identifier with Risk Management

This repository contains a web-based application designed to identify and optimize trading opportunities for BTC/USD using historical data and various technical analysis strategies.

## Project Description
The application allows users to simulate trading strategies on historical BTC/USD data, primarily leveraging a Moving Average Crossover strategy with optional confirmation filters. It provides tools for single strategy simulation, manual optimization, comprehensive strategy optimization, and visualization of classic chart patterns.

## Features
* **Date Range Selection:** Analyze historical data within a specified timeframe.
* **Customizable Strategy Parameters:** Adjust initial investment, tax rate, service fee, and periods for various indicators (Short MA, Long MA, RSI, Bollinger Bands, Volume MA).
* **Optional Filters:** Enable/disable Stop-Loss/Take-Profit, RSI Filter, Bollinger Bands (BB) Filter, and Volume Filter to refine trading signals.
* **Current Strategy Simulation:** Visualize the performance of a single, user-defined strategy with price, MA, RSI, and Volume charts.
* **Fully-Filtered Strategy Simulation:** A direct comparison chart showing the strategy performance with all filters forcibly enabled.
* **Manual Strategy Optimization:** Find the best performing Moving Average combination within user-defined ranges.
* **Comprehensive Strategy Optimization:** An exhaustive search to find the absolute best-performing strategy configuration across all MA periods and 16 possible filter combinations.
* **AI Strategy Analysis:** (When Comprehensive Optimization is complete) Get a qualitative analysis of the optimal strategy's characteristics, strengths, and weaknesses from a generative AI.
* **Trade Log:** Detailed record of all buy and sell transactions for the optimal strategy.
* **Potential Sell Scenarios:** Displays conditions for triggering a sell for any open positions.
* **Chart Pattern Visualization:** Illustrates classic chart patterns like Head and Shoulders, Cup and Handle, Double Top/Bottom, and Triangles.

## How Signals Are Calculated
The model generates buy and sell signals based on a combination of technical indicators and risk management rules:
1.  **Moving Average (MA) Crossover:** A "Golden Cross" (short MA over long MA) is a buy signal; a "Death Cross" (short MA under long MA) is a sell signal.
2.  **Stop-Loss & Take-Profit:** If enabled, positions are automatically sold if the price drops by the Stop-Loss percentage or rises by the Take-Profit percentage from the entry price.
3.  **Optional Confirmation Filters:**
    * **RSI Filter:** For a buy, RSI must be below the overbought level; for a sell, it must be above the oversold level.
    * **Bollinger Bands (BB) Filter:** For a buy, price must be below the middle BB line; for a sell, it must be above.
    * **Volume Filter:** A signal requires volume to be above its recent moving average.

## Usage
To use this application:
1.  Ensure the `index.html` file is in the same directory as the `btc-usd-max.csv` data file.
2.  Open the `index.html` file directly in a web browser.

The application will load historical BTC/USD data and populate default date ranges and strategy parameters. You can then adjust the settings and run simulations or optimizations.

## Optimization
The tool offers two levels of optimization:
* **Manual Strategy Optimization:** Define ranges for Short and Long Moving Average periods. The tool will test every combination within these ranges, applying the filters currently selected in the 'Strategy Parameters' section.
* **Comprehensive Strategy Optimization:** This is an exhaustive search that tests all Short MA periods (2-30) against all longer MA periods (up to 100), and critically, all 16 possible combinations of the filters (SL/TP, RSI, BB, Volume) to find the single best-performing strategy.

## Advanced Analysis: Combining Patterns with Quantitative Signals
The tool provides a section to visualize classic chart patterns. This feature is intended to be used in conjunction with quantitative analysis:
1.  **Visual Identification:** Identify a potential pattern on a live chart.
2.  **Historical Validation:** Use the tool's Date Range Selection to isolate a past instance where a similar pattern occurred.
3.  **Quantitative Analysis:** Run a "Comprehensive Strategy Optimization" for that specific historical timeframe to find the most profitable quantitative signals that worked during that pattern.
4.  **Apply to the Present:** Use the data-backed signals found by the tool as confirmation to enter or exit a trade when a similar pattern forms in live markets.

## License
**Proprietary Software License - All Rights Reserved**

**Copyright (c) 2025 AmbiguousError. All Rights Reserved.**

This software and its associated documentation files (the "Software") are the exclusive property of AmbiguousError.

No part of this Software, including but not limited to its code, documentation, or any derivative works, may be:
* **Used** for any purpose, whether personal or commercial.
* **Reproduced** in any form or by any means.
* **Distributed** to any third party.
* **Modified** or adapted in any way.
* **Sold**, sublicensed, or otherwise transferred.

Any unauthorized use, reproduction, distribution, modification, or sale of this Software is strictly prohibited and may result in legal action.

This license signifies that, by default, **no permissions are granted** for the use, distribution, modification, or sale of this Software without the express prior written consent of AmbiguousError.
