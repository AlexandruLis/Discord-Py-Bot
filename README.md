# Discord-Py-Bot
 A bot in python using discord.py
 
 In order to run the bot you will need to generate a discord bot token as well as a reddit API app. They're free and easy to generate
 
Discord bot token: https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord

Reddit API info: https://stackoverflow.com/a/42304034
 # Setup

 create a file called globals.py in directory "/classified"
 Paste the following and fill it with your preffered paths, and your reddit api credentials.

>copypasta_file_path = ""
>reactions_file_path = ""
>banned_subredditss = ""
>blacklist_file_path = ""
>settings_file_path = ""


>reddit_class_client_id = ""
>reddit_class_client_secret = ""
>reddit_class_username = ""
>reddit_class_password = ""
>reddit_class_user_agent = ""


>default_json_for_guild = '{ ' \
                         ' "blacklist": { "enabled" : 1 }, ' \
                         ' "copypasta": { "enabled" : 1 }, ' \
                         ' "dictionary": { "enabled" : 1 }, ' \
                         ' "discordbotvoice": { "enabled" : 1 }, ' \
                         ' "google": { "enabled" : 1, ' \
                                '"translate" : { "enabled": 1, "languages" : ["de","fr", "it", "eo"] }}, ' \
                         ' "discordrategirl": { "enabled" : 1 }, ' \
                         ' "miscellaneous": { "enabled" : 1 }, ' \
                         ' "reactions": { "enabled" : 1 }, ' \
                         ' "reddit": { "enabled" : 1 }, ' \
                         ' "youtube": { "enabled" : 1 }, ' \
                         ' "logging": { "enabled" : 1, "on_edit": {"channel_to_post_in": "667890763274780692"} } ' \
                         '}'
    
Create a file called token.py in /classified/bot_token
Paste and fill it with your token
>bot_token = ""
