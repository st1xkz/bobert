from typing import Sequence

import hikari

from bobert.core.stuff.langs import CUSTOM_LANGUAGES


def sort_roles(roles: Sequence[hikari.Role]) -> Sequence[hikari.Role]:
    return sorted(roles, key=lambda r: r.position, reverse=True)


def detect_language(input_value):
    input_value = input_value.strip().lower()

    for code, details in CUSTOM_LANGUAGES.items():
        if input_value in [code, details[0].lower(), details[1].lower()]:
            return code

    return None


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
        hikari.Permissions.MENTION_ROLES: "Mention \@everyone, \@here, and All Roles",
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


def get_questions(role: str):
    if role == "Event Planner":
        return [
            (
                "Tell us about yourself.",
                "Introduce yourself. Share your skills, timezone, or any personal details.",
            ),
            (
                "Why do you want to be an Event Planner?",
                "Explain your motivations for wanting this role.",
            ),
            (
                "What experience do you have?",
                "Highlight any relevant experience or skills you possess.",
            ),
            (
                "How would you plan and coordinate events?",
                "Describe your approach to organizing and managing events.",
            ),
            (
                "Ideas or improvements if selected?",
                "Showcase your creativity and commitment to server improvement.",
            ),
        ]
    elif role == "Event Assistant":
        return [
            (
                "Tell us about yourself.",
                "Introduce yourself. Share your skills, timezone, or any personal details.",
            ),
            (
                "Why do you want to be an Event Assistant?",
                "Explain your motivations for wanting this role.",
            ),
            (
                "What experience do you have?",
                "Highlight any relevant experience or skills you possess.",
            ),
            (
                "How would you support event planners?",
                "Describe how you would assist event planners in their duties.",
            ),
            (
                "Ideas or improvements if selected?",
                "Showcase your creativity and commitment to server improvement.",
            ),
        ]
    elif role == "Trainee":
        return [
            (
                "Tell us about yourself.",
                "Introduce yourself. Share your skills, timezone, or any personal details.",
            ),
            (
                "Why do you want to be a Trainee?",
                "Explain your motivations for wanting this role.",
            ),
            (
                "What experience do you have?",
                "Highlight any relevant experience or skills you possess.",
            ),
            (
                "How would you handle conflict in the server?",
                "Put yourself in a scenario where your problem-solving and conflict resolution skills are used.",
            ),
            (
                "Ideas or improvements if selected?",
                "Showcase your creativity and commitment to server improvement.",
            ),
        ]
    else:
        return []


def get_acceptance_message(role: str):
    if role == "Event Planner":
        return {
            "title": "Congratulations! Your Event Planner Application has been Approved!",
            "description": """
Hello {user},

We're thrilled to inform you that your application for the Event Planner role has been approved! 🎉
            """,
            "fields": [
                {
                    "name": "What to Expect:",
                    "value": """
- You'll receive the **Event Planner** role shortly, granting you access to event planning channels and permissions.
- Our team will provide you with all the necessary tools and guidance to host engaging events for the community.
""",
                },
                {
                    "name": "Next Steps:",
                    "value": """
- Be ready to plan and execute amazing events that bring joy to our members.
- If you have any questions or need support, feel free to contact our staff team.

We look forward to seeing the fantastic events you'll create!

Best,
Sage Events Team
""",
                },
            ],
        }
    elif role == "Event Assistant":
        return {
            "title": "Congratulations! Your Event Assistant Application has been Approved!",
            "description": """
Hello {user},

We're thrilled to inform you that your application for the Event Assistant role has been approved! 🎉
""",
            "fields": [
                {
                    "name": "What to Expect:",
                    "value": """
- You'll receive the **Event Assistant** role, allowing you to assist in event planning and execution.
- You'll work closely with Event Planners and other team members to ensure events run smoothly.
                 """,
                },
                {
                    "name": "Next Steps:",
                    "value": """
- Be prepared to support event planners and contribute to the success of our events.
- Our team is here to help you succeed, so don't hesitate to ask for guidance.

We're excited to have you on board and look forward to your contributions!

Best,
Sage Events Team
""",
                },
            ],
        }
    elif role == "Trainee":
        return {
            "title": "Congratulations! Your Trainee Application has been Approved!",
            "description": """
Hello {user},

We're thrilled to inform you that your application for the Trainee role has been approved! 🎉
""",
            "fields": [
                {
                    "name": "What to Expect:",
                    "value": """
- You'll receive the **Trainees** role shortly, granting you access to staff-exclusive channels and trainee-specific privileges.
- Our staff team will reach out to provide additional information about your role and responsibilities during the training period.
- Please review our server guidelines and familiarize yourself with our rules to maintain a positive and welcoming community.
""",
                },
                {
                    "name": "Training Period:",
                    "value": """
- As a Trainee, you'll have the opportunity to learn and grow within our staff team. We'll provide guidance and mentorship to help you succeed.
- During your training, you'll work closely with experienced staff members and gain valuable experience in server moderation.
""",
                },
                {
                    "name": "Next Steps:",
                    "value": """
- Be prepared to contribute positively to our server and help us maintain a friendly environment.
- If you have any questions or need assistance, feel free to reach out to a staff member.

Congratulations once again, and welcome aboard! We are thrilled to have you join our team and are eager to see you thrive in your new role.

Best,
Sage Staff Team
""",
                },
            ],
        }
    else:
        return {
            "title": "Role Not Found",
            "description": "The specified role does not match any known role.",
            "fields": [],
        }


