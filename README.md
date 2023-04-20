# Minecraft Bot Controller

This is a Python script that allows you to control a Minecraft bot via the Mineflayer API. You can send commands to the bot in JavaScript using a Node.js script and a named pipe.

## Requirements

- Python 3
- Node.js
- openai
- win32pipe
- win32file
- Mineflayer

## Explanation
- The Python script will create a named pipe called `Foo` and wait for a client to connect.
- The Node.js script will connect to the pipe and start a Minecraft bot using Mineflayer.
- You can send commands to the bot by using in game chat
- The Python script will read the commands from the pipe and use openai to generate a preprompt for the bot.
- The preprompt will be something like this:You are controlling a minecraft bot via the mineflayer api.Only reply in java script with mineflayer funcions in the order they should be executed To complete The goal
- The goal will be based on the blocks and entities around the bot, which are filtered by the Node.js script.
- The Python script will append the preprompt to the command and use openai to generate a response for the bot.
- The response will be something like this:bot.crouch() bot.dig(block) bot.uncrouch() bot.placeBlock(block, vec3(0, 1, 0))
- The Python script will send the response back to the Node.js script via the pipe.
- The Node.js script will execute the response using eval().
