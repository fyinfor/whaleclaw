#!/usr/bin/env python3
#coding:utf-8
"""
Format and display QMT account data in a readable format.

This script helps format the output from get_trade_detail_data() and
other account query functions for easier reading and debugging.
"""

import json
import sys
from typing import Any, Dict, List, Optional


def format_trade_data(data: Any, indent: int = 0) -> str:
    """
    Format trade data from get_trade_detail_data() for display.
    
    Args:
        data: Trade data object (PythonObj from QMT)
        indent: Indentation level
    
    Returns:
        Formatted string representation
    """
    indent_str = "  " * indent
    
    if hasattr(data, '__dict__'):
        # Python object with attributes
        result = []
        for attr in dir(data):
            if not attr.startswith('_'):
                try:
                    value = getattr(data, attr)
                    if not callable(value):
                        result.append(f"{indent_str}{attr}: {value}")
                except:
                    pass
        return "\n".join(result)
    
    elif isinstance(data, dict):
        # Dictionary
        result = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                result.append(f"{indent_str}{key}:")
                result.append(format_trade_data(value, indent + 1))
            else:
                result.append(f"{indent_str}{key}: {value}")
        return "\n".join(result)
    
    elif isinstance(data, list):
        # List
        result = []
        for i, item in enumerate(data):
            result.append(f"{indent_str}[{i}]:")
            result.append(format_trade_data(item, indent + 1))
        return "\n".join(result)
    
    else:
        return f"{indent_str}{data}"


def format_order_info(order: Any) -> str:
    """
    Format order information for display.
    
    Args:
        order: Order object from get_value_by_order_id()
    
    Returns:
        Formatted string
    """
    if hasattr(order, '__dict__'):
        lines = [
            "Order Information:",
            "=" * 50,
        ]
        
        # Common order fields
        fields = [
            'order_id', 'stock_code', 'order_type', 'order_volume',
            'price', 'price_type', 'order_status', 'traded_volume',
            'traded_price', 'order_time', 'strategy_name', 'order_remark'
        ]
        
        for field in fields:
            if hasattr(order, field):
                value = getattr(order, field)
                lines.append(f"{field:20}: {value}")
        
        return "\n".join(lines)
    
    return str(order)


def main():
    """CLI interface for formatting account data."""
    if len(sys.argv) < 2:
        print("Usage: format_account_data.py <command> [input]")
        print("\nCommands:")
        print("  trade <json_file>     - Format trade data from JSON file")
        print("  order <json_file>     - Format order info from JSON file")
        print("  help                  - Show this help message")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "help":
        print(__doc__)
        sys.exit(0)
    
    elif command in ["trade", "order"]:
        if len(sys.argv) < 3:
            print(f"Error: {command} requires an input file")
            sys.exit(1)
        
        input_file = sys.argv[2]
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if command == "trade":
                print(format_trade_data(data))
            elif command == "order":
                print(format_order_info(data))
        except FileNotFoundError:
            print(f"Error: File not found: {input_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()

