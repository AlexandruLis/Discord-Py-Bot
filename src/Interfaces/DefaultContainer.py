import pickle


class PickleDefaultContainer:
    """
    TODO
    """

    def __init__(self, path):
        """
        A file path where to store the dictionary of copyitems in a pickle format
        :param path: file name or true path
        """
        self.file_path = path  # Dictionary picke location
        self.item_dict = self.load_dict_from_file()
        if self.item_dict is None:  # No dict found, make an empty one
            self.item_dict = {}
            self.save_dict_to_file()

    def save_dict_to_file(self):
        """
        Saves the dictionary to the file
        """
        file = open(self.file_path, "wb")
        pickle.dump(self.item_dict, file)
        file.close()

    def load_dict_from_file(self):
        """
        Loads the dictionary from the file
        """
        try:
            file = open(self.file_path, "rb")
            dict_holder = pickle.load(file)
            file.close()
            return dict_holder
        except EOFError:  # Dictionary file exists but it's empty or a bunch of spaces
            self.item_dict = {}
        except FileNotFoundError:  # Dictionary file doesnt exist
            file = open(self.file_path, "wb")
            file.close()
