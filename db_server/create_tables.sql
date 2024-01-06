
CREATE TABLE accounts (
    account_id VARCHAR(255) PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_rooms (
    room_id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    release VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE
);

CREATE TABLE chat_messages (
    message_serial SERIAL PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    sender_id VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id) ON DELETE CASCADE
);
