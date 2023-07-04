from objects.balanceable import Balanceable

# Invest in @items so that each item's percent_fill equals @target_percent_fill
# Required: Categories' percent filled should be roughly equal
# Returns: the remainder of @investment_value
def __increase_items_percent_fill(items, target_percent_fill, investment_value):
    if investment_value <= 0:
        return 0
    elif not len(items):
        return investment_value

    cash_needed = sum([item.get_cash_needed_to_reach_percent_fill(target_percent_fill) for item in items])

    if cash_needed <= investment_value:
        for item in items:
            item.invest(item.get_cash_needed_to_reach_percent_fill(target_percent_fill))
        return investment_value - cash_needed
    else:
        total_percentage = sum([item.target_percentage for item in items])
        for item in items:
            item.invest(investment_value * (item.target_percentage / total_percentage))
        return 0

def balanced_invest(balanceable: Balanceable, investment_value):
    remaining_investment_value = investment_value

    deficit_items = balanceable.get_deficit_items()
    deficit_items.sort(key = lambda c: c.get_percent_fill())
    percent_fills = [item.get_percent_fill() for item in deficit_items] + [1]

    # Level the deficits (at the end of this section, all deficit percent fills
    # should equal the max in deficit_items)
    for i in range(len(deficit_items)):
        next_higher_percentage_fill = percent_fills[i+1]
        items_to_invest_in = deficit_items[:i+1]
        remaining_investment_value = __increase_items_percent_fill(items_to_invest_in, next_higher_percentage_fill, remaining_investment_value)

    return investment_value - remaining_investment_value
