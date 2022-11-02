import random


# Returns the random email and password based on Discord member's name
def login_generator(member):
    member = member.replace(" ", ".")
    domains = [
        "@aol.com",
        "@gmail.com",
        "@msn.com",
        "@hotmail.com",
        "@icloud.com",
        "@yahoo.com",
        "@aim.com",
        "@netscape.com",
    ]
    ran_email = [
        "hasASmallPeen",
        "LovesBigButts",
        "theFootFetishMaster",
        "herpes_free_since_03",
        "dildoSwaggins",
        "PigBenis481933274",
        "chillin_like_a_villiam_24",
        "AssButt",
        "ChynaIsHot",
        "gl",
    ]
    email_full = member + random.choice(ran_email) + random.choice(domains)
    ran_password = random.choice(
        [
            "PASSWORD",
            "0123456",
            "PA55W0RD",
            "JESUSLOVESME",
            "244466666688888888",
            "111111",
            "hArderDADDY6969",
            "YamaDamaDiRingDikaDingDing",
            "Punches_baby_pandas",
            "peeinyourbutt",
            "HardRock9inch",
            "Turds3",
        ]
    )

    return email_full, ran_password


# Returns a random "common word" from a list of common words
def random_common_word():
    common_words = [
        "oop",
        "yolo",
        "sus",
        "rat",
        "no shot",
        "random",
        "nudes",
        "peen",
        "lol",
        "lady",
    ]
    return random.choice(common_words)


# Random "Last message" from DM
def random_dm():
    messages = [
        "I hope nobody finds my nudes folder",
        "Honestly, I love the way my farts smell.",
        "You'll have to come over and checkout my e-girl bathwater collection.",
        "First of all, how dare you?",
        "What happens in Vegas, stays in Vegas.",
        "This one time at band camp...",
        "I hope blueballs aren\'t real.",
    ]
    return random.choice(messages)
