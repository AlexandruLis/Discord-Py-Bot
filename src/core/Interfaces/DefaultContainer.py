import pickle


class PickleDefaultContainer:
    """
    TODO
    """

    def __init__(self, path):
        """
        :param path: file name or true path
        """
        self.filePath = path  # Dictionary pickle location
        self.dict = self.loadDict()
        if self.dict is None:  # No dict found, make an empty one
            self.dict = {}
            self.saveDict()

    def saveDict(self):
        """
        Saves the dictionary to the file
        """
        file = open(self.filePath, "wb")
        pickle.dump(self.dict, file)
        file.close()

    def loadDict(self):
        """
        Loads the dictionary from the file
        """
        try:
            file = open(self.filePath, "rb")
            dictHolder = pickle.load(file)
            file.close()
            return dictHolder
        except EOFError:  # Dictionary file exists but it's empty or a bunch of spaces
            self.dict = {}
        except FileNotFoundError:  # Dictionary file doesnt exist
            file = open(self.filePath, "wb")
            file.close()
