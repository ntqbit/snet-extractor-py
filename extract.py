import argparse
import requests
import parser
import os
import json
from urllib.parse import urlparse


SNET_FLAGS_URL = 'https://www.gstatic.com/android/snet/snet.flags'


def download_file(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ExtractorException(
            f'Server returned {response.status_code} code. URL: {url}')

    return response.content


def get_snet_flags():
    return download_file(SNET_FLAGS_URL)


def download_jar(url):
    return download_file(url)


def extract_jar_filename_from_url(url):
    return urlparse(jar_url).path.split('/')[-1]


# Parse command line arguments
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument(
    '--output-file', '-o', type=str, help='Path to output JAR file.')
argument_parser.add_argument(
    '--output-dir', '-d', type=str, help='Path to output JAR directory')
argument_parser.add_argument(
    '--save-all', '-v', type=str, help='Path to directory with intermediate downloaded binaries')
args = argument_parser.parse_args()

if args.output_file and args.output_dir:
    parser.error('Either JAR file or directory should be specified, not both.')

# Download SNET flags
snet_flags_binary = get_snet_flags()
snet_flags = parser.parse_snet_flags(snet_flags_binary)
print('[+] SafetyNet version: ' + snet_flags['version'])

# Download JAR
jar_url = snet_flags['payload']['url']
print('[+] JAR url: ' + jar_url)
jar_snet = download_jar(jar_url)
jar = parser.parse_jar_binary(jar_snet)
jar_url_filename = extract_jar_filename_from_url(jar_url)

# Get JAR path
if args.output_file:
    jar_path = args.output_file
else:
    jar_filename = jar_url_filename + '.jar'
    if args.output_dir:
        jar_path = os.path.join(args.output_dir, jar_filename)
    else:
        jar_path = jar_filename

# Save JAR
with open(jar_path, 'wb') as f:
    f.write(jar)

print('[+] JAR saved to ' + jar_path)

# Save intermediate binaries
if args.save_all:
    # Create directory if not exists
    if not os.path.isdir(args.save_all):
        os.mkdir(args.save_all)

    def save_file(name, data):
        with open(os.path.join(args.save_all, name), 'wb') as f:
            f.write(data)

    save_file('snet.flags', snet_flags_binary)
    save_file('snet_flags.json', json.dumps(snet_flags['payload'], indent=4).encode())
    save_file(jar_url_filename, jar_snet)
    print(f'[+] Intermediate binaries stored to {args.save_all}')

print('[+] Done.')
