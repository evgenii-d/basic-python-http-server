# Basic Python HTTP Server (BPHS)

Command-line static HTTP server build upon Python [`HTTPServer`][1] from [standard library][2].

No additional dependencies required.

## Installation

One-file bundled executable can be downloaded from the **Releases** section.

## Usage

```txt
bphs [-h] [-p] [-d] [-l]

-h, --help     show help message and exit
-p, --port     port to use [8080]
-d, --dir      directory to serve [current directory]
-l, --listing  enable directory listing
```

[1]: https://github.com/python/cpython/blob/3.12/Lib/http/server.py
[2]: https://docs.python.org/3/library/http.server.html
