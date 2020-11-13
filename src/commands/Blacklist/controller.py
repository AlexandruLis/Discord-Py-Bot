from src.commands.Blacklist.blacklistStorage import Blacklist
from classified.globals import blacklist_file_path
from src.commands.BotMiscellaneous.cog import MiscellaneousCog


class BlacklistController:
    def __init__(self, guild):
        """
        Loads the file
        """
        self.guild = guild  # The discord channel
        self.blacklist = Blacklist(blacklist_file_path + str(guild.id))  # The dictionary of copypastas read from file

    def add(self, channel, blacklistType, key: str):
        """
        :param channel: ctx.guild.channel
        :param blacklistType: string
        :param rawMessage: string
        :return:
        """
        # try:
        #     key = self.extract_details(rawMessage, blacklistType)
        # except ValueError as e:
        #     return str(e)
        status = self.blacklist.addBlacklist(key, channel, blacklistType)
        if status == 0:
            return 'I have no idea how you triggered this response'
        elif status == -1:
            return 'Already exists'
        self.blacklist.save_dict_to_file()
        return "Success"

    def extract_details(self, rawMessage, blacklistType):
        valueList = rawMessage.split()
        if blacklistType == 'message':
            return rawMessage
        elif blacklistType == 'emoji':
            for value in valueList:
                try:
                    emoji_id = MiscellaneousCog.find_number_in_str(value)
                    return str(emoji_id)
                except ValueError:
                    pass
        else:
            raise ValueError("'{}' is not a blacklist type!".format(blacklistType))

    # def get(self, key: str):
    #     """
    #     Returns a copy pasta / message for key
    #     :param key: a string/ key / message that triggers a keyword
    #     :return: string, a Quotes
    #     """
    #     return self.pastas.pasta_dict[key]

    def remove(self, key):
        """
        Removes a Quotes
        :param key: key of the Quotes to be removed
        :return: status = if the copy pasta was found and removed or not
        """
        status = self.pastas.remove_pasta(key)
        self.pastas.save_dict_to_file()
        return status

    def removeByValue(self, key):
        status = self.pastas.removeSauce(
            key)
        self.pastas.save_dict_to_file()
        return status

    # if that then do this
    def get_dict(self):
        """
        Returns the dictionary of copypastas
        :return: dictionary
        """
        return self.pastas.pasta_dict

    def update_to_access_bits(self):
        self.pastas.update_to_access_bits()

    def set_bits(self, msg):
        self.pastas.load_dict_from_file()
        return self.pastas.set_bits_value(msg)
