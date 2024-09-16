from io import BytesIO


class Handler:
    def getArg(self, message):
        if message.reply_to_message and len(message.command) < 2:
            return message.reply_to_message.text or message.reply_to_message.caption or ""
        return message.text.split(None, 1)[1] if len(message.command) > 1 else ""

    def getMsg(self, message, is_chatbot=False):
        reply_text = message.reply_to_message.text or message.reply_to_message.caption if message.reply_to_message else ""
        user_text = message.text if is_chatbot else (message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else "")
        return f"{user_text}\n\n{reply_text}".strip() if reply_text and user_text else reply_text + user_text

    async def sendLongPres(self, message, output):
        if len(output) <= 4000:
            await message.reply(output)
        else:
            with BytesIO(output.encode()) as out_file:
                out_file.name = "result.txt"
                await message.reply_document(document=out_file)

    def getTime(self, seconds):
        time_units = [(60, "s"), (60, "m"), (24, "h"), (7, "d"), (4.34812, "w")]
        result = []

        for unit_seconds, suffix in time_units:
            if seconds == 0:
                break
            seconds, value = divmod(seconds, unit_seconds)
            if value > 0:
                result.append(f"{int(value)}{suffix}")

        if not result:
            return "0s"

        return ":".join(result[::-1])
