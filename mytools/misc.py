from io import BytesIO


class Handler:
    def getArg(self, message):
        return (
            message.reply_to_message.text or message.reply_to_message.caption
            if message.reply_to_message and len(message.command) < 2
            else message.text.split(None, 1)[1] if len(message.command) > 1 else ""
        )

    def getMsg(self, message):
        reply_text = message.reply_to_message.text or message.reply_to_message.caption if message.reply_to_message else ""
        user_text = message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else ""
        return f"{user_text}\n\n{reply_text}".strip() if reply_text and user_text else reply_text + user_text

    async def sendLongPres(self, message, output, is_delete=None):
        (
            await message.reply(output)
            if len(output) <= 4000
            else await message.reply_document(document=BytesIO(output.encode(), name="result.txt"))
        )
        if is_delete:
            await is_delete.delete()
