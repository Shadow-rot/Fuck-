import urllib.request
from pymongo import ReturnDocument

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

WRONG_FORMAT_TEXT = """Wrong ❌️ format...  eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

use rarity number accordingly rarity Map

rarity_map = 1 (🟢 𝗖𝗼𝗺𝗺𝗼𝗻), 2 (🟣 𝗥𝗮𝗿𝗲) , 3 (🟡 𝗟𝗲𝗴𝗲𝗻𝗱𝗮𝗿𝘆), 4 (💮 𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝗘𝗱𝗶𝘁𝗶𝗼𝗻), 5 (🔮 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗘𝗱𝗶𝘁𝗶𝗼𝗻), 6 (🎗️ 𝗦𝘂𝗽𝗿𝗲𝗺𝗲)"""



async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        try:
            urllib.request.urlopen(args[0])
        except:
            await update.message.reply_text('Invalid URL.')
            return

        rarity_map = {1: "🟢 𝗖𝗼𝗺𝗺𝗼𝗻", 2: "🟣 𝗥𝗮𝗿𝗲", 3: "🟡 𝗟𝗲𝗴𝗲𝗻𝗱𝗮𝗿𝘆", 4: "💮 𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝗘𝗱𝗶𝘁𝗶𝗼𝗻", 5: "🔮 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗘𝗱𝗶𝘁𝗶𝗼𝗻",6: "🎗️ 𝗦𝘂𝗽𝗿𝗲𝗺𝗲"}
        try:
            rarity = rarity_map[int(args[3])]
        except KeyError:
            await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, or 5.')
            return

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id
        }

        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=args[0],
                caption=f'<b>Character 𝙉𝙖𝙢𝙚:</b> {character_name}\n<b>𝘼𝙣𝙞𝙢𝙚 𝙉𝙖𝙢𝙚:</b> {anime}\n<b>𝙍𝙖𝙧𝙞𝙩𝙮:</b> {rarity}\n<b>𝙄𝘿:</b> {id}\n𝘼𝙙𝙙𝙚𝙙 𝘽𝙮 ➪ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('CHARACTER ADDED....')
        except:
            await collection.insert_one(character)
            update.effective_message.reply_text("ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴅᴅᴇᴅ ʙᴜᴛ ɴᴏ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ғᴏᴜɴᴅ. ᴄᴏɴsɪᴅᴇʀ ᴀᴅᴅɪɴɢ ᴏɴᴇ .")
        
    except Exception as e:
        await update.message.reply_text(f'Character Upload Unsuccessful. Error: {str(e)}\nIf you think this is a source error, forward to: {SUPPORT_CHAT}')

async def delete(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask my Owner to use this Command...')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('Incorrect format... Please use: /delete ID')
            return

        
        character = await collection.find_one_and_delete({'id': args[0]})

        if character:
            
            await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
            await update.message.reply_text('DONE')
        else:
            await update.message.reply_text('ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ғʀᴏᴍ ᴅʙ, ʙᴜᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴄʜᴀɴɴᴇʟ')
    except Exception as e:
        await update.message.reply_text(f'{str(e)}')

async def update(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('Incorrect format. Please use: /update id field new_value')
            return

        # Get character by ID
        character = await collection.find_one({'id': args[0]})
        if not character:
            await update.message.reply_text('Character not found.')
            return

        # Check if field is valid
        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if args[1] not in valid_fields:
            await update.message.reply_text(f'Invalid field. Please use one of the following: {", ".join(valid_fields)}')
            return

        # Update field
        if args[1] in ['name', 'anime']:
            new_value = args[2].replace('-', ' ').title()
        elif args[1] == 'rarity':
            rarity_map = {1: "🟢 𝗖𝗼𝗺𝗺𝗼𝗻", 2: "🟣 𝗥𝗮𝗿𝗲", 3: "🟡 𝗟𝗲𝗴𝗲𝗻𝗱𝗮𝗿𝘆", 4: "💮 𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝗘𝗱𝗶𝘁𝗶𝗼𝗻", 5 : "🔮 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗘𝗱𝗶𝘁𝗶𝗼𝗻", 6: "🎗️ 𝗦𝘂𝗽𝗿𝗲𝗺𝗲"}
            try:
                new_value = rarity_map[int(args[2])]
            except KeyError:
                await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, 4, or 5.')
                return
        else:
            new_value = args[2]

        await collection.find_one_and_update({'id': args[0]}, {'$set': {args[1]: new_value}})

        
        if args[1] == 'img_url':
            await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=new_value,
                caption=f'<b>Character 𝙉𝙖𝙢𝙚:</b> {character["name"]}\n<b>𝘼𝙣𝙞𝙢𝙚 𝙉𝙖𝙢𝙚:</b> {character["anime"]}\n<b>𝙍𝙖𝙧𝙞𝙩𝙮:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\n𝙐𝙥𝙙𝙖𝙩𝙚𝙙 𝘽𝙮 ➪ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.find_one_and_update({'id': args[0]}, {'$set': {'message_id': message.message_id}})
        else:
            
            await context.bot.edit_message_caption(
                chat_id=CHARA_CHANNEL_ID,
                message_id=character['message_id'],
                caption=f'<b>Character 𝙉𝙖𝙢𝙚:</b> {character["name"]}\n<b>𝘼𝙣𝙞𝙢𝙚 𝙉𝙖𝙢𝙚:</b> {character["anime"]}\n<b>𝙍𝙖𝙧𝙞𝙩𝙮:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\n𝙐𝙥𝙙𝙖𝙩𝙚𝙙 𝘽𝙮 ➪ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )

        await update.message.reply_text('ᴜᴘᴅᴀᴛᴇᴅ ᴅᴏɴᴇ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ... ʙᴜᴛ sᴏᴍᴇᴛɪᴍᴇs ɪᴛ ᴛᴀᴋᴇs ᴛɪᴍᴇ ᴛᴏ ᴇᴅɪᴛ ᴄᴀᴘᴛɪᴏɴ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ...sᴏ ᴡᴀɪᴛ...')
    except Exception as e:
        await update.message.reply_text(f'ɪ ɢᴜᴇss ᴅɪᴅ ɴᴏᴛ ᴀᴅᴅᴇᴅ ʙᴏᴛ ɪɴ ᴄʜᴀɴɴᴇʟ... ᴏʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴜᴘʟᴏᴀᴅᴇᴅ ʟᴏɴɢ ᴛɪᴍᴇ ᴀɢᴏ... ᴏʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴏᴛ ᴇxɪᴛs... ᴏʀʀ ᴡʀᴏɴɢ ɪᴅ')

UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
application.add_handler(UPLOAD_HANDLER)
DELETE_HANDLER = CommandHandler('delete', delete, block=False)
application.add_handler(DELETE_HANDLER)
UPDATE_HANDLER = CommandHandler('update', update, block=False)
application.add_handler(UPDATE_HANDLER)
