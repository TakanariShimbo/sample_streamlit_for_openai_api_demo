-- CREATE TABLE accounts (
--     account_id VARCHAR(255) PRIMARY KEY,
--     password VARCHAR(255) NOT NULL,
-- );

CREATE TABLE chat_rooms (
    room_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
);

CREATE TABLE chat_messages (
    message_serial SERIAL PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id) ON DELETE CASCADE,
);

-- CREATE TABLE chat_messages (
--     message_serial SERIAL PRIMARY KEY,
--     room_id VARCHAR(255) NOT NULL,
--     account_id VARCHAR(255) NOT NULL,
--     role VARCHAR(255) NOT NULL,
--     content TEXT NOT NULL,
--     FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id) ON DELETE CASCADE,
--     FOREIGN KEY (account_id) REFERENCES message_senders (account_id)
-- );

