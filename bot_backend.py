import json
import subprocess
import openai
import re
import threading
import win32pipe, win32file

openai.api_key = ""
node_path = 'C:\\Program Files\\nodejs\\node.exe'
node_script = 'bot_Front_end.js'

PIPE_NAME = r'\\.\pipe\Foo'

pipe = win32pipe.CreateNamedPipe(
    PIPE_NAME,
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    0,
    None
)

# Start the Node.js process and redirect its stderr stream to the stderr stream of the Python process
node_process = subprocess.Popen([node_path, node_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def print_output(process):
    while True:
        output = process.stdout.readline()
        if not output:
            break
        output_str = output.decode('utf-8').strip()
        if output_str.startswith('DATA:'):
            data = json.loads(output_str[5:])
            # process data
        else:
            print(output_str)
            

t = threading.Thread(target=print_output, args=(node_process,))
t.start()

print("waiting for client")
win32pipe.ConnectNamedPipe(pipe, None)
print("got client")

def extract_code(text):
    pattern = r'```(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1)
        return code
    else:
        return text
x = 0
while True:
    
    print(x)
    x += 1
    response = node_process.stdout.readline()
    if not response:
        print('not responce')
        break
    if response.startswith(b'DATA:'):
        data = json.loads(response[5:].decode('utf-8'))
        blocks = data['blocks']
        filtered_entities = data['filtered_entities']
        message = data['message']
        preprompt = 'You are controlling a minecraft bot via the mineflayer api.Only reply in java script with mineflayer funcions in the order they should be executed To complete The goal set by The user. You will also be provied with some conext of The surrounding blocks and entities.'
        message_history = []
        message_history.append({"role": "system", "content": preprompt})
        message_history.append({"role": "user", "content": str(blocks)})
        message_history.append({"role": "user", "content": str(filtered_entities)})
        message_history.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=message_history
                    )
        response2 = response['choices'][0]['message']['content']
        print('bot reply',response2)
        # Parse the actions specified in the response
        code = extract_code(response2)
        if code is None:
            print('No code found in response')
        else:
            print(f"writing message")
            win32file.WriteFile(pipe, code.encode())
            print('code sent')