from portfolio_manager.objects.asset import Asset
from constants import ALL_SYMBOLS

unwanted_characters = '\"*$%+\n'

# Parses the CSV file and returns a list of Asset objects
def parse(csv_file):
    assets = []

    # Discard the first line (column headers)
    csv_file.readline()

    # Iterate over asset lines
    for line in csv_file:
        if line == '\n':
            break
        filtered = line.translate({ord(i): None for i in unwanted_characters})
        members = filtered.split(',')
        asset = Asset()

        asset.symbol = members[1]

        if asset.symbol not in ALL_SYMBOLS:
            continue
        
        asset.account_id = members[0]
        asset.description = members[2]
        asset.quantity = float(members[3])
        asset.last_price = __dollar_str_to_cent_int(members[4])
        asset.last_price_change = __dollar_str_to_cent_int(members[5])
        asset.initial_balance = __dollar_str_to_cent_int(members[6])
        asset.todays_gain_cent = __dollar_str_to_cent_int(members[7])
        asset.todays_gain_percent = __dollar_str_to_cent_int(members[8])
        asset.total_gain_cent = __dollar_str_to_cent_int(members[9])
        asset.total_gain_percent = __dollar_str_to_cent_int(members[10])
        asset.cost_basis_share = __dollar_str_to_cent_int(members[11])
        asset.cost_basis_total = __dollar_str_to_cent_int(members[12])
        asset.category = members[13]

        assets.append(asset)
    
    return assets


def __dollar_str_to_cent_int(val):
    try:
        return int(float(val) * 100)
    except ValueError:
        return val
