#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import requests
import json
import base64
import hashlib
import time
import logging
import zlib
from urllib.parse import urlencode
from pathlib import Path

def get_config():
    # Default configuration
    config = {
        "aws_profile": "default",
        "aws_region": "us-east-1",
        "auth0_domain": os.getenv("SMOOTHDEV_AUTH0_DOMAIN", "auth.dev.smoothdev.io"),
        "auth0_client_id": os.getenv("SMOOTHDEV_AUTH0_CLIENT_ID", ""),
        "auth0_audience": os.getenv("SMOOTHDEV_AUTH0_AUDIENCE", "https://auth.dev.smoothdev.io/api"),
        "redirect_uri": os.getenv("SMOOTHDEV_REDIRECT_URI", "http://localhost:3000/api/auth/callback"),
        "smoothdevio_dir": os.path.expanduser("~/.smoothdevio"),
    }

    # Load user config if exists
    user_config_file = Path(config["smoothdevio_dir"]) / "config.json"
    if user_config_file.exists():
        try:
            with open(user_config_file) as f:
                user_config = json.load(f)
                config.update(user_config)
        except Exception as e:
            logger.warning(f"Failed to load user config: {e}")

    # Ensure directory exists
    os.makedirs(config["smoothdevio_dir"], exist_ok=True)

    # Derive paths for JWT files
    config["jwt_file"] = os.path.join(config["smoothdevio_dir"], "auth0_jwt")
    config["jwt_expiry_file"] = os.path.join(config["smoothdevio_dir"], "auth0_jwt_expiry")

    return config

# Configure logger
logger = logging.getLogger("commit_message_generator")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--diff", help="Diff input")
    parser.add_argument("-f", "--file", help="File containing diff input")
    parser.add_argument("-b", "--branch", help="Branch name")
    parser.add_argument("-i", "--issue", help="Issue key")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

def get_diff_input(args):
    if args.diff:
        return args.diff
    elif args.file:
        with open(args.file, 'r') as file:
            return file.read()
    else:
        return subprocess.getoutput("git diff --cached")

def get_branch_name(args):
    return args.branch if args.branch else subprocess.getoutput("git rev-parse --abbrev-ref HEAD")

def get_issue_key(args):
    return f"#{args.issue}" if args.issue else ""

def debug_log(message, debug):
    if debug:
        logger.debug(message)

def validate_diff_input(diff_input):
    if not diff_input:
        logger.error("Error: diff input is required.")
        sys.exit(1)

def generate_code_verifier_and_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def get_device_code():
    device_code_url = f"https://{config['auth0_domain']}/oauth/device/code"
    response = requests.post(device_code_url, json={
        "client_id": config['auth0_client_id'],
        "scope": "openid profile email",
        "audience": config['auth0_audience']
    })
    response.raise_for_status()
    return response.json()

def authenticate_user(device_code_data):
    verification_uri = device_code_data['verification_uri']
    if sys.platform == "win32":
        os.startfile(verification_uri)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", verification_uri])
    else:
        subprocess.Popen(["xdg-open", verification_uri])
    logger.info('1. On your computer or mobile device navigate to: %s', device_code_data['verification_uri_complete'])
    logger.info('2. Enter the following code: %s', device_code_data['user_code'])

def poll_for_token(device_code_data):
    token_url = f"https://{config['auth0_domain']}/oauth/token"
    token_payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code_data['device_code'],
        'client_id': config['auth0_client_id']
    }
    while True:
        response = requests.post(token_url, data=token_payload)
        token_data = response.json()
        if response.status_code == 200:
            return token_data
        elif token_data['error'] not in ('authorization_pending', 'slow_down'):
            raise Exception(token_data['error_description'])
        time.sleep(device_code_data['interval'])

def get_jwt():
    device_code_data = get_device_code()
    authenticate_user(device_code_data)
    token_data = poll_for_token(device_code_data)
    jwt = token_data['access_token']
    jwt_expiry = token_data['expires_in']
    with open(config['jwt_file'], 'w') as file:
        file.write(jwt)
    with open(config['jwt_expiry_file'], 'w') as file:
        file.write(str(int(time.time()) + jwt_expiry))
    return jwt

def is_jwt_valid():
    if os.path.isfile(config['jwt_file']) and os.path.isfile(config['jwt_expiry_file']):
        current_time = int(time.time())
        with open(config['jwt_expiry_file'], 'r') as file:
            jwt_expiry = int(file.read().strip())
        return current_time < jwt_expiry
    return False

