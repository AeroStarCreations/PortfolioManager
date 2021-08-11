from objects.account_details import AccountDetails

ACCOUNTS = {
    '1': AccountDetails('Z04711651', 'Index Fund'),
    '2': AccountDetails('Z09549221', 'ETF'),
    '3': AccountDetails('Z09542051', 'Junkyard')
}

TASKS = [
    'Invest Cash',
    'Rebalance',
    'Get Summary'
]

INDEX_FUND_SYMBOLS = [
    'FPADX',
    'FSKAX',
    'FSMAX',
    'FSPSX',
    'FSSNX',
    'FUAMX',
    'FXAIX',
    'FXNAX',
    'FSMDX',
    'FSGGX'
]

ETF_SYMBOLS = [
    'QQQM',
    'VUG',
    'VO',
    'VB',
    'SPEM',
    'IEMG',
    'SPTL',
    'IAGG',
]

JUNKYARD_SYMBOLS = [
    'AMZN',
    'FSMAX',
    'FSKAX',
    'FSPSX'
]

ALL_SYMBOLS = INDEX_FUND_SYMBOLS + ETF_SYMBOLS + JUNKYARD_SYMBOLS + ['FCASH']

INDEX_FUND_ALLOCATIONS = {
    'large_cap': {
        'name': 'Large Cap',
        'assets': {
            'FXAIX': 0.35,
            'FSKAX': 0
        }
    },
    'mid_cap': {
        'name': 'Mid Cap',
        'assets': {
            'FSMAX': 0,
            'FSMDX': 0.2
        }
    },
    'small_cap': {
        'name': 'Small Cap',
        'assets': {
            'FSSNX': 0.2
        }
    },
    'int_developed': {
        'name': 'Intl Developed',
        'assets': {
            'FSPSX': 0,
            'FSGGX': 0.1
        }
    },
    'int_emerging': {
        'name': 'Intl Emerging',
        'assets': {
            'FPADX': 0.1
        }
    },
    'domestic_bond': {
        'name': "Domestic Bond",
        'assets': {
            'FXNAX': 0.025,
            'FUAMX': 0.025
        }
    }
}

ETF_ALLOCATIONS = {
    'large_cap': {
        'name': 'Large Cap',
        'assets': {
            'QQQM': 0.25,
            'VUG': 0.10
        }
    },
    'mid_cap': {
        'name': 'Mid Cap',
        'assets': {
            'VO': 0.2
        }
    },
    'small_cap': {
        'name': 'Small Cap',
        'assets': {
            'VB': 0.2
        }
    },
    'int_developed': {
        'name': 'Intl Developed',
        'assets': {
            'SPEM': 0.1
        }
    },
    'int_emerging': {
        'name': 'Intl Emerging',
        'assets': {
            'IEMG': 0.1
        }
    },
    'domestic_bond': {
        'name': "Domestic Bond",
        'assets': {
            'SPTL': 0.025
        }
    },
    'int_bond': {
        'name': "International Bond",
        'assets': {
            'IAGG': 0.025
        }
    }
}

JUNKYARD_ALLOCATIONS = {
    'all': {
        'name': "All",
        'assets': {
            'AMZN': 100,
            'FSMAX': 0,
            'FSKAX': 0,
            'FSPSX': 0,
        }
    }
}

def format_cents(cents):
    try:
        result = f'${abs(cents/100):,.2f}'
        if cents < 0:
            return f'({result})'
        return result
    except TypeError:
        return str(cents)
