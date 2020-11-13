from src.commands.copypasta.copypastas import Quotes
from classified.globals import quotes_file_path


class QuotesController:

    def __init__(self, guild):
        """
        Loads the file
        """
        self.guild = guild  # The discord channel
        self.quotes = Quotes(quotes_file_path + str(guild.id))  # generic path + g_id identifier

    def add(self, key: str, quote: str, bits):
        """
        Add a quote
        TODO lol
        :return:
        """
        status = self.quotes.addQuote(key, quote, bits)
        if status == 0:
            return 0
        elif status == -1:
            return -1
        self.quotes.saveDict()

    def get(self, key: str):
        """
        Returns a message for key
        :param key: a string/ key / message that triggers a keyword
        :return: quote
        """
        return self.quotes.quotesDict[key]

    def remove(self, key):
        """
        Remove a quote
        :param key:
        :return: status = action result
        """
        status = self.quotes.removeQuote(key)
        self.quotes.saveDict()
        return status

    def removeByQuote(self, key):
        status = self.quotes.removeByQuote(
            key)
        self.quotes.saveDict()
        return status

    # if that then do this
    def get_dict(self):
        """
        Returns the dictionary
        :return: dictionary
        """
        return self.quotes.quotesDict

    def update_to_access_bits(self):
        self.quotes.update_to_access_bits()

    def set_bits(self, key, bits):
        self.quotes.loadDict()
        return self.quotes.setBits(key, bits)