def get_rejection_message(role: str):
    if role == "Event Planner":
        return {
            "title": "Regarding Your Event Planner Application",
            "description": """
Hello {user},

Thank you for your interest in joining as an Event Planner and for taking the time to submit your application.

At this time, we have decided not to move forward with your application. We understand this may be disappointing, but please know that this decision does not reflect your worth as a member of our community.
""",
            "fields": [
                {
                    "name": "Potential Opportunities",
                    "value": """
While the Event Planner position may not be available right now, you can still contribute and gain valuable experience:
- Assist with Community Events: Volunteer to help with smaller community events or activities. This will allow you to demonstrate your event planning skills and enthusiasm.
- Engage in Community Projects: Participate in server-wide projects or initiatives to build connections and gain relevant experience.
- Contribute to Other Roles: Explore other roles or responsibilities within the server that align with your interests and skills.

By actively contributing, you'll build a strong profile that could increase your chances of being selected for the Event Planner role in the future.
""",
                },
                {
                    "name": "Feedback",
                    "value": """
We encourage you to review our event planning guidelines and consider reapplying in the future. If you'd like feedback on your application, please reach out to us. We are committed to providing constructive feedback to help you enhance your application for future opportunities.
""",
                },
                {
                    "name": "Reapplying:",
                    "value": """
We encourage you to stay active and positive within our community. Opportunities to join our team may arise in the future, and we'd be glad to consider your application again.

If you have any questions or need further information, please reach out to a staff member.

Thank you for your understanding and for being a valuable part of our community.

Best,
Sage Events Team
""",
                },
            ],
        }
    elif role == "Event Assistant":
        return {
            "title": "Regarding Your Event Assistant Application",
            "description": """
Hello {user}, 

Thank you for your interest in joining as an Event Assistant and for taking the time to submit your application.

At this time, we have decided not to move forward with your application. We understand this may be disappointing, but please know that this decision does not reflect your worth as a member of our community.
""",
            "fields": [
                {
                    "name": "Potential Opportunities",
                    "value": """
While the Event Assistant position may not be available right now, you can still contribute and gain valuable experience:
- Support Community Initiatives: Help with ongoing server projects or activities to showcase your skills and dedication.
- Engage in Community Discussions: Actively participate in server discussions and activities to build your presence and demonstrate your enthusiasm.
- Contribute to Other Roles: Explore other roles or responsibilities within the server that align with your interests and skills.

By actively contributing, you’ll build a strong profile that could increase your chances of being selected for the Event Assistant role in the future.
""",
                },
                {
                    "name": "Feedback",
                    "value": """
We encourage you to review our event assisting guidelines and consider reapplying in the future. If you'd like feedback on your application, please reach out to us. We are committed to providing constructive feedback to help you enhance your application for future opportunities.
""",
                },
                {
                    "name": "Reapplying:",
                    "value": """
We encourage you to stay active and positive within our community. Opportunities to join our team may arise in the future, and we'd be glad to consider your application again.

If you have any questions or need further information, please reach out to a staff member.

Thank you for your understanding and for being a valuable part of our community.

Best,
Sage Events Team
""",
                },
            ],
        }
    elif role == "Trainee":
        return {
            "title": "Regarding Your Trainee Application",
            "description": """
Hello {user},

Thank you for your interest in joining as a Trainee and for taking the time to submit your application.

At this time, we have decided not to move forward with your application. We understand this may be disappointing, but please know that this decision does not reflect your worth as a member of our community.
""",
            "fields": [
                {
                    "name": "Potential Opportunities",
                    "value": """
While the Trainee position may not be available right now, you can still contribute and gain valuable experience:
- Volunteer for Community Tasks: Help with various server activities or moderation tasks to demonstrate your commitment and readiness.
- Engage Actively in Feedback Sessions: Participate actively in feedback sessions to provide valuable insights on how the server can improve.
- Contribute to Other Roles: Explore other roles or responsibilities within the server that align with your interests and skills.

By actively contributing, you’ll build a strong profile that could increase your chances of being selected for the Trainee role in the future.
""",
                },
                {
                    "name": "Feedback",
                    "value": """
We encourage you to review our trainee guidelines and consider reapplying in the future. If you'd like feedback on your application, please reach out to us. We are committed to providing constructive feedback to help you enhance your application for future opportunities.
""",
                },
                {
                    "name": "Reapplying",
                    "value": """
We encourage you to stay active and positive within our community. Opportunities to join our team may arise in the future, and we'd be glad to consider your application again.

If you have any questions or need further information, please reach out to a staff member.

Thank you for your understanding and for being a valuable part of our community.

Best,
Sage Staff Team
""",
                },
            ],
        }
    else:
        return {
            "title": "Role Not Found",
            "description": "The specified role does not match any known role.",
            "fields": [],
        }
