class Allocation():

    def __init__(self):
        self.categories = []

    def with_category(self, allocation_category):
        self.add_category(allocation_category)
        return self

    def verify(self):
        assert sum([category.get_total_percentage() for category in self.categories]) == 1.0
        return self

    def add_category(self, allocation_category):
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
