from src.commands.Settings.Settings import Settings
from classified.globals import settings_file_path


class SettingsController:
    def __init__(self, guild):
        self.settings = Settings(settings_file_path + str(guild.id), guild.id)
        self.guild = guild

    def add(self, jsonString):
        return self.settings.add(self.guild.id, jsonString)

    def update(self, jsonString):
        return self.settings.update(jsonString)  # TODO

    def remove(self, guildId):
        return self.settings.remove(self.guild.id)

    def get(self):
        return self.settings.get(self.guild.id)

    def get_setting(self, module, command):
        return self.settings.get_setting(self.guild.id, module, command)

    def get_option(self, module, command, option):
        return self.settings.get_option(self.guild.id, module, command, option)
