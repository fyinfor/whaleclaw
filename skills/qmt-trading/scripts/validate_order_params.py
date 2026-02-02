#!/usr/bin/env python3
#coding:utf-8
"""
Validate QMT order parameters before placing orders.

This script helps validate passorder() parameters to catch errors before
submitting orders to the QMT platform.
"""

import sys
from typing import Optional, Tuple


def validate_passorder_params(
    opType: int,
    orderType: int,
    accountid: str,
    orderCode: str,
    prType: int,
    price: float,
    volume: int,
    strategyName: str,
    quickTrade: int,
    userOrderId: str,
) -> Tuple[bool, Optional[str]]:
    """
    Validate passorder() parameters.
    
    Returns:
        (is_valid, error_message)
    """
    # Validate opType
    if opType not in [1, 2]:
        return False, f"opType must be 1 (sell) or 2 (buy), got {opType}"
    
    # Validate orderType
    if not isinstance(orderType, int) or orderType < 0:
        return False, f"orderType must be a positive integer, got {orderType}"
    
    # Validate accountid
    if not accountid or not isinstance(accountid, str):
        return False, f"accountid must be a non-empty string, got {accountid}"
    
    # Validate orderCode format (e.g., '000001.SZ', 'cu2403.SF')
    if not orderCode or not isinstance(orderCode, str):
        return False, f"orderCode must be a non-empty string, got {orderCode}"
    
    if '.' not in orderCode:
        return False, f"orderCode must include exchange suffix (e.g., '.SZ', '.SH', '.SF'), got {orderCode}"
    
    # Validate prType
    if not isinstance(prType, int) or prType < 0:
        return False, f"prType must be a non-negative integer, got {prType}"
    
    # Validate price
    if not isinstance(price, (int, float)) or price < 0:
        return False, f"price must be a non-negative number, got {price}"
    
    # Validate volume
    if not isinstance(volume, int) or volume <= 0:
        return False, f"volume must be a positive integer, got {volume}"
    
    # Validate strategyName
    if not strategyName or not isinstance(strategyName, str):
        return False, f"strategyName must be a non-empty string, got {strategyName}"
    
    # Validate quickTrade
    if quickTrade not in [0, 1]:
        return False, f"quickTrade must be 0 or 1, got {quickTrade}"
    
    # Validate userOrderId (can be empty but must be string)
    if not isinstance(userOrderId, str):
        return False, f"userOrderId must be a string, got {userOrderId}"
    
    return True, None


def validate_futures_params(
    stockcode: str,
    amount: int,
    style: Optional[str] = None,
    price: Optional[float] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Validate futures trading function parameters.
    
    Returns:
        (is_valid, error_message)
    """
    # Validate stockcode
    if not stockcode or not isinstance(stockcode, str):
        return False, f"stockcode must be a non-empty string, got {stockcode}"
    
    if '.' not in stockcode:
        return False, f"stockcode must include exchange suffix (e.g., '.IF', '.SF'), got {stockcode}"
    
    # Validate amount
    if not isinstance(amount, int) or amount <= 0:
        return False, f"amount must be a positive integer, got {amount}"
    
    # Validate style if provided
    if style is not None:
        valid_styles = ['LATEST', 'FIX', 'HANG', 'COMPETE', 'MARKET', 'SALE1', 'BUY1']
        if style.upper() not in valid_styles:
            return False, f"style must be one of {valid_styles}, got {style}"
        
        # If style is FIX, price must be provided
        if style.upper() == 'FIX' and price is None:
            return False, "price must be provided when style is 'FIX'"
    
    # Validate price if provided
    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            return False, f"price must be a non-negative number, got {price}"
    
    return True, None


def main():
    """CLI interface for parameter validation."""
    if len(sys.argv) < 2:
        print("Usage: validate_order_params.py <function> [args...]")
        print("\nFunctions:")
        print("  passorder <opType> <orderType> <accountid> <orderCode> <prType> <price> <volume> <strategyName> <quickTrade> <userOrderId>")
        print("  futures <stockcode> <amount> [style] [price]")
        sys.exit(1)
    
    func = sys.argv[1]
    
    if func == "passorder":
        if len(sys.argv) < 12:
            print("Error: passorder requires 10 parameters")
            sys.exit(1)
        
        try:
            opType = int(sys.argv[2])
            orderType = int(sys.argv[3])
            accountid = sys.argv[4]
            orderCode = sys.argv[5]
            prType = int(sys.argv[6])
            price = float(sys.argv[7])
            volume = int(sys.argv[8])
            strategyName = sys.argv[9]
            quickTrade = int(sys.argv[10])
            userOrderId = sys.argv[11]
            
            is_valid, error = validate_passorder_params(
                opType, orderType, accountid, orderCode, prType,
                price, volume, strategyName, quickTrade, userOrderId
            )
            
            if is_valid:
                print("✓ All parameters are valid")
                sys.exit(0)
            else:
                print(f"✗ Validation failed: {error}")
                sys.exit(1)
        except ValueError as e:
            print(f"✗ Invalid parameter type: {e}")
            sys.exit(1)
    
    elif func == "futures":
        if len(sys.argv) < 4:
            print("Error: futures requires at least 2 parameters (stockcode, amount)")
            sys.exit(1)
        
        stockcode = sys.argv[2]
        amount = int(sys.argv[3])
        style = sys.argv[4] if len(sys.argv) > 4 else None
        price = float(sys.argv[5]) if len(sys.argv) > 5 else None
        
        is_valid, error = validate_futures_params(stockcode, amount, style, price)
        
        if is_valid:
            print("✓ All parameters are valid")
            sys.exit(0)
        else:
            print(f"✗ Validation failed: {error}")
            sys.exit(1)
    
    else:
        print(f"Error: Unknown function '{func}'")
        sys.exit(1)


if __name__ == "__main__":
    main()

