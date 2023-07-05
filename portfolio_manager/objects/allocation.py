from .allocation_category import AllocationCategory

class Allocation():

    def __init__(self):
        self.categories = []

    def with_category(self, allocation_category: AllocationCategory):
        self.add_category(allocation_category)
        return self

    def verify(self):
        # print(f'sum = ${sum([category.get_total_percentage() for category in self.categories])}')
        # proximityTo100 = abs(sum([category.get_total_percentage() for category in self.categories]) - 1.0)
        # assert proximityTo100 < 0.000000000000001
        total_percentage = sum([category.get_total_percentage() for category in self.categories])
        assert 100 == total_percentage, f'Total allocation percentage must equal 100. Was {total_percentage}'
        return self

    def add_category(self, allocation_category: AllocationCategory):
        self.categories.append(allocation_category)

    def get_categories(self):
        return self.categories

    def get_list_of_symbols(self):
        symbols = []
        for category in self.categories:
            symbols = symbols + category.get_list_of_symbols()
        return symbols

    def contains_symbol(self, symbol):
        return any([category.contains_symbol(symbol) for category in self.categories])

    def __str__(self):
        string = '------- Allocation Object -------'
        string = string + ''.join([f'\n{category}' for category in self.categories])
        string = string + '\n---------------------------------'
        return string
