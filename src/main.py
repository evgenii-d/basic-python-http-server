""" Basic Python HTTP Server """

import os
import logging
import argparse
import itertools
from io import BytesIO
from pathlib import Path
from functools import partial
from socketserver import ThreadingMixIn
from http.server import HTTPServer, SimpleHTTPRequestHandler


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')


class CustomHelpFormatter(argparse.HelpFormatter):
    """ Custom Help Formatter to fix additional spaces that appear if metavar is empty """

    def _format_action_invocation(self, action: argparse.Action) -> str:
        default_format = super()._format_action_invocation(action)
        return default_format.replace(" ,", ",")


class ThreadingBasicServer(ThreadingMixIn, HTTPServer):
    """ Enable threading for HTTP Server """


class BasicHTTPRequestHandler(SimpleHTTPRequestHandler):
    """ Custom Request Handler """

    def __init__(self, *handler_args, **handler_kwargs) -> None:
        self.dir_listing = handler_kwargs.pop('dir_listing', False)
        self.enable_cors = handler_kwargs.pop('enable_cors', False)
        super().__init__(*handler_args, **handler_kwargs)
        self.follow_symlinks = False

    def end_headers(self):
        """ Allow requests from any origin """
        if self.enable_cors:
            self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    # https://en.wikipedia.org/wiki/List_of_Unicode_characters#Control_codes
    _control_char_table = str.maketrans({c: fr'\x{c:02x}' for c in
                                         itertools.chain(range(0x20), range(0x7f, 0xa0))})
    _control_char_table[ord('\\')] = r'\\'

    def log_message(self, *log_args) -> None:
        """ Custom log message formatter """
        message: str = log_args[0] % log_args[1:]
        logging.info("%s - - %s",
                     self.address_string(),
                     message.translate(self._control_char_table))

    def list_directory(self, path: str | os.PathLike[str]) -> BytesIO | None:
        """ Add control over directory listing """
        if not self.dir_listing:
            self.send_error(403, "Directory listing is disabled")
            return None
        return super().list_directory(path)


def basic_http_server(port: int, public_dir: Path, dir_listing: bool, cors: bool) -> None:
    """ Starts a basic HTTP server """
    if not public_dir.exists() or not public_dir.is_dir():
        logging.error("Directory \"%s\" doesn't exist", public_dir)
        return

    logging.info("Initializing Basic HTTP Server")
    try:
        httpd = ThreadingBasicServer(("", port), partial(
            BasicHTTPRequestHandler, directory=public_dir,
            dir_listing=dir_listing, enable_cors=cors))

        logging.info("Available on port %s", port)
        httpd.serve_forever()
    except PermissionError as error:
        logging.error("%s. Port is already in use?", error)


def parse_arguments() -> argparse.Namespace:
    """ Parses command-line arguments """
    parser = argparse.ArgumentParser(
        prog="bphs", description="Basic Python HTTP Server",
        formatter_class=CustomHelpFormatter
    )

    parser.add_argument("-p", "--port",
                        default=8080, type=int,
                        help="port to use [8080]")
    parser.add_argument("-d", "--dir", metavar="PATH",
                        default=Path(os.getcwd()), type=Path,
                        help="directory to serve [current directory]")
    parser.add_argument("-l", "--listing", action="store_true",
                        help="enable directory listing")
    parser.add_argument("--cors", action="store_true",
                        help="enable CORS headers")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    try:
        basic_http_server(args.port, args.dir, args.listing, args.cors)
    except KeyboardInterrupt:
        logging.info("Basic HTTP Server stopped")
