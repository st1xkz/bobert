from typing import Sequence

import hikari


def sort_roles(roles: Sequence[hikari.Role]) -> Sequence[hikari.Role]:
    return sorted(roles, key=lambda r: r.position, reverse=True)


def get_role_permission_names():
    return {
        hikari.Permissions.VIEW_CHANNEL: "View Channels",
        hikari.Permissions.MANAGE_CHANNELS: "Manage Channels",
        hikari.Permissions.MANAGE_ROLES: "Manage Roles",
        hikari.Permissions.CREATE_GUILD_EXPRESSIONS: "Create Expressions",
        hikari.Permissions.VIEW_AUDIT_LOG: "View Audit Log",
        hikari.Permissions.VIEW_GUILD_INSIGHTS: "View Server Insights",
        hikari.Permissions.MANAGE_WEBHOOKS: "Manage Webhooks",
        hikari.Permissions.MANAGE_GUILD: "Manage Server",
        hikari.Permissions.CREATE_INSTANT_INVITE: "Create Invite",
        hikari.Permissions.CHANGE_NICKNAME: "Change Nickname",
        hikari.Permissions.MANAGE_NICKNAMES: "Manage Nicknames",
        hikari.Permissions.KICK_MEMBERS: "Kick Members",
        hikari.Permissions.BAN_MEMBERS: "Ban Members",
        hikari.Permissions.MODERATE_MEMBERS: "Timeout Members",
        hikari.Permissions.SEND_MESSAGES: "Send Messages",
        hikari.Permissions.SEND_MESSAGES_IN_THREADS: "Send Messages in Threads",
        hikari.Permissions.CREATE_PUBLIC_THREADS: "Create Public Threads",
        hikari.Permissions.CREATE_PRIVATE_THREADS: "Create Private Threads",
        hikari.Permissions.EMBED_LINKS: "Embed Links",
        hikari.Permissions.ATTACH_FILES: "Attach Files",
        hikari.Permissions.ADD_REACTIONS: "Add Reactions",
        hikari.Permissions.USE_EXTERNAL_EMOJIS: "Use External Emoji",
        hikari.Permissions.USE_EXTERNAL_STICKERS: "Use External Stickers",
        hikari.Permissions.MENTION_ROLES: "Mention @everyone, @here, and All Roles",
        hikari.Permissions.MANAGE_MESSAGES: "Manage Messages",
        hikari.Permissions.MANAGE_THREADS: "Manage Threads",
        hikari.Permissions.READ_MESSAGE_HISTORY: "Read Message History",
        hikari.Permissions.SEND_TTS_MESSAGES: "Send Text-to-Speech Messages",
        hikari.Permissions.USE_APPLICATION_COMMANDS: "Use Application Commands",
        hikari.Permissions.SEND_VOICE_MESSAGES: "Send Voice Messages",
        hikari.Permissions.CONNECT: "Connect",
        hikari.Permissions.SPEAK: "Speak",
        hikari.Permissions.STREAM: "Video",
        hikari.Permissions.START_EMBEDDED_ACTIVITIES: "Use Activities",
        hikari.Permissions.USE_SOUNDBOARD: "Use Soundboard",
        hikari.Permissions.USE_EXTERNAL_SOUNDS: "Use External Sounds",
        hikari.Permissions.USE_VOICE_ACTIVITY: "Use Voice Activity",
        hikari.Permissions.PRIORITY_SPEAKER: "Priority Speaker",
        hikari.Permissions.MUTE_MEMBERS: "Mute Members",
        hikari.Permissions.DEAFEN_MEMBERS: "Deafen Members",
        hikari.Permissions.MOVE_MEMBERS: "Move Members",
        hikari.Permissions.REQUEST_TO_SPEAK: "Request to Speak",
        hikari.Permissions.CREATE_EVENTS: "Create Events",
        hikari.Permissions.MANAGE_EVENTS: "Manage Events",
        hikari.Permissions.ADMINISTRATOR: "Administrator",
    }
