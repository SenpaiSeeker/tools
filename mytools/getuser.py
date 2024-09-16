from pyrogram import enums


class Extract:
    async def getUserId(self, message, username):
        entities = message.entities

        if entities:
            entity_index = 1 if message.text.startswith("/") else 0
            entity = entities[entity_index]

            if entity.type == enums.MessageEntityType.MENTION:
                return (await message._client.get_chat(username)).id
            elif entity.type == enums.MessageEntityType.TEXT_MENTION:
                return entity.user.id
        return username

    async def userId(self, message, text):
        if text.isdigit():
            return int(text)
        else:
            return await self.getUserId(message, text)

    async def getRid(self, message, sender_chat=False):
        text = message.text.strip()
        args = text.split()

        if message.reply_to_message:
            reply = message.reply_to_message
            if reply.from_user:
                user_id = reply.from_user.id
            elif sender_chat and reply.sender_chat and reply.sender_chat.id != message.chat.id:
                user_id = reply.sender_chat.id
            else:
                return None, None

            reason = text.split(None, 1)[1] if len(args) > 1 else None
            return user_id, reason

        if len(args) == 2:
            user = args[1]
            return await self.userId(message, user), None

        if len(args) > 2:
            user, reason = args[1], " ".join(args[2:])
            return await self.userId(message, user), reason

        return None, None

    async def getAdmin(self, message):
        member = await message._client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER)

    async def getId(self, message):
        return (await self.getRid(message))[0]

    def getMention(self, user):
        name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        link = f"tg://user?id={user.id}"
        return f"[{name}]({link})"
