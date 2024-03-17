# Basic Python HTTP Server (BPHS)

Command-line static HTTP server build upon Python [`HTTPServer`][1] from [standard library][2].

No additional dependencies required.

## Installation

One-file bundled executable can be downloaded from the **Releases** section.

Tested on Windows 10/11, Ubuntu 22.04.

## Usage

```txt
bphs [-h] [-p PORT] [-d PATH] [-l] [--cors]

-h, --help            show help message and exit
-p PORT, --port PORT  port to use [8080]
-d PATH, --dir PATH   directory to serve [current directory]
-l, --listing         enable directory listing
--cors                enable CORS headers
```

[1]: https://github.com/python/cpython/blob/3.12/Lib/http/server.py
[2]: https://docs.python.org/3/library/http.server.html
