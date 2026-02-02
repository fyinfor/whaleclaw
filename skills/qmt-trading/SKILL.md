---
name: qmt-trading
description: "Automated trading operations for XunTou QMT (迅投 QMT) platform. Use when creating, modifying, or executing trading strategies that require: (1) Placing orders (stocks, futures, options), (2) Querying account information and trade history, (3) Managing futures positions (open/close), (4) Margin trading operations, (5) Algorithmic order execution, or any other automated trading tasks on the QMT platform."
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
      },
  }
---

# QMT Trading

Automated trading operations for XunTou QMT (迅投 QMT) platform.

## Authentication

QMT supports two API modes:

**Built-in Python (this skill)**: Runs inside QMT platform, no token required. Account is auto-assigned from strategy config.

**XtQuant API**: External Python library, requires token authentication. Get token from [投研用户中心](https://xuntou.net/#/userInfo) and set via `xtdc.set_token('your_token')`. See [XtQuant examples](https://dict.thinktrader.net/nativeApi/code_examples.html) for external API usage.

## Quick start

QMT strategies use `init()` and `handlebar()` functions:

```python
#coding:gbk

account = "test"  # Auto-assigned in strategy trading interface

def init(ContextInfo):
    pass

def handlebar(ContextInfo):
    passorder(2, 1101, account, '000001.SZ', 14, 0.0, 100,
              'MyStrategy', 1, '备注', ContextInfo)
```

## Helper scripts

Use bundled scripts to validate parameters and format data before submitting orders.

### Validate order parameters

Validate `passorder()` parameters before submitting:

```bash
python {baseDir}/scripts/validate_order_params.py passorder 2 1101 "1000044" "000001.SZ" 14 0.0 100 "MyStrategy" 1 "备注"
```

Validate futures trading parameters:

```bash
python {baseDir}/scripts/validate_order_params.py futures "IF1805.IF" 1 "FIX" 3750
python {baseDir}/scripts/validate_order_params.py futures "IF1805.IF" 1 "LATEST"
```

**When to use**: Before placing orders in production, especially when parameters come from variables or user input.

### Format account data

Format trade data from `get_trade_detail_data()` for readable display:

```bash
# Export data to JSON first (in QMT strategy)
# Then format it:
python {baseDir}/scripts/format_account_data.py trade account_data.json
python {baseDir}/scripts/format_account_data.py order order_info.json
```

**When to use**: When debugging account queries or analyzing order history.

## Order placement

Use `passorder()` for comprehensive order placement:

```python
passorder(
    opType,        # 2=buy, 1=sell
    orderType,     # Order combination method
    accountid,     # Account ID
    orderCode,     # Security code (e.g., '000001.SZ', 'cu2403.SF')
    prType,        # Price type
    price,         # Order price (0 for market order)
    volume,        # Order quantity
    strategyName,  # Strategy identifier
    quickTrade,    # Quick trade flag
    userOrderId,   # User notes
    ContextInfo    # Strategy context (required)
)
```

**Tip**: Validate parameters with `scripts/validate_order_params.py` before submitting in production.

## Account queries

```python
# Account funds and orders
trade_data = get_trade_detail_data(account)

# Historical trades
history_data = get_history_trade_detail_data(account)

# IPO information
ipo_data = get_ipo_data()

# New stock subscription limit
limit = get_new_purchase_limit(account)

# Order details by order ID
order_info = get_value_by_order_id(order_id)
```

**Tip**: Use `scripts/format_account_data.py` to format query results for debugging.

## Futures trading

**Buy operations:**
- `buy_open(stockcode, amount[, style, price], ContextInfo[, accId])` - Buy to open
- `buy_close_tdayfirst(...)` - Buy to close (today first)
- `buy_close_ydayfirst(...)` - Buy to close (yesterday first)

**Sell operations:**
- `sell_open(...)` - Sell to open
- `sell_close_tdayfirst(...)` - Sell to close (today first)
- `sell_close_ydayfirst(...)` - Sell to close (yesterday first)

**Price styles:** `'LATEST'` (default), `'FIX'`, `'HANG'`, `'COMPETE'`, `'MARKET'`, `'SALE1'`, `'BUY1'`

```python
def handlebar(ContextInfo):
    # Buy to open 1 lot at latest price
    buy_open('IF1805.IF', 1, ContextInfo, account)
    
    # Sell to close 2 lots at fixed price
    sell_close_tdayfirst('IF1805.IF', 2, 'fix', 3750, ContextInfo, account)
```

## Margin trading

```python
# Credit account details
credit_info = query_credit_account(account)

# Maximum margin trading volume
max_volume = query_credit_opvolume(account)

# Marginable securities
assure_list = get_assure_contract(account)

# Shortable securities
short_list = get_enable_short_contract(account)

# Margin contracts
unclosed = get_unclosed_compacts(account)
closed = get_closed_compacts(account)
```

## Options trading

```python
# Option underlying positions
option_pos = get_option_subject_position(account)

# Option combination positions
comb_pos = get_comb_option(account)
```

## Order management

- `cancel()` - Cancel order
- `cancel_task()` - Cancel task
- `pause_task()` - Pause task
- `resume_task()` - Resume task

## Algorithmic trading

- `algo_passorder()` - Algorithmic order (order splitting)
- `smart_algo_passorder()` - Smart algorithm (VWAP, etc.)

## Stock basket

```python
# Get stock basket
basket = get_basket(account)

# Set stock basket
set_basket(account, basket_data)
```

## Hong Kong-Shenzhen Connect

```python
# Exchange rate data
rate_data = get_hkt_exchange_rate(account, 'HUGANGTONG')  # or 'SHENGANGTONG'

# Returns: bidReferenceRate, askReferenceRate, dayBuyRiseRate, daySaleRiseRate
```

## Notes

- All trading functions require `ContextInfo` parameter (strategy context object).
- In strategy trading interface, account is auto-assigned from config. In editor mode, set account manually.
- Editor mode orders don't generate actual orders - use for testing only.
- QMT Python scripts typically require `#coding:gbk` encoding declaration.
- `get_debt_contract()` is deprecated - use `get_unclosed_compacts()` and `get_closed_compacts()` instead.

## Documentation

- QMT Trading Functions API: https://dict.thinktrader.net/innerApi/trading_function.html
- XtQuant API Examples (token auth): https://dict.thinktrader.net/nativeApi/code_examples.html
- Token获取: https://xuntou.net/#/userInfo
