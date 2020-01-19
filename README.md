# Discord-Py-Bot
 A bot in python using discord.py
 
 In order to run the bot you will need to generate a discord bot token as well as a reddit API app. They're free and easy to generate
 
Discord bot token: https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord

Reddit API info: https://stackoverflow.com/a/42304034
 # Disclaimer
 I'm not good at formatting .readme
 # Setup

 create a file called globals.py in directory "/classified"
 Paste the following and fill it with your preffered paths, and your reddit api credentials.

>copypasta_file_path = "pickles/copypastas/copypastas_pickle.txt"                 
reactions_file_path = "pickles/reactions/reactions_pickle.txt"      
banned_subredditss = "pickles/reddit/banned_subreddits"        
blacklist_file_path = "pickles/blacklist/blacklist_pickle.txt"       
settings_file_path = "pickles/settings/settings_pickle.txt"      

>reddit_class_client_id = ""     
reddit_class_client_secret = ""      
reddit_class_username = ""      
reddit_class_password = ""      
reddit_class_user_agent = ""      


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

# Commands:   
CopyPasta = Bot responds to keywords by posting a message    
    -addpasta:  Add response to keyword 
    
>Example: .addpasta test "test response" 1

    -eatpasta:  Removes one of the copypastas   
    
>Example: .eatpasta test

    -pastabits: Changes if the trigger message gets deleted 
    
>Example: .pastabits test | 1
               
Dictionary = Parsing trough urban dictionary   

    -define:    UrbanDict definiton of a certain word  
    
>Example: .define sneakers

    -wotd:      Word of the day on UrbanDictionary
    
>Example: .wotd
          
DiscordBotVoice = Supposed to play music but it'll be added later   
    -join:      Bot joins the voice channel the user is in   
    -leave:     Bot leaves voice   
         
DiscordRateGirl (BETA) = Generates 2 PRNG values that stay consistent depending on day   
    -rategirl:  Rates @User by 2 values, Hot and Crazy   
    
>Example: .rategirl @User
         
         
Miscellaneous = For filler commands that don't deserve their own class   
    -avm:       Print avatar of pinged User   
    -badbot:    Same as goodbot       
    -cm:        Turns cm (height) to ft + inch (metric to imperial) by approximation   
    -dice:      Rolls 2 dice ( returns 2 values between 1-6)   
    -erase:     Erase N messages (admin only)  
    
>Example: .erase 5  # erases 5 messages

    -ft:        Turns height ft.inch (Eg: 5.11) to cm (imperial to metric)      
    -img:       Returns the first result from google images      
    -goodbot:   Filler command. Bot sends a message on call.      
    -hide:      Removes the messages of a user from a channel (admin only)
    
>Example: .hide @User 5  # Delete 5 messages of @User

    -kg:        Turn kg into lb (metric to imperial)      
    -killbot:   Turns the bot off (admin only)   
    -lb:        Turn lb into kg (imperial to metric)   
         
Reactions = Bot adds a reaction to a message that contains certain keywords   
    -addreact:  Add a reaction to a keyword/keywords  
    
>Example: .addreact love :heart:

    -rmreact:   Removes a reaction to a keyword/keywords
    
>Example: .rmreact love
        
Reddit = Parsing reddit for you   

>Example: .rbon funny 5

    -rbon:      Best Of N from a subreddit   
    -rrand:     Random search result from a subreddit   
    -rrsearch:  Random post from search results      
    -rsearch:   Top post from reddit search      
    -rtop:      Top post from hot section of subreddit   
         
Youtube = Parsing Youtube     

>Example: .yt cats
   
    -randyt:    Random result of a topic from youtube      
    -yt:        First result from youtube of a topic     
    
Blacklist = Bot blacklists a message/word/emoji/user !in the posted channel! TODO: make it blacklist serverwide
    -blacklist: 
    
>Example: .blacklist word idiot
>Example: .blacklist user @MentionUser # This is troll imo as it just deletes whatever they post as soon as it sees it, doesn't stop @MentionUser from spamming the channel
>Example: .blacklist message @MentionUser # The exact sentence they said gets deleted whenever posted
>Example: .blacklist emoji @MentionUser # Blocks all the emojis in the last @MentionUser message that contains Emojis

    
Settings = Disable or enable bot features based on Modules or Commands
    - .settings get/add/reset # TODO implement update and check json validity
    
> Example: .settings add {some json} # see setup default_json_for_guild

    - General format for the json is "Module": {"enabled": 1/0, "Command": {"enabled": 1/0, "optionName": {} }
    
> Example json "google": { "enabled" : 1, "translate" : { "enabled": 1, "languages" : ["de","fr", "it", "eo"] }}

