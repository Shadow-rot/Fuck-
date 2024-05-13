class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6584789596"
    sudo_users = "6101457748", "5932230962", "6100011620", "2010819209", "5702598840", "1813320767", "6154972031", "6584789596", "5702598840"
    GROUP_ID = -1002133191051
    TOKEN = "7067713339:AAGB3tSBfrrh1wHKuDmKthKqxLWKmi7HdNI"
    mongo_url = "mongodb+srv://Srikanta:srikanta@cluster0.xzbil3m.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/ed23556d07d33db18402d.jpg", "https://telegra.ph//file/e64337bbc6cdac7e6b178.jpg"]
    SUPPORT_CHAT = "Grabbing_Your_WH_Group"
    UPDATE_CHAT = "Grabbing_Your_WH_Channel"
    BOT_USERNAME = "Testing_Opx_bot"
    CHARA_CHANNEL_ID = "-1002009998662"
    api_id = 24089031
    api_hash = "0615e3afe13ddaaf8e9ddbd3977d35ff"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
