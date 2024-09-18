-- Creation of all tables necessary for the bot to function

CREATE TABLE IF NOT EXISTS tickets
(
    user_id BIGINT,
    channel_id BIGINT
);

CREATE TABLE IF NOT EXISTS mutes
(
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    mute_until TIMESTAMPTZ,
    strike_count INT NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, role_id)
)