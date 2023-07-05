from .objects.asset import Asset
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

        asset.symbol = members[2]

        if asset.symbol not in ALL_SYMBOLS:
            continue
        
        asset.account_id = members[0]
        asset.description = members[3]
        asset.quantity = float(members[4])
        asset.last_price = __dollar_str_to_cent_int(members[5])
        asset.last_price_change = __dollar_str_to_cent_int(members[6])
        asset.initial_balance = __dollar_str_to_cent_int(members[7])
        asset.todays_gain_cent = __dollar_str_to_cent_int(members[8])
        asset.todays_gain_percent = __dollar_str_to_cent_int(members[9])
        asset.total_gain_cent = __dollar_str_to_cent_int(members[10])
        asset.total_gain_percent = __dollar_str_to_cent_int(members[11])
        asset.cost_basis_share = __dollar_str_to_cent_int(members[12])
        asset.cost_basis_total = __dollar_str_to_cent_int(members[13])
        asset.category = members[14]

        assets.append(asset)
    
    return assets


def __dollar_str_to_cent_int(val):
    try:
        return int(float(val) * 100)
    except ValueError:
        return val
