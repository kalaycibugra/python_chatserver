# python_chatserver
a. Server manages only one room. Any client may register to the chat room at any time by
sending the message "REGISTER<IP:port:nick>"

b. After registration, each registered member can send a message to the room as
"ROOMMSG<message_itself>".

c. Server announces any registered user or any sent message to all the registered parties.
