class AllocationCategory():
    
    def __init__(self, name):
        self.name = name
        self.assets = {}

    def with_asset(self, symbol, percentage):
        self.add_asset(symbol, percentage)
        return self

    def add_asset(self, symbol, percentage):
        assert percentage >= 0.0, 'Asset allocation is less than 0.0'
        assert percentage <= 1.0, 'Asset allocation is more than 1.0'
        self.assets[symbol] = percentage

    def get_assets(self):
        return self.assets

    def get_total_percentage(self):
        return sum(self.assets.values())

    def get_list_of_symbols(self):
        return self.assets.keys()

    def contains_symbol(self, symbol):
        return any([symbol == sym for sym in self.assets.keys()])

    def __str__(self):
        string = self.name
        string = string + ''.join([f'\n  {symbol}: {percentage}' for symbol, percentage in self.assets.items()])
        return string