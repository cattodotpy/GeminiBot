import discord


def prepare(
    guild: discord.Guild,
    channel: discord.TextChannel | discord.DMChannel,
    author: discord.Member,
):
    return {
        "author": prepare_user(author),
        "guild": {
            "id": guild.id,
            "name": guild.name,
            "icon_url": guild.icon.url if guild.icon else "",
            "member_count": guild.member_count,
            "owner": prepare_user(guild.owner),
            "members": [member.display_name for member in guild.members[:1000]]
            + ["..."]
            if guild.member_count > 1000
            else [member.display_name for member in guild.members],
            "channels": [channel.name for channel in guild.channels],
        },
        "channel": {
            "id": channel.id,
            "name": channel.name,
            "topic": channel.topic,
        },
    }


def prepare_user(user: discord.Member):
    return {
        "id": user.id,
        "name": user.global_name,
        "username": user.name,
        "discriminator": user.discriminator,
        "mention": user.mention,
        "avatar_url": user.display_avatar.url,
        "mutual_guilds": [guild.name for guild in user.mutual_guilds],
        "roles": [role.name for role in user.roles],
        "permissions": [perm for perm, value in user.guild_permissions if value],
    }


SEPERATOR = " " * 2


def visualize_dict(tree, d=0):
    output = ""
    if tree is None or len(tree) == 0:
        output += SEPERATOR * d + "-\n"
    elif isinstance(tree, list):
        if isinstance(tree[0], dict):
            for item in tree:
                output += visualize_dict(item, d)
        elif isinstance(tree[0], str):
            output += SEPERATOR * d + "\n".join(tree) + "\n"
    elif isinstance(tree, dict):
        for key, val in tree.items():
            if isinstance(val, (dict, list)):
                output += SEPERATOR * d + str(key) + "\n"
                output += visualize_dict(val, d + 1)
            else:
                output += SEPERATOR * d + f"{key}: {val}\n"
    else:
        output += SEPERATOR * d + str(tree) + "\n"

    # print(output)
    return output
