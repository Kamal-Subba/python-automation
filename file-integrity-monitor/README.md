# SHA-256 File Hashing Utility

A Python command-line tool that calculates SHA-256 hashes for files and directories.

I built it to get hands-on with file handling, cryptographic hashing, argument parsing, and error handling in Python. It's also the foundation for a file integrity monitor that can catch unexpected or unauthorized changes to files.

## V1 Features

- Hashes individual files
- Recursively hashes files inside directories
- Accepts multiple file and directory paths in one run
- Reads files in binary mode, in chunks, so large files never have to fit in memory
- Handles missing paths and unreadable files without crashing
- Prints each hash next to its file path, in a consistent sorted order

**Current limitation:** V1 calculates hashes but doesn't compare them against previously recorded values yet.

## How It Works

The tool uses only Python's standard library.

| Module | Purpose |
|---|---|
| `hashlib` | Calculates the SHA-256 hashes |
| `argparse` | Handles command-line arguments |
| `pathlib` | Handles file paths and directory traversal |

For each path you give it, the tool:

1. Checks whether the path is a file or a directory
2. Finds every file inside any directories, recursively
3. Opens each file in binary mode
4. Reads it in chunks and feeds each chunk to the SHA-256 hash object
5. Prints the hex digest alongside the file path
6. Reports any file it can't read and moves on to the next one

## Requirements

- Python 3
- Permission to read the files you want to hash

No third-party packages needed.

## Usage

From the project directory:

```bash
cd file-integrity-monitor
```

See the available options:

```bash
python3 fim.py --help
```

Hash a single file:

```bash
python3 fim.py example.txt
```

Hash a directory:

```bash
python3 fim.py /path/to/directory
```

Hash multiple targets at once:

```bash
python3 fim.py example.txt /path/to/directory
```

Each successfully hashed file is printed on its own line:

```
File: example.txt | SHA256: <hash>
```

## Testing

I've manually tested the tool against individual files and directories with multiple files. During development I also checked its output against the Linux `sha256sum` utility, and the digests matched:

```bash
sha256sum example.txt
```

Automated unit tests haven't been written yet. They're part of the V2 plan.

## Security Considerations

A SHA-256 hash is a fixed-length fingerprint of a file's contents. If the contents change, the hash will almost certainly change too, which makes hashing a useful way to spot unexpected modifications.

It has limits, though:

- A hash alone doesn't tell you whether a file is malicious
- V1 doesn't keep a trusted baseline to compare against
- Integrity monitoring only works when you compare against previously recorded hashes
- If the baseline itself is tampered with, future checks can't be trusted
- The tool can only hash files it has permission to read

## V2 Plan

The next phase turns the hashing utility into a working file integrity monitor:

- [ ] Generate and store baseline hashes
- [ ] Compare current hashes against the baseline
- [ ] Detect modified, added, and deleted files
- [ ] Produce structured results
- [ ] Run automatically on a schedule
- [ ] Alert when a change is detected
- [ ] Expand error handling and add automated tests

### Home Lab Integration

Longer term, I want to run this in my home SOC lab to watch sensitive configuration files for unexpected changes and forward integrity events to Wazuh for centralized monitoring.

## What I Learned

- Organizing Python code into functions
- Parsing command-line arguments
- Walking files and directories
- Working with binary files
- Cryptographic hashing
- Handling exceptions
- Checking my program's output against an independent tool

This project will keep growing as I add monitoring, automation, and alerting.
