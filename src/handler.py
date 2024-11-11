import runpod
import requests
import mimetypes
import subprocess
import threading

def stream_reader(stream):
    while True:
        line = stream.readline()
        if not line:
            break
        print(line.decode('utf-8'), end='')

# Start the process
process = subprocess.Popen(
    ["scripts/app-start.sh"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Start threads to read from stdout and stderr
stdout_thread = threading.Thread(target=stream_reader, args=(process.stdout,))
stderr_thread = threading.Thread(target=stream_reader, args=(process.stderr,))

stdout_thread.start()
stderr_thread.start()

import requests
import time

# URL to ping
url = "http://localhost:8000"

def check_server():
    try:
        response = requests.get(url)
        # Check for a successful response (status codes 200-299)
        print("Could connect to unstructured api server")
        return True
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return False

# Call the function every 100 ms until it succeeds
while not check_server():
    time.sleep(0.1)

def make_request(params: dict):
    url = 'http://localhost:8000/general/v0/general'
    headers = {'accept': 'application/json'}

    print("Handling request for the following params")
    print(params)

    # Extract the file path and remove it from params
    file_path = params.pop('files')

    # Open the file and send the request
    file_content = requests.get(file_path).content


    file_content_type = params.get("content_type") or 'application/octet-stream'
    print("using content type " + file_content_type)
    files = {'files': ('filename', file_content, file_content_type)}
    data = {key: str(value) for key, value in params.items()}

    response = requests.post(url, headers=headers, files=files, data=data)

    return response.json()

def handler(job):
    print("got job")
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    response = make_request(job_input)

    return response

print("start server---->")
runpod.serverless.start({"handler": handler})
