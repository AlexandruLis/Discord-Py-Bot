from src.core.Interfaces.DefaultContainer import PickleDefaultContainer
from classified.globals import default_json_for_guild
import copy
import json
from json import JSONDecodeError


class Settings(PickleDefaultContainer):

    def __init__(self, path, gid):
        super().__init__(path)
        if self.dict == {}:
            self.dict[gid] = self.get(gid)

    def get(self, guildId):
        try:
            return json.dumps(self.dict[guildId], sort_keys=True, indent=2)
        except KeyError:
            return copy.deepcopy(json.loads(default_json_for_guild))

    def on_initialize(self):
        pass

    def add(self, guildId, jsonString):
        try:
            self.dict[guildId] = json.loads(jsonString)
            self.saveDict()
            # print(self.item_dict)
        except KeyError:
            return "Wrong"

    def update(self, jsonString):
        try:
            update_fields = json.loads(jsonString)
        except JSONDecodeError:
            return "Invalid json"

        updated = False
        for field in update_fields:
            print(field)
            print(self.dict)
            guild_key = list(self.dict.keys())[0]  # Grab the key of the discord guild
            # No I have not coded myself into a corner and I'm too lazy to fix it
            # TODO make the json.loads be the dictionary...
            if field in self.dict[guild_key]:
                self.dict[guild_key][field] = update_fields[field]
                self.saveDict()
                updated = True
        if updated:
            return "Successfully updated"
        return "Field not recognized"

    def remove(self, guildId):
        # print(default_json_for_guild)
        self.dict[guildId] = json.loads(default_json_for_guild)
        self.saveDict()
        return "Reset"
        # print(self.item_dict)

    def get_setting(self, guildId, module, command):

        if self.dict[guildId][module]['enabled'] == 0:
            return False
        try:
            if self.dict[guildId][module][command]['enabled'] == 0:
                return False
        except KeyError:
            # print("Here")
            return True
        return True

    def get_option(self, guildId, module, command, option):
        return self.dict[guildId][module][command][option]
