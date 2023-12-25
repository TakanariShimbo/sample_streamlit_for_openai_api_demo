CREATE TABLE chat_rooms (
    room_serial SERIAL PRIMARY KEY,
    room_id VARCHAR(255) UNIQUE NOT NULL,
    room_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

CREATE TABLE chat_messages (
    message_serial SERIAL PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    sender_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES chat_rooms (room_id) ON DELETE CASCADE
);
