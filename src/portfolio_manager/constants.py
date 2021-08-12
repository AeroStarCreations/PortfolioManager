from portfolio_manager.objects.account_details import AccountDetails
from portfolio_manager.objects.allocation import Allocation
from portfolio_manager.objects.allocation_category import AllocationCategory

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

ALL_SYMBOLS = INDEX_FUND_SYMBOLS + ETF_SYMBOLS + JUNKYARD_SYMBOLS + ['FCASH', 'USD']

INDEX_FUND_ALLOCATIONS_2 = (Allocation()
    .with_category(
        AllocationCategory('Large Cap')
            .with_asset("FXAIX", 0.35)
            .with_asset("FSKAX", 0)
    ).with_category(
        AllocationCategory('Mid Cap')
            .with_asset('FSMDX', 0.2)
            .with_asset('FSMAX', 0)
    ).with_category(
        AllocationCategory('Small Cap')
            .with_asset('FSSNX', 0.2)
    ).with_category(
        AllocationCategory('Intl Developed')
            .with_asset('FSGGX', 0.1)
            .with_asset('FSPSX', 0)
    ).with_category(
        AllocationCategory('Intl Emerging')
            .with_asset('FPADX', 0.1)
    ).with_category(
        AllocationCategory('Domestic Bond')
            .with_asset('FXNAX', 0.025)
            .with_asset('FUAMX', 0.025)
    )
).verify()

ETF_ALLOCATIONS_2 = (Allocation()
    .with_category(
        AllocationCategory('Large Cap')
            .with_asset("QQQM", 0.25)
            .with_asset("VUG", 0.1)
    ).with_category(
        AllocationCategory('Mid Cap')
            .with_asset('VO', 0.2)
    ).with_category(
        AllocationCategory('Small Cap')
            .with_asset('VB', 0.2)
    ).with_category(
        AllocationCategory('Intl Developed')
            .with_asset('SPEM', 0.1)
    ).with_category(
        AllocationCategory('Intl Emerging')
            .with_asset('IEMG', 0.1)
    ).with_category(
        AllocationCategory('Domestic Bond')
            .with_asset('SPTL', 0.025)
    ).with_category(
        AllocationCategory('Intl Bond')
            .with_asset('IAGG', 0.025)
    )
).verify()

JUNKYARD_ALLOCATIONS_2 = (Allocation()
    .with_category(
        AllocationCategory('All')
            .with_asset('AMZN', 1)
            .with_asset('FSMAX', 0)
            .with_asset('FSKAX', 0)
            .with_asset('FSPSX', 0)
    )
).verify()

ACCOUNTS = {
    '1': AccountDetails('Z04711651', 'Index Fund', INDEX_FUND_ALLOCATIONS_2),
    '2': AccountDetails('Z09549221', 'ETF', ETF_ALLOCATIONS_2),
    '3': AccountDetails('Z09542051', 'Junkyard', JUNKYARD_ALLOCATIONS_2)
}

def format_cents(cents):
    try:
        result = f'${abs(cents/100):,.2f}'
        if cents < 0:
            return f'({result})'
        return result
    except TypeError:
        return str(cents)
