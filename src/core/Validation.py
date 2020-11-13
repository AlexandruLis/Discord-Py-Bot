async def validateAdmin(message):
    if not message.author.top_role.permissions.administrator:
        await message.channel.send("You have no power here")
        return False
    return True
