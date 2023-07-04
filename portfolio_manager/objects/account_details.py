from allocation import Allocation

class AccountDetails():
    def __init__(self, id, name, asset_allocation: Allocation):
        self.id = id
        self.name = name
        self.asset_allocation = asset_allocation