CREATE TABLE chat_gpt_messages (
    message_id SERIAL PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    sender_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL
);