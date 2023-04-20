const mineflayer = require('mineflayer');
const readline = require('readline');
// Node.js
const net = require('net');

const PIPE_NAME = "\\\\.\\pipe\\Foo";

const socket = new net.Socket();

socket.connect(PIPE_NAME, () => {
    console.log('Connected to pipe.');
});

let BOT_USERNAME = 'bot'
// Create a new bot object
const bot = mineflayer.createBot({
    host: 'localhost',
    port: 25565,
    username: BOT_USERNAME
});
console.log("console.log works!")

bot.on('spawn', () => {
    console.log("Started mineflayer");
    });

// Listen for chat messages
bot.on('chat', (username, message) => {
    // Ignore messages sent by the bot itself
    console.log("test");
    if (username === bot.username) return;
    console.log(username, message);
    let entities = bot.entities;
    let filtered_entities = [];
    let characterCount = 0;
    if (entities != null || entities[1]['name'] != null) {
        for (let x in entities) {
            let filtered_entity = [
                entities[x]['name'],
                entities[x]['position'].x,
                entities[x]['position'].y,
                entities[x]['position'].z,
                entities[x]['velocity'].x,
                entities[x]['velocity'].y,
                entities[x]['velocity'].z
            ];
            filtered_entities.push(filtered_entity);
            characterCount += JSON.stringify(filtered_entity).length;
            if (characterCount >= 1000) {
                break;
            }
        }
    }

    let blocks = [];
    characterCount = 0;
    // Loop over a range of positions around the bot
    for (let d = 0; d <= 5; d++) {
        for (let x = -d; x <= d; x++) {
            for (let y = -d; y <= d; y++) {
                for (let z = -d; z <= d; z++) {
                    if (Math.abs(x) != d && Math.abs(y) != d && Math.abs(z) != d) continue;
                    // Get the block at each position
                    let block = bot.blockAt(bot.entity.position.offset(x, y, z));
                    // Exclude air blocks and other unnecessary information
                    if (block.name != 'air') {
                        // Add only the necessary information about the block to the list of blocks
                        let blockData = [
                            block.name,
                            block.position.x,
                            block.position.y,
                            block.position.z
                        ];
                        blocks.push(blockData);
                        characterCount += JSON.stringify(blockData).length;
                        if (characterCount >= 1000) {
                            break;
                        }
                    }
                }
            }
        }
        if (characterCount >= 1000) {
            break;
        }
    }

    // Send the data to the Python script
    process.stdout.write('DATA:' + JSON.stringify({ blocks, filtered_entities, message }) + '\n')
});


socket.on('data', (data) => {
    eval(data.toString()); // Evaluate Data Received from Pipe as JavaScript Code
});