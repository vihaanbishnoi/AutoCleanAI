from memory_db import init_db, save_chat, get_last_chats

init_db()
save_chat("user", "Hello")
save_chat("assistant", "Hi there")

print(get_last_chats())
