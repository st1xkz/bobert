import io
from datetime import datetime

import hikari
import hikari.audit_logs
import lightbulb

from bobert.core.utils import constants as const
from bobert.core.utils import helpers
from bobert.core.utils.chron import format_dt

mod_logs = lightbulb.Plugin("mod-logs")

MOD_CH = 825402276721721355


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
            color=0xF94833,  # Red color for message deletes
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
        color=0xFE8019,  # Orange color for message bulk deletes
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
            color=0xFABD2F,  # Yellow color for message edits
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
            color=0x8EC07C,  # Green color for channel creation
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
            color=0xF94833,  # Red color for channel deletion
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Deleted by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"CHID: {channel.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        break


# TODO: Fix channel permission updates
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
            color=0x3DA5D9,  # Blue color for channel updates
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
            color=0x000000,  # Default color for role creation
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


@mod_logs.listener(hikari.RoleDeleteEvent)
async def on_delete_role(event: hikari.RoleDeleteEvent) -> None:
    """Role deletion logging"""
    role = event.old_role

    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=role.guild_id, event_type=hikari.AuditLogEventType.ROLE_DELETE
    ):
        member = list(entry.users.values())[0]

        embed = hikari.Embed(
            title="Role Deleted",
            color=(
                role.color if role.color else 0x000000
            ),  # Default color for role deletion if role has no color
            description=f"{const.EMOJI_DELETE} A role `{role.name}` was deleted",
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Deleted by {member.username} ({member.id})",
            icon=member.display_avatar_url,
        )
        embed.set_footer(text=f"RID: {role.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        break


# TODO: Fix role permission changes
@mod_logs.listener(hikari.RoleUpdateEvent)
async def on_role_update(event: hikari.RoleUpdateEvent) -> None:
    """Role update logging"""
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
            color=new_role.color,  # Default color for role updates if role has no color
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


@mod_logs.listener(hikari.MemberUpdateEvent)
async def on_member_update(event: hikari.MemberUpdateEvent) -> None:
    """Member update logging"""
    old_member = event.old_member
    new_member = event.member

    # Timeout logging
    if (
        old_member.communication_disabled_until()
        != new_member.communication_disabled_until()
    ):
        disabled_until = new_member.communication_disabled_until()

        async for entry in mod_logs.bot.rest.fetch_audit_log(
            guild=event.guild_id, event_type=hikari.AuditLogEventType.MEMBER_UPDATE
        ):
            for entry in entry.entries.values():
                if entry.action_type == hikari.AuditLogEventType.MEMBER_UPDATE:
                    if entry.target_id == event.user_id:
                        moderator = await entry.fetch_user()
                        if moderator:
                            reason = (
                                entry.reason if entry.reason else "No reason provided"
                            )
                            if disabled_until is None:
                                embed = hikari.Embed(
                                    title="Member Timeout Removed",
                                    description=f"{const.EMOJI_TIMEOUT} A member {event.user.mention} has had their timeout removed",
                                    color=0xFABD2F,  # Yellow color for member timeout removal
                                    timestamp=datetime.now().astimezone(),
                                )
                                embed.add_field(
                                    name="Reason:", value=reason, inline=False
                                )
                                embed.set_author(
                                    name=f"Removed by {moderator.username} ({moderator.id})",
                                    icon=moderator.display_avatar_url,
                                )
                                embed.set_footer(text=f"UID: {event.user.id}")
                                await mod_logs.bot.rest.create_message(
                                    MOD_CH, embed=embed
                                )
                                return
                            else:
                                description = (
                                    f"{const.EMOJI_TIMEOUT} A member {event.user.mention} "
                                    f"has been timed out until {format_dt(disabled_until)} "
                                    f"({format_dt(disabled_until, style='R')})"
                                )
                                embed = hikari.Embed(
                                    title="Member Updated ",
                                    description=description,
                                    color=0xFABD2F,  # Yellow color for member timeout
                                    timestamp=datetime.now().astimezone(),
                                )
                                embed.add_field(
                                    name="Reason:", value=reason, inline=False
                                )
                                embed.set_author(
                                    name=f"Timed out by {moderator.username} ({moderator.id})",
                                    icon=moderator.display_avatar_url,
                                )
                                embed.set_footer(text=f"UID: {event.user.id}")
                                await mod_logs.bot.rest.create_message(
                                    MOD_CH, embed=embed
                                )
                            break

    updates = []

    if old_member.nickname != new_member.nickname:
        old_nickname = (
            old_member.nickname if old_member.nickname is not None else "None"
        )
        new_nickname = (
            new_member.nickname if new_member.nickname is not None else "None"
        )
        updates.append(("Nickname", old_nickname, new_nickname))
    if old_member.role_ids != new_member.role_ids:
        roles = await event.get_guild().fetch_roles()
        roles = helpers.sort_roles(roles)

        before_roles = [
            f"<@&{role.id}>"
            for role in roles
            if role.id in old_member.role_ids and role.id != new_member.guild_id
        ]
        after_roles = [
            f"<@&{role_id}>"
            for role_id in new_member.role_ids
            if role_id != new_member.guild_id
        ]

        before_roles_str = " ".join(before_roles) if before_roles else "None"

        added_roles = [role for role in after_roles if role not in before_roles]
        removed_roles = [role for role in before_roles if role not in after_roles]

        if added_roles:
            updates.append(("Add Roles", before_roles_str, added_roles[0]))
        if removed_roles:
            updates.append(("Remove Roles", before_roles_str, removed_roles[0]))

    if updates:
        update_types = [update[0] for update in updates]
        update_type = ", ".join(update_types)

        embed = hikari.Embed(
            title=f"Member Updated ({update_type})",
            description=f"{const.EMOJI_INFO} A member {new_member.mention} was updated",
            color=0x9B72CF,  # Purple color for member updates
            timestamp=datetime.now().astimezone(),
        )
        for update in updates:
            embed.add_field(name="Before:", value=update[1], inline=False)
            embed.add_field(name="After:", value=update[2], inline=False)
            footer = (
                f"RID: {update[2].split('@&')[1][:-1]}"
                if update_type != "Nickname"
                else f"UID: {new_member.id}"
            )
        embed.set_author(
            name=f"Updated by {new_member.username} ({new_member.id})",
            icon=new_member.display_avatar_url,
        )
        embed.set_footer(text=footer)
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
        return


@mod_logs.listener(hikari.BanCreateEvent)
async def on_user_ban(event: hikari.BanCreateEvent) -> None:
    """Member ban logging"""
    ban_info = await event.fetch_ban()
    ban_reason = ban_info.reason if ban_info.reason else "No reason provided"

    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.guild_id, event_type=hikari.AuditLogEventType.MEMBER_BAN_ADD
    ):
        for entry in entry.entries.values():
            if entry.action_type == hikari.AuditLogEventType.MEMBER_BAN_ADD:
                if entry.target_id == ban_info.user.id:
                    moderator = await entry.fetch_user()
                    if moderator:
                        embed = hikari.Embed(
                            title="Member Banned",
                            description=f"{const.EMOJI_BAN} A member {ban_info.user.mention} was banned",
                            color=0xF94833,  # Red color for user bans
                            timestamp=datetime.now().astimezone(),
                        )
                        embed.add_field(name="Reason:", value=ban_reason, inline=False)
                        embed.set_author(
                            name=f"Banned by {moderator.username} ({moderator.id})",
                            icon=moderator.display_avatar_url,
                        )
                        embed.set_footer(text=f"UID: {ban_info.user.id}")
                        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
                    return


