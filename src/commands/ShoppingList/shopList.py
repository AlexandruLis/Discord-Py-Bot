from src.core.Interfaces.DefaultContainer import PickleDefaultContainer


class ShopList(PickleDefaultContainer):
    def add_item(self, item: str, amount: str, category: str = 'none'):
        if self.item_dict[category] is None:
            self.item_dict[category] = {}
        self.item_dict[category][item]['amount'] = amount

    def remove_item(self, item: str, category: str = 'none'):
        """
        Remove an item. If category not given, look into all categories.
        :param item: Item to remove.
        :param category: Category in which it is.
        :return: TODO : decide
        """
        pass

    def remove_category(self, category: str):
        """
        Remove a category. Also removes all items.
        :param category: Name of category to remove
        :return: TODO : decide
        """
        pass

    def merge_categories(self, to_merge: str, merge_into: str):
        """
        Merge 2 categories. to_merge items will get moved into merge_into. to_merge gets removed in the process.
        :param to_merge: list you want to merge
        :param merge_into: list to merge into
        :return: TODO : decide
        """
        pass

    def return_category(self, category: str = 'none'):
        pass

    def return_all(self):
        pass

    def return_similar
