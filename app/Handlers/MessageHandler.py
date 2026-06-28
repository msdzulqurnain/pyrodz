class MessageHandler:
    async def message(self, client, message):
        if message.text:
            await message.reply(message.text)
        elif message.photo:
            await message.reply_photo(message.photo.file_id)
        elif message.video:
            await message.reply_video(message.video.file_id)
        elif message.document:
            await message.reply_document(message.document.file_id)
        elif message.audio:
            await message.reply_audio(message.audio.file_id)
        elif message.voice:
            await message.reply_voice(message.voice.file_id)
        elif message.sticker:
            await message.reply_sticker(message.sticker.file_id)
        elif message.animation:
            await message.reply_animation(message.animation.file_id)
