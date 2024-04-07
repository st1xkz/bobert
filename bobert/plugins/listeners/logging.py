import io
from datetime import datetime

import hikari
import lightbulb

from bobert.core.utils import constants as const
from bobert.core.utils.helpers import get_role_permission_names

mod_logs = lightbulb.Plugin("mod-logs")

MOD_CH = 993698032463925398


@mod_logs.listener(hikari.GuildMessageDeleteEvent)
async def on_deleted_message(event: hikari.GuildMessageDeleteEvent) -> None:
    """Message deletion logging"""
    message = event.old_message
    member_id = message.author
    member = event.get_guild().get_member(member_id)

    if message is None:
        return
    if message.author.is_bot:
        return
    if member is not None:
        # Send to mod log channel
        embed = hikari.Embed(
            title="Message Deleted",
            description=f"{const.EMOJI_DELETE} A message was deleted in <#{event.get_channel().id}>",
            color=0xF94833,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(name="Content:", value=message.content, inline=False)
        embed.set_author(
            name=f"Deleted by {member} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"MID: {message.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        return


@mod_logs.listener(hikari.GuildBulkMessageDeleteEvent)
async def on_bulk_deleted_message(
    event: hikari.GuildBulkMessageDeleteEvent,
) -> None:
    """Bulk message deletion logging"""
    # Create list to store info about each deleted message
    msg_info = []

    for message_id, message in event.old_messages.items():
        member = event.get_guild().get_member(message.author)
        if member is not None:
            msg_data = f"[{message.created_at.strftime('%b %d %Y %H:%M:%S')}] "
            msg_data += f"{member} - ({member.id}) "
            msg_data += f"[{message_id}]: "
            msg_data += f"{message.content}\n"
            msg_info.append(msg_data)

    # Create a string from the message info
    msg_info_str = "\n".join(msg_info)

    # Convert the string to bytes
    bytes_data = msg_info_str.encode("utf-8")

    # Send to mod log channel
    embed = hikari.Embed(
        title="Bulk Messages Deleted",
        description=f"{const.EMOJI_DELETE} **{len(event.message_ids)}** messages were deleted in <#{event.get_channel().id}>. See the attached file for details.",
        color=0xFE8019,
        timestamp=datetime.now().astimezone(),
    )
    file_data = hikari.Bytes(bytes_data, "bulk_delete.txt")
    await mod_logs.bot.rest.create_message(MOD_CH, embed=embed, attachment=file_data)


@mod_logs.listener(hikari.GuildMessageUpdateEvent)
async def on_edited_message(event: hikari.GuildMessageUpdateEvent) -> None:
    """Edited message logging"""
    # Check if message is from bot or webhook
    if event.is_bot or event.is_webhook:
        return

    member = event.member
    if member is None:
        return

    if member is not None:
        embed = hikari.Embed(
            title="Message Edited",
            description=f"{const.EMOJI_EDIT} A message was edited in <#{event.get_channel().id}>",
            color=0xFABD2F,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(name="Before:", value=event.old_message.content, inline=False)
        embed.add_field(name="After:", value=event.content, inline=False)
        embed.set_author(
            name=f"Edited by {member} ({member.id})", icon=member.display_avatar_url
        )
        embed.set_footer(text=f"MID: {event.message_id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


@mod_logs.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    """Voice channel activity logging"""
    user_id = event.state.user_id
    old_ch_id = event.old_state.channel_id if event.old_state else None
    new_ch_id = event.state.channel_id

    # Check if user is joining or leaving a voice channel
    if old_ch_id is None:
        action = "joined"
        color = 0x8EC07C  # Green color for join action
    elif new_ch_id is None:
        action = "left"
        color = 0xF94833  # Red color for leave action
    else:
        action = "moved"
        color = 0xFABD2F  # Yellow color for move action

    embed = hikari.Embed(
        title=f"{action.capitalize()} Voice Channel",
        description=f"<@{user_id}> ({user_id}) has {action} a voice channel",
        color=color,
        timestamp=datetime.now().astimezone(),
    )
    if action == "moved":
        embed.description = f"<@{user_id}> ({user_id}) has {action} voice channels"
        if old_ch_id:
            embed.add_field(name="From Channel:", value=f"<#{old_ch_id}>")
        if new_ch_id:
            embed.add_field(name="To Channel:", value=f"<#{new_ch_id}>")
    else:
        if new_ch_id or old_ch_id:
            embed.add_field(name="Channel:", value=f"<#{new_ch_id or old_ch_id}>")
    if new_ch_id or old_ch_id:
        embed.set_footer(text=f"CHID: {new_ch_id or old_ch_id}")

    await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


@mod_logs.listener(hikari.GuildChannelCreateEvent)
async def on_channel_create(event: hikari.GuildChannelCreateEvent) -> None:
    """Channel creation logging"""
    channel = event.channel

    # Determine emoji based on channel type
    emoji = const.EMOJI_TEXT
    if channel.type is hikari.ChannelType.GUILD_VOICE:
        emoji = const.EMOJI_VOICE
    elif channel.type is hikari.ChannelType.GUILD_FORUM:
        emoji = const.EMOJI_FORUM
    elif channel.type is hikari.ChannelType.GUILD_STAGE:
        emoji = const.EMOJI_STAGE
    elif channel.type is hikari.ChannelType.GUILD_CATEGORY:
        emoji = const.EMOJI_CATEGORY

    # Fetch audit logs
    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.get_guild(), event_type=hikari.AuditLogEventType.CHANNEL_CREATE
    ):
        member = list(entry.users.values())[0]

        embed = hikari.Embed(
            title="Channel Created",
            description=f"A new {channel.type.name.split('_')[-1].lower()} {emoji} channel `{channel.name}` was created",
            color=0x8EC07C,
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Created by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"CHID: {channel.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        break


@mod_logs.listener(hikari.GuildChannelDeleteEvent)
async def on_channel_delete(event: hikari.GuildChannelDeleteEvent) -> None:
    """Channel deletion logging"""
    channel = event.channel

    # Determine emoji based on channel type
    emoji = const.EMOJI_TEXT
    if channel.type is hikari.ChannelType.GUILD_VOICE:
        emoji = const.EMOJI_VOICE
    elif channel.type is hikari.ChannelType.GUILD_FORUM:
        emoji = const.EMOJI_FORUM
    elif channel.type is hikari.ChannelType.GUILD_STAGE:
        emoji = const.EMOJI_STAGE
    elif channel.type is hikari.ChannelType.GUILD_CATEGORY:
        emoji = const.EMOJI_CATEGORY

    # Fetch audit logs
    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.get_guild(), event_type=hikari.AuditLogEventType.CHANNEL_DELETE
    ):
        member = list(entry.users.values())[0]

        embed = hikari.Embed(
            title="Channel Deleted",
            description=f"{const.EMOJI_DELETE} A {channel.type.name.split('_')[-1].lower()} {emoji} channel `{channel.name}` was deleted",
            color=0xF94833,
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Deleted by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"CHID: {channel.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        break


# Finish on_channel_update listener
@mod_logs.listener(hikari.GuildChannelUpdateEvent)
async def on_channel_update(event: hikari.GuildChannelUpdateEvent) -> None:
    """Channel update logging"""
    old_ch = event.old_channel
    new_ch = event.channel

    # Determine emoji based on channel type
    emoji = const.EMOJI_TEXT
    if new_ch.type is hikari.ChannelType.GUILD_VOICE:
        emoji = const.EMOJI_VOICE
    elif new_ch.type is hikari.ChannelType.GUILD_FORUM:
        emoji = const.EMOJI_FORUM
    elif new_ch.type is hikari.ChannelType.GUILD_STAGE:
        emoji = const.EMOJI_STAGE
    elif new_ch.type is hikari.ChannelType.GUILD_CATEGORY:
        emoji = const.EMOJI_CATEGORY

    # Determine title based on type of update
    update_type = "Unknown"
    before = []
    after = []
    before_perms = ", ".join(
        [
            f"{str(p)}: {old_ch.permission_overwrites[p]}"
            for p in old_ch.permission_overwrites
        ]
    )
    after_perms = ", ".join(
        [
            f"{str(p)}: {new_ch.permission_overwrites[p]}"
            for p in new_ch.permission_overwrites
        ]
    )

    if new_ch.name != old_ch.name:
        update_type = "Name"
        before.append(old_ch.name)
        after.append(new_ch.name)
    if isinstance(new_ch, hikari.GuildTextChannel):
        if new_ch.topic != old_ch.topic:
            update_type = "Topic"
            before.append(old_ch.topic)
            after.append(new_ch.topic)
    if new_ch.position != old_ch.position:
        update_type = "Position"
        before.append(old_ch.position)
        after.append(new_ch.position)
    if new_ch.is_nsfw != old_ch.is_nsfw:
        update_type = "NSFW"
        before.append(old_ch.is_nsfw)
        after.append(new_ch.is_nsfw)
    if before_perms != after_perms:
        update_type = "Permissions"
        before.append(before_perms)
        after.append(after_perms)

    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.get_guild(), event_type=hikari.AuditLogEventType.CHANNEL_UPDATE
    ):
        member = list(entry.users.values())[0]

        embed = hikari.Embed(
            title=f"Channel Updated ({update_type})",
            description=f"{const.EMOJI_INFO} A {new_ch.type.name.split('_')[-1].lower()} {emoji} channel `{new_ch.name}` was updated",
            color=0x3DA5D9,
            timestamp=datetime.now().astimezone(),
        )
        if before and after:
            # Add before and after fields for each property that changed
            for before_changes, after_changes in zip(before, after):
                embed.add_field(name="Before:", value=before_changes, inline=False)
                embed.add_field(name="After:", value=after_changes, inline=False)
        embed.set_author(
            name=f"Updated by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"CHID: {new_ch.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        return


@mod_logs.listener(hikari.RoleCreateEvent)
async def on_create_role(event: hikari.RoleCreateEvent) -> None:
    """Role creation logging"""
    role = event.role

    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=role.guild_id, event_type=hikari.AuditLogEventType.ROLE_CREATE
    ):
        member = list(entry.users.values())[0]

        embed = hikari.Embed(
            title="Role Created",
            color=0x000000,
            description=f"A new role `{role.name}` was created",
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Created by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"RID: {role.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        break


@mod_logs.listener(hikari.RoleUpdateEvent)
async def on_role_update(event: hikari.RoleUpdateEvent) -> None:
    """Role update event"""
    old_role = event.old_role
    new_role = event.role

    # Determine the changes made to role
    updates = []

    if new_role.name != old_role.name:
        updates.append(("Name", old_role.name, new_role.name))
    if new_role.color != old_role.color:
        updates.append(("Color", f"#{old_role.color:06X}", f"#{new_role.color:06X}"))
    if new_role.is_mentionable != old_role.is_mentionable:
        updates.append(
            ("Mentionable", old_role.is_mentionable, new_role.is_mentionable)
        )
    if new_role.is_hoisted != old_role.is_hoisted:
        updates.append(("Hoisted", old_role.is_hoisted, new_role.is_hoisted))
    if new_role.position != old_role.position:
        updates.append(("Position", old_role.position, new_role.position))

    update_type = "No updates"

    if updates:
        if len(updates) == 1:
            update_type, before, after = updates[0]
        else:
            update_type = "Multiple"
            before = "\n".join(f"{change[0]}: {change[1]}" for change in updates)
            after = "\n".join(f"{change[0]}: {change[2]}" for change in updates)

    # Fetch audit log entries for the role update event
    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.guild_id, event_type=hikari.AuditLogEventType.ROLE_UPDATE
    ):
        member = list(entry.users.values())[0]

        if entry.entries.get(event.role_id):
            perm_changes = []
            perm_names = {}
            # Check if the entry contains permission changes
            for change in entry.changes:
                if change.key == hikari.AuditLogChangeKey.PERMISSION_OVERWRITES:
                    for perm_id, perm_name in perm_names.items():
                        old_perm_value = (
                            "Denied" if perm_id in change.old_value else "Granted"
                        )
                        new_perm_value = (
                            "Denied" if perm_id in change.new_value else "Granted"
                        )
                        perm_changes.append((perm_name, old_perm_value, new_perm_value))
            if perm_changes:
                updates.append(("Permissions", perm_changes))
            update_type = "Permissions"
            break

        embed = hikari.Embed(
            title=f"Role Updated ({update_type})",
            description=f"{const.EMOJI_INFO} A role `{new_role.name}` was updated",
            color=new_role.color,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(name="Before:", value=before, inline=False)
        embed.add_field(name="After:", value=after, inline=False)
        embed.set_author(
            name=f"Updated by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"RID: {new_role.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        return


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mod_logs)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(mod_logs)