@mod_logs.listener(hikari.BanDeleteEvent)
async def on_user_unban(event: hikari.BanDeleteEvent) -> None:
    """Member unban logging"""
    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.guild_id, event_type=hikari.AuditLogEventType.MEMBER_BAN_REMOVE
    ):
        for entry in entry.entries.values():
            if entry.action_type == hikari.AuditLogEventType.MEMBER_BAN_REMOVE:
                if entry.target_id == event.user_id:
                    moderator = await entry.fetch_user()
                    if moderator:
                        reason = entry.reason if entry.reason else "No reason provided"
                        embed = hikari.Embed(
                            title="Member Unbanned",
                            description=f"{const.EMOJI_BAN} A member {event.user.mention} was unbanned",
                            color=0x8EC07C,  # Green color for user unbans
                            timestamp=datetime.now().astimezone(),
                        )
                        embed.add_field(name="Reason:", value=reason, inline=False)
                        embed.set_author(
                            name=f"Unbanned by {moderator.username} ({moderator.id})",
                            icon=moderator.display_avatar_url,
                        )
                        embed.set_footer(text=f"UID: {event.user_id}")
                        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
                    break


@mod_logs.listener(hikari.MemberDeleteEvent)
async def on_user_kick(event: hikari.MemberDeleteEvent) -> None:
    """Member kick logging"""
    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.guild_id, event_type=hikari.AuditLogEventType.MEMBER_KICK
    ):
        for entry in entry.entries.values():
            if entry.action_type == hikari.AuditLogEventType.MEMBER_KICK:
                if entry.target_id == event.user_id:
                    moderator = await entry.fetch_user()
                    if moderator:
                        reason = entry.reason if entry.reason else "No reason provided"
                        embed = hikari.Embed(
                            title="Member Kicked",
                            description=f"{const.EMOJI_KICK} A member {event.user.mention} was kicked",
                            color=0xFE8019,  # Orange color for user kicks
                            timestamp=datetime.now().astimezone(),
                        )
                        embed.add_field(name="Reason:", value=reason, inline=False)
                        embed.set_author(
                            name=f"Kicked by {moderator.username} ({moderator.id})",
                            icon=moderator.display_avatar_url,
                        )
                        embed.set_footer(text=f"UID: {event.user.id}")
                        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
                    break


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mod_logs)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(mod_logs)
