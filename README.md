# SafetyNet JAR extractor
Command line tool to download and extract the latest version of the Google Play Services SafetyNet Jar file.

Rewritten version of anestisb's [snet-extractor](https://github.com/anestisb/snet-extractor) on python.

# How to use
Run
```bash
python extract.py
```
to download and store the JAR file to the current folder as `{date}-{version}.snet.jar`

Run
```bash
python extract.py --save-all path
```
to download and store the JAR file and save all intermediate binaries such as snet.flags binary, snet_flags payload as JSON, and JAR binary.

## Help:
```bash
usage: extract.py [-h] [--output-file OUTPUT_FILE] [--output-dir OUTPUT_DIR] [--save-all SAVE_ALL]

options:
  -h, --help            show this help message and exit
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Path to output JAR file.
  --output-dir OUTPUT_DIR, -d OUTPUT_DIR
                        Path to output JAR directory
  --save-all SAVE_ALL, -v SAVE_ALL
                        Path to directory with intermediate downloaded binaries
```

# Credits
All credits to [snet-extractor](https://github.com/anestisb/snet-extractor).