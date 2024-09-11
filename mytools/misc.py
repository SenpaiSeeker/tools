from io import BytesIO


class Handler:
    def get_arg(message):
        if message.reply_to_message and len(message.command) < 2:
            return message.reply_to_message.text or message.reply_to_message.caption or ""
        return message.text.split(None, 1)[1] if len(message.command) > 1 else ""

    def get_text(message, is_chatbot=False):
        reply_text = message.reply_to_message.text or message.reply_to_message.caption if message.reply_to_message else ""
        user_text = message.text if is_chatbot else message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else ""
        return f"{user_text}\n\n{reply_text}" if reply_text and user_text else reply_text + user_text

    async def send_large_output(message, output):
        if len(output) <= 4000:
            await message.reply(output)
        else:
            with BytesIO(str.encode(str(output))) as out_file:
                out_file.name = "result.txt"
                await message.reply_document(document=out_file)
