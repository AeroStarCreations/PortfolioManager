def format_cents(cents):
    try:
        result = f'${abs(cents/100):,.2f}'
        if cents < 0:
            return f'({result})'
        return result
    except TypeError:
        return str(cents)