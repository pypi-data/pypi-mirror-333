import argparse
import base64
import json
import os
import subprocess
import uuid

def main():
    new_uuid = uuid.uuid4()

    parser = argparse.ArgumentParser()
    parser.add_argument('prompt', type=str, help='Prompt describing the plot to generate.')
    parser.add_argument('--output', type=str, default=f'maxplotlib_output_{new_uuid}', help='Output directory to save the image.')
    parser.add_argument('--server', type=str, help='Server IP address for the maxplotlib server. Overrides MAXPLOTLIB_SERVER_IP environment variable.', default='localhost')
    args = parser.parse_args()

    # Get server IP from command line argument or environment variable
    server_ip = args.server or os.getenv('MAXPLOTLIB_SERVER_IP')
    if not server_ip:
        raise ValueError("Server IP must be provided either via --server argument or MAXPLOTLIB_SERVER_IP environment variable")

    os.makedirs(args.output, exist_ok=True)
    os.makedirs(f'{args.output}', exist_ok=True)

    curl_command = [
        'curl', '-s', '-X', 'POST',
        f'http://{server_ip}:8000/plot/', '-F',
        f'prompt={args.prompt}', '-o', f'{args.output}/response.json'
    ]
    subprocess.run(curl_command, check=True)

    with open(f'{args.output}/response.json', 'r') as file:
        data = json.load(file)
        image_data = data['images']
        image_bytes = [base64.b64decode(d) for d in image_data]
        for i, im in enumerate(image_bytes):
            with open(f'{args.output}/option{i}.png', 'wb') as img_file:
                img_file.write(im)
    print(f"Image saved in '{args.output}/'")

if __name__ == '__main__':
    main()
