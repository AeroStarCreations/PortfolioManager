def format_cents(cents) -> str:
    try:
        result = f'${abs(cents/100):,.2f}'
        if cents < 0:
            return f'({result})'
        return result
    except TypeError:
        return str(cents)
    
def format_dollars(dollars: float) -> str:
    try:
        result = f'${dollars:,.2f}'
        if dollars < 0:
            return f'({result})'
    except TypeError:
        return str(dollars)