def get_stored_jwt():
    with open(config['jwt_file'], 'r') as file:
        return file.read().strip()

def sanitize_payload(payload):
    # Implement sanitization logic here
    # For example, remove any suspicious patterns or content
    sanitized_diff = payload["diff"].replace("169.254.169.254", "[REDACTED]")
    payload["diff"] = sanitized_diff
    return payload

def validate_payload(payload):
    # Implement validation logic here
    # For example, ensure the diff does not contain any URLs or IP addresses
    if "169.254.169.254" in payload["diff"]:
        raise ValueError("Invalid content in diff input")
    return payload

def encode_payload(payload):
    compressed_payload = zlib.compress(json.dumps(payload).encode('utf-8'))
    return base64.b64encode(compressed_payload).decode('utf-8')

def send_api_request(jwt, payload):
    response = requests.post(
        "https://rest.dev.smoothdev.io/commit_message_generator",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}"
        },
        json={"payload": payload}
    )
    return response

def handle_api_response(response):
    if response.status_code != 200:
        error_messages = {
            400: "Bad Request - The server could not understand the request",
            401: "Unauthorized - Authentication is required and has failed",
            403: "Forbidden - You don't have permission to access this resource",
            404: "Not Found - The requested resource could not be found",
            500: "Internal Server Error - Something went wrong on the server",
            502: "Bad Gateway - The server received an invalid response",
            503: "Service Unavailable - The server is temporarily unavailable",
            504: "Gateway Timeout - The server timed out waiting for the request"
        }
        error_msg = error_messages.get(response.status_code, "Unknown error occurred")
        logger.error("Error: HTTP Status %d - %s", response.status_code, error_msg)
        logger.error("Response: %s", response.text)
        sys.exit(1)
    
    # Decode and unzip the response
    encoded_content = response.json().get("commit_message")
    if not encoded_content:
        logger.error("Error: No commit message found in the response")
        sys.exit(1)
    
    decoded_content = base64.b64decode(encoded_content)
    uncompressed_content = zlib.decompress(decoded_content).decode('utf-8')
    
    return uncompressed_content

def split_payload(payload, max_size):
    payload_str = json.dumps(payload)
    payload_bytes = payload_str.encode('utf-8')
    chunks = [payload_bytes[i:i + max_size] for i in range(0, len(payload_bytes), max_size)]
    return [base64.b64encode(chunk).decode('utf-8') for chunk in chunks]

def main():
    args = parse_arguments()
    diff_input = get_diff_input(args)
    validate_diff_input(diff_input)
    branch_name = get_branch_name(args)
    issue_key = get_issue_key(args)
    debug = args.debug

    debug_log(f"Branch Name: {branch_name}", debug)
    debug_log(f"Issue Key: {issue_key}", debug)

    if is_jwt_valid():
        jwt = get_stored_jwt()
        debug_log(f"Using stored JWT: {jwt}", debug)
    else:
        jwt = get_jwt()
        debug_log(f"JWT: {jwt}", debug)

    payload = {
        "diff": diff_input,
        "branch": branch_name,
        "issue": issue_key
    }

    debug_log(f"Payload before sanitization: {json.dumps(payload)}", debug)

    sanitized_payload = sanitize_payload(payload)
    validated_payload = validate_payload(sanitized_payload)

    debug_log(f"Sanitized and Validated Payload: {json.dumps(validated_payload)}", debug)

    encoded_payload = encode_payload(validated_payload)
    payload_size = len(encoded_payload.encode('utf-8'))
    if payload_size > 10 * 1024 * 1024:  # 10MB
        logger.error("Error: Payload size exceeds 10MB limit.")
        sys.exit(1)

    # Split payload into smaller chunks if necessary
    max_chunk_size = 6 * 1024 * 1024  # 6MB
    if payload_size > max_chunk_size:
        payload_chunks = split_payload(validated_payload, max_chunk_size)
        for chunk in payload_chunks:
            response = send_api_request(jwt, chunk)
            debug_log(f"HTTP Status Code: {response.status_code}", debug)
            debug_log(f"Response Body: {response.text}", debug)
            commit_message = handle_api_response(response)
            print(commit_message)
    else:
        response = send_api_request(jwt, encoded_payload)
        debug_log(f"HTTP Status Code: {response.status_code}", debug)
        debug_log(f"Response Body: {response.text}", debug)
        commit_message = handle_api_response(response)
        print(commit_message)

if __name__ == "__main__":
    config = get_config()
    main()