import asyncio
import io
import os
import typing
from collections import deque
from datetime import datetime, timedelta, timezone

import hikari
import hikari.audit_logs
import lightbulb

from bobert.core.utils import chron
from bobert.core.utils import constants as const
from bobert.core.utils import helpers

mod_logs = lightbulb.Plugin("mod-logs")

"""
TODO:
List of things to fix and/or add
- Fix type check errors
- purge-only channels
- specific channels to not log

(Scroll down this file to see if there are any FIXME tags)
"""


async def get_audit_log_entry(
    bot: hikari.GatewayBot,
    guild_id: hikari.Snowflake,
    target_id: hikari.Snowflake,
    action_type: hikari.AuditLogEventType,
    time_window: int = 5,  # Seconds
) -> hikari.AuditLogEntry | None:
    """
    Fetches recent audit log entries of a specific type for a target
    and returns the audit log entry within the time window.
    """
    await asyncio.sleep(5)
    now = datetime.now(timezone.utc)

    async for log in bot.rest.fetch_audit_log(guild=guild_id, event_type=action_type):
        for entry in log.entries.values():
            entry_time = entry.id.created_at
            time_difference = (now - entry_time).total_seconds()

            if entry.target_id == target_id and time_difference <= time_window:
                return entry

    return None


# Test server IDs
MOD_CH = 993698032463925398
GUILD_ID = 993565814517141514


######################
# ----- Events ----- #
######################


@mod_logs.listener(hikari.GuildMessageDeleteEvent)
async def on_deleted_message(event: hikari.GuildMessageDeleteEvent) -> None:
    EXCLUDED_CH = [806649868314869760]

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID or (
        event.get_channel() and event.get_channel().id in EXCLUDED_CH
    ):
        return

    message = event.old_message
    if message is None:
        return

    member_id = message.author.id if message.author else None
    member = (
        await event.app.rest.fetch_member(event.guild_id, member_id)
        if member_id
        else None
    )

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=member_id,
        action_type=hikari.AuditLogEventType.MESSAGE_DELETE,
        time_window=10,  # Adjust as needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        embed = hikari.Embed(
            title="Message Deleted",
            description=f"{const.EMOJI_DELETE} A message from {member.mention if member else 'Unknown User'} was deleted in <#{event.get_channel().id if event.get_channel() else 'Unknown Channel'}>",
            color=0xF94833,
            timestamp=datetime.now().astimezone(),
        )
        if getattr(message, "content", "").strip():
            embed.add_field(name="Content:", value=message.content, inline=False)
        if message.attachments:
            embed.add_field(
                name="Attachments:",
                value="This message contained one or more attachments",
                inline=False,
            )
        if message.stickers:
            embed.add_field(
                name="Stickers:",
                value="This message contained a sticker",
                inline=False,
            )
        embed.set_author(
            name=f"Deleted by {moderator.username} ({moderator.id})",
            icon=moderator.display_avatar_url if moderator else None,
        )
        embed.set_footer(text=f"MID: {message.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)
    else:
        embed = hikari.Embed(
            title="Message Deleted",
            description=f"{const.EMOJI_DELETE} A message was deleted in <#{event.get_channel().id if event.get_channel() else 'Unknown Channel'}>",
            color=0xF94833,
            timestamp=datetime.now().astimezone(),
        )
        if message.content and message.content.strip():
            embed.add_field(name="Content:", value=message.content, inline=False)
        if message.attachments:
            embed.add_field(
                name="Attachments:",
                value="This message contained one or more attachments",
                inline=False,
            )
        if message.stickers:
            embed.add_field(
                name="Stickers:",
                value="This message contained a sticker",
                inline=False,
            )
        embed.set_author(
            name=(
                f"Deleted by {member.username} ({member.id})"
                if member
                else "Unknown User"
            ),
            icon=member.display_avatar_url if member else None,
        )
        embed.set_footer(text=f"MID: {message.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


@mod_logs.listener(hikari.GuildBulkMessageDeleteEvent)
async def on_bulk_deleted_message(event: hikari.GuildBulkMessageDeleteEvent) -> None:
    """Bulk message deletion logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    msg_info = []

    for message_id, message in event.old_messages.items():
        if message:
            member = await event.app.rest.fetch_member(
                event.guild_id, message.author.id
            )
            if member:
                msg_data = f"[{message.created_at.strftime('%b %d %Y %H:%M:%S')}] "
                msg_data += f"{member.username}#{member.discriminator} - ({member.id}) "
                msg_data += f"[{message_id}]: "
                msg_data += f"{message.content}\n"
                msg_info.append(msg_data)

    msg_info_str = "\n".join(msg_info)

    bytes_data = msg_info_str.encode("utf-8")

    embed = hikari.Embed(
        title="Bulk Messages Deleted",
        description=f"{const.EMOJI_DELETE} **{len(event.message_ids)}** messages were deleted in <#{event.channel_id}>. See the attached file for details.",
        color=0xFE8019,  # Orange color for message bulk deletes
        timestamp=datetime.now().astimezone(),
    )
    file_data = hikari.Bytes(bytes_data, "bulk_delete.txt")
    await mod_logs.bot.rest.create_message(MOD_CH, embed=embed, attachment=file_data)


@mod_logs.listener(hikari.GuildMessageUpdateEvent)
async def on_edited_message(event: hikari.GuildMessageUpdateEvent) -> None:
    """Edited message logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

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
        return


@mod_logs.listener(hikari.VoiceStateUpdateEvent)
async def on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    """Voice channel activity logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    user_id = event.state.user_id
    old_ch_id = event.old_state.channel_id if event.old_state else None
    new_ch_id = event.state.channel_id

    # Check if the user has moved to a different voice channel
    if old_ch_id != new_ch_id:
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
    """Channel/category creation logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

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

    title = "Channel Created"
    if channel.type is hikari.ChannelType.GUILD_CATEGORY:
        title = "Category Created"

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=channel.id,
        action_type=hikari.AuditLogEventType.CHANNEL_CREATE,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        embed = hikari.Embed(
            title=title,
            description=f"A new {channel.type.name.split('_')[-1].lower()} {emoji} channel `{channel.name}` was created",
            color=0x8EC07C,  # Green color for channel creation
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Created by {moderator.username} ({moderator.id})",
            icon=moderator.display_avatar_url,
        )
        embed.set_footer(text=f"CHID: {channel.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


@mod_logs.listener(hikari.GuildChannelDeleteEvent)
async def on_channel_delete(event: hikari.GuildChannelDeleteEvent) -> None:
    """Channel/category deletion logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

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

    title = "Channel Deleted"
    if channel.type is hikari.ChannelType.GUILD_CATEGORY:
        title = "Category Deleted"

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=channel.id,
        action_type=hikari.AuditLogEventType.CHANNEL_DELETE,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        embed = hikari.Embed(
            title=title,
            description=f"{const.EMOJI_DELETE} A {channel.type.name.split('_')[-1].lower()} {emoji} channel `{channel.name}` was deleted",
            color=0xF94833,  # Red color for channel deletion
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Deleted by {moderator.username} ({moderator.id})",
            icon=moderator.display_avatar_url,
        )
        embed.set_footer(text=f"CHID: {channel.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


# FIXME: Add update_type "Multiple" when multiple changes are saved in one go
# FIXME: Fix update_type display. update_type "Topic" displays incorrectly
@mod_logs.listener(hikari.GuildChannelUpdateEvent)
async def on_channel_update(event: hikari.GuildChannelUpdateEvent) -> None:
    """Channel update logging"""
    if event.guild_id != GUILD_ID:
        return

    old_ch = event.old_channel
    new_ch = event.channel

    if new_ch.position != old_ch.position:
        return

    # Determine emoji based on channel type
    emoji = const.EMOJI_TEXT
    if new_ch.type == hikari.ChannelType.GUILD_VOICE:
        emoji = const.EMOJI_VOICE
    elif new_ch.type == hikari.ChannelType.GUILD_FORUM:
        emoji = const.EMOJI_FORUM
    elif new_ch.type == hikari.ChannelType.GUILD_STAGE:
        emoji = const.EMOJI_STAGE
    elif new_ch.type == hikari.ChannelType.GUILD_CATEGORY:
        emoji = const.EMOJI_CATEGORY

    update_type = None
    update_types = set()
    before = []
    after = []

    description = ""

    perm_type = ""

    perm_names = helpers.get_role_permission_names()
    old_overwrites = old_ch.permission_overwrites
    new_overwrites = new_ch.permission_overwrites

    for overwrite_id, old_overwrite in old_overwrites.items():
        new_overwrite = new_overwrites.get(overwrite_id)
        if new_overwrite is None:
            # Overwrite was removed
            for perm_flag, perm_name in perm_names.items():
                status = (
                    f"{const.EMOJI_NEGATIVE}"
                    if perm_flag in old_overwrite.allow
                    else f"{const.EMOJI_NEUTRAL}"
                )
                before.append(f"{status} : {perm_name}")
        elif (
            new_overwrite.allow != old_overwrite.allow
            or new_overwrite.deny != old_overwrite.deny
        ):
            # Overwrite was changed
            for perm_flag, perm_name in perm_names.items():
                old_status = (
                    f"{const.EMOJI_POSITIVE}"
                    if perm_flag in old_overwrite.allow
                    else (
                        f"{const.EMOJI_NEGATIVE}"
                        if perm_flag in old_overwrite.deny
                        else f"{const.EMOJI_NEUTRAL}"
                    )
                )
                new_status = (
                    f"{const.EMOJI_POSITIVE}"
                    if perm_flag in new_overwrite.allow
                    else (
                        f"{const.EMOJI_NEGATIVE}"
                        if perm_flag in new_overwrite.deny
                        else f"{const.EMOJI_NEUTRAL}"
                    )
                )
                if old_status != new_status:
                    perm_type = (
                        f"`@everyone ({event.get_guild().id})`"
                        if overwrite_id == event.get_guild().id
                        else (
                            f"`{event.get_guild().get_role(overwrite_id)} ({overwrite_id})`"
                            if old_overwrite.type == hikari.PermissionOverwriteType.ROLE
                            else f"`{event.get_guild().get_member(overwrite_id)} ({overwrite_id})`"
                        )
                    )
                    before.append(f"{old_status} : {perm_name}")
                    after.append(f"{new_status} : {perm_name}")

    if before or after:
        update_type = "Permissions"
        description = (
            f"{const.EMOJI_INFO} A {new_ch.type.name.split('_')[-1].lower()} {emoji} channel `{new_ch.name}` was updated "
            f"with changes to {perm_type}"
        )

    if new_ch.name != old_ch.name:
        update_type = "Name"
        before.append(str(old_ch.name))
        after.append(str(new_ch.name))

    if isinstance(new_ch, hikari.GuildTextChannel) or isinstance(
        new_ch, hikari.GuildForumChannel
    ):
        if new_ch.topic != old_ch.topic:
            before_topic = old_ch.topic if old_ch.topic is not None else ""
            after_topic = new_ch.topic if new_ch.topic is not None else ""
            # Only log the topic change if it actually changed
            if before_topic != after_topic:
                update_type = "Topic"
                if old_ch.topic is not None:
                    before.append(before_topic)
                after.append(after_topic)

        if new_ch.rate_limit_per_user != old_ch.rate_limit_per_user:
            update_type = "Slowmode"
            before.append(
                "Off"
                if old_ch.rate_limit_per_user == timedelta(0)
                else chron.short_delta(old_ch.rate_limit_per_user)
            )
            after.append(
                "Off"
                if new_ch.rate_limit_per_user == timedelta(0)
                else chron.short_delta(new_ch.rate_limit_per_user)
            )

    if new_ch.is_nsfw != old_ch.is_nsfw:
        update_type = "NSFW"
        before.append(str(old_ch.is_nsfw))
        after.append(str(new_ch.is_nsfw))

    if isinstance(new_ch, hikari.GuildVoiceChannel) or isinstance(
        new_ch, hikari.GuildStageChannel
    ):
        if new_ch.bitrate != old_ch.bitrate:
            update_type = "Bitrate"
            before.append(f"{old_ch.bitrate // 1000}kbps")
            after.append(f"{new_ch.bitrate // 1000}kbps")

        if new_ch.region != old_ch.region:
            update_type = "Region Override"
            before.append(
                "Automatic" if old_ch.region is None else old_ch.region.capitalize()
            )
            after.append(
                "Automatic" if new_ch.region is None else new_ch.region.capitalize()
            )

        if new_ch.user_limit != old_ch.user_limit:
            update_type = "User Limit"
            before.append(
                "No Limit" if old_ch.user_limit == 0 else f"{old_ch.user_limit} users"
            )
            after.append(
                "No Limit" if new_ch.user_limit == 0 else f"{old_ch.user_limit} users"
            )

        if new_ch.video_quality_mode != old_ch.video_quality_mode:
            update_type = "Video Quality"
            before.append(
                "Auto"
                if old_ch.video_quality_mode == hikari.VideoQualityMode.AUTO
                else "720p"
            )
            after.append(
                "Auto"
                if new_ch.video_quality_mode == hikari.VideoQualityMode.AUTO
                else "720p"
            )

    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.get_guild(), event_type=hikari.AuditLogEventType.CHANNEL_UPDATE
    ):
        member = list(entry.users.values())[0]

        embed = hikari.Embed(
            title=f"Channel Updated ({update_type})",
            description=(
                description
                if update_type == "Permissions"
                else f"{const.EMOJI_INFO} A {new_ch.type.name.split('_')[-1].lower()} {emoji} channel `{new_ch.name}` was updated"
            ),
            color=0x3DA5D9,  # Blue color for channel updates
            timestamp=datetime.now().astimezone(),
        )
        if before and after:
            if update_type == "Permissions":
                if before:
                    embed.add_field(
                        name="Before:", value="\n".join(before), inline=False
                    )
                if after:
                    embed.add_field(name="After:", value="\n".join(after), inline=False)
            else:
                if before:
                    embed.add_field(
                        name="Before:",
                        value="\n".join(before),
                        inline=False,
                    )
                if after:
                    embed.add_field(name="After:", value="\n".join(after), inline=False)
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

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    role = event.role

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=role.id,
        action_type=hikari.AuditLogEventType.ROLE_CREATE,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        embed = hikari.Embed(
            title="Role Created",
            color=0x000000,  # Default color for role creation
            description=f"A new role `{role.name}` was created",
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Created by {moderator.username} ({moderator.id})",
            icon=moderator.display_avatar_url,
        )
        embed.set_footer(text=f"RID: {role.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


@mod_logs.listener(hikari.RoleDeleteEvent)
async def on_delete_role(event: hikari.RoleDeleteEvent) -> None:
    """Role deletion logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    role = event.old_role

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=role.id,
        action_type=hikari.AuditLogEventType.ROLE_DELETE,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        embed = hikari.Embed(
            title="Role Deleted",
            color=(
                role.color if role.color else 0x000000
            ),  # Default color for role deletion if role has no color
            description=f"{const.EMOJI_DELETE} A role `{role.name}` was deleted",
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Deleted by {moderator.username} ({moderator.id})",
            icon=moderator.display_avatar_url,
        )
        embed.set_footer(text=f"RID: {role.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)


# FIXME: Fix role permission changes
@mod_logs.listener(hikari.RoleUpdateEvent)
async def on_role_update(event: hikari.RoleUpdateEvent) -> None:
    """Role update logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    old_role = event.old_role
    new_role = event.role

    update_type = None
    before = []
    after = []

    perm_type = ""

    perm_names = helpers.get_role_permission_names()
    old_overwrites = old_role.permissions
    new_overwrites = new_role.permissions

    for overwrite_id, old_overwrite in old_overwrites.items():
        new_overwrite = new_overwrites.get(overwrite_id)
        if new_overwrite is None:
            # Overwrite was removed
            for perm_flag, perm_name in perm_names.items():
                status = (
                    f"{const.EMOJI_NEGATIVE}"
                    if perm_flag in old_overwrite.allow
                    else f"{const.EMOJI_NEUTRAL}"
                )
                before.append(f"{status} : {perm_name}")
        elif (
            new_overwrite.allow != old_overwrite.allow
            or new_overwrite.deny != old_overwrite.deny
        ):
            # Overwrite was changed
            for perm_flag, perm_name in perm_names.items():
                old_status = (
                    f"{const.EMOJI_POSITIVE}"
                    if perm_flag in old_overwrite.allow
                    else (
                        f"{const.EMOJI_NEGATIVE}"
                        if perm_flag in old_overwrite.deny
                        else f"{const.EMOJI_NEUTRAL}"
                    )
                )
                new_status = (
                    f"{const.EMOJI_POSITIVE}"
                    if perm_flag in new_overwrite.allow
                    else (
                        f"{const.EMOJI_NEGATIVE}"
                        if perm_flag in new_overwrite.deny
                        else f"{const.EMOJI_NEUTRAL}"
                    )
                )
                if old_status != new_status:
                    perm_type = (
                        f"`@everyone ({event.get_guild().id})`"
                        if overwrite_id == event.get_guild().id
                        else (
                            f"`{event.get_guild().get_role(overwrite_id)} ({overwrite_id})`"
                            if old_overwrite.type == hikari.PermissionOverwriteType.ROLE
                            else f"`{event.get_guild().get_member(overwrite_id)} ({overwrite_id})`"
                        )
                    )
                    before.append(f"{old_status} : {perm_name}")
                    after.append(f"{new_status} : {perm_name}")

    if before or after:
        update_type = "Permissions"
        description = (
            f"{const.EMOJI_INFO} A {new_ch.type.name.split('_')[-1].lower()} {emoji} channel `{new_ch.name}` was updated "
            f"with changes to {perm_type}"
        )

    if new_role.name != old_role.name:
        update_type = "Name"
        before.append(old_role.name)
        after.append(new_role.name)

    if new_role.color != old_role.color:
        update_type = "Color"
        before.append(f"#{old_role.color:06X}")
        after.append(f"#{new_role.color:06X}")

    if new_role.is_mentionable != old_role.is_mentionable:
        update_type = "Mentionable"
        before.append(old_role.is_mentionable)
        after.append(new_role.is_mentionable)

    if new_role.is_hoisted != old_role.is_hoisted:
        update_type = "Hoisted"
        before.append(old_role.is_hoisted)
        after.append(new_role.is_hoisted)

    # Check if permission changes are present in the audit log
    async for entry in mod_logs.bot.rest.fetch_audit_log(
        guild=event.guild_id, event_type=hikari.AuditLogEventType.ROLE_UPDATE
    ):
        member = list(entry.users.values())[0]

    embed = hikari.Embed(
        title=f"Role Updated ({update_type})",
        description=f"{const.EMOJI_INFO} A role `{new_role.name}` was updated",
        color=new_role.color,
        timestamp=datetime.now().astimezone(),
    )
    embed.add_field(name="Before:", value="\n".join(before), inline=False)
    embed.add_field(name="After:", value="\n".join(after), inline=False)

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

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    old_member = event.old_member
    new_member = event.member

    if new_member is None:
        return

    old_nickname = old_member.nickname if old_member else None
    new_nickname = new_member.nickname

    # Handle Nickname Changes
    if old_nickname != new_nickname:
        moderator_usn = "Unknown"
        moderator = None
        log_entry_1 = await get_audit_log_entry(
            mod_logs.bot,
            event.guild_id,
            target_id=new_member.id,
            action_type=hikari.AuditLogEventType.MEMBER_UPDATE,
            time_window=10,  # Adjust if needed
        )
        if log_entry_1:
            moderator = await log_entry_1.fetch_user()
            moderator_usn = f"{moderator.username} ({moderator.id})"
        embed = hikari.Embed(
            title="Member Updated (Nickname)",
            description=f"{const.EMOJI_INFO} A member {new_member.mention} was updated",
            color=0x9B72CF,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(
            name="Before:", value=old_nickname if old_nickname else "None", inline=False
        )
        embed.add_field(
            name="After:", value=new_nickname if new_nickname else "None", inline=False
        )
        embed.set_author(
            name=f"Updated by {moderator_usn}",
            icon=moderator.display_avatar_url if moderator else None,
        )
        embed.set_footer(text=f"UID: {new_member.id}")
        await mod_logs.bot.rest.create_message(MOD_CH, embed=embed)

    # Handle Role Changes
    if old_member.role_ids != new_member.role_ids:
        log_entry_2 = await get_audit_log_entry(
            mod_logs.bot,
            event.guild_id,
            target_id=new_member.id,
            action_type=hikari.AuditLogEventType.MEMBER_ROLE_UPDATE,
            time_window=10,
        )
        if log_entry_2:
            moderator = await log_entry_2.fetch_user()
            moderator_usn = f"{moderator.username} ({moderator.id})"

            guild = event.get_guild()
            if guild is None:
                return

            roles = await guild.fetch_roles()
            roles = helpers.sort_roles(roles)

            before_roles = [
                f"<@&{role.id}>"
                for role in roles
                if role.id in old_member.role_ids and role.id != new_member.guild_id
            ]
            before_roles_str = " ".join(before_roles) if before_roles else "None"

            added_roles_ids = [
                role_id
                for role_id in new_member.role_ids
                if role_id not in old_member.role_ids and role_id != new_member.guild_id
            ]
            removed_roles_ids = [
                role_id
                for role_id in old_member.role_ids
                if role_id not in new_member.role_ids and role_id != new_member.guild_id
            ]

            added_roles_mentions = [f"<@&{role_id}>" for role_id in added_roles_ids]
            removed_roles_mentions = [f"<@&{role_id}>" for role_id in removed_roles_ids]

            if added_roles_mentions:
                added_roles_str = " ".join(added_roles_mentions)
                embed_add = hikari.Embed(
                    title="Member Updated (Add Roles)",
                    description=f"{const.EMOJI_INFO} A member {new_member.mention} was updated",
                    color=0x9B72CF,
                    timestamp=datetime.now().astimezone(),
                )
                embed_add.add_field(
                    name="Before:", value=before_roles_str, inline=False
                )
                embed_add.add_field(name="Added:", value=added_roles_str, inline=False)
                embed_add.set_author(
                    name=f"Updated by {moderator_usn}",
                    icon=moderator.display_avatar_url if moderator else None,
                )
                if added_roles_ids:
                    footer_text = f"RID: {added_roles_ids[0]}"
                    if len(added_roles_ids) > 1:
                        footer_text += f" +{len(added_roles_ids) - 1} more"
                    embed_add.set_footer(text=footer_text)
                    await mod_logs.bot.rest.create_message(MOD_CH, embed=embed_add)

            if removed_roles_mentions:
                removed_roles_str = " ".join(removed_roles_mentions)
                embed_remove = hikari.Embed(
                    title="Member Updated (Remove Roles)",
                    description=f"{const.EMOJI_INFO} A member {new_member.mention} was updated",
                    color=0x9B72CF,
                    timestamp=datetime.now().astimezone(),
                )
                embed_remove.add_field(
                    name="Before:", value=before_roles_str, inline=False
                )
                embed_remove.add_field(
                    name="Removed:", value=removed_roles_str, inline=False
                )
                embed_remove.set_author(
                    name=f"Updated by {moderator_usn}",
                    icon=moderator.display_avatar_url if moderator else None,
                )
                if removed_roles_ids:
                    footer_text = f"RID: {removed_roles_ids[0]}"
                    if len(removed_roles_ids) > 1:
                        footer_text += f" +{len(removed_roles_ids) - 1} more"
                    embed_remove.set_footer(text=footer_text)
                    await mod_logs.bot.rest.create_message(MOD_CH, embed=embed_remove)


@mod_logs.listener(hikari.BanCreateEvent)
async def on_user_ban(event: hikari.BanCreateEvent) -> None:
    """Member ban logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    ban_info = await event.fetch_ban()
    ban_reason = ban_info.reason if ban_info.reason else "No reason provided"

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=ban_info.user.id,
        action_type=hikari.AuditLogEventType.MEMBER_BAN_ADD,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
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


@mod_logs.listener(hikari.BanDeleteEvent)
async def on_user_unban(event: hikari.BanDeleteEvent) -> None:
    """Member unban logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=event.user_id,
        action_type=hikari.AuditLogEventType.MEMBER_BAN_REMOVE,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        reason = log_entry.reason if log_entry.reason else "No reason provided"
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


@mod_logs.listener(hikari.MemberDeleteEvent)
async def on_user_kick(event: hikari.MemberDeleteEvent) -> None:
    """Member kick logging"""

    # Ensures the event only runs from the intended server
    if event.guild_id != GUILD_ID:
        return

    log_entry = await get_audit_log_entry(
        mod_logs.bot,
        event.guild_id,
        target_id=event.user_id,
        action_type=hikari.AuditLogEventType.MEMBER_KICK,
        time_window=10,  # Adjust if needed
    )

    if log_entry:
        moderator = await log_entry.fetch_user()
        reason = log_entry.reason if log_entry.reason else "No reason provided"
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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mod_logs)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(mod_logs)
