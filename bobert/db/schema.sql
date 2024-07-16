-- Creation of all tables necessary for the bot to function

CREATE TABLE IF NOT EXISTS tickets
(
    user_id BIGINT,
    channel_id BIGINT
);