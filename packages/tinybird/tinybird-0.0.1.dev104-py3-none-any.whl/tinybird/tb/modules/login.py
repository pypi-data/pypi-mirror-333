import http.server
import os
import socketserver
import threading
import time
import urllib.parse
import webbrowser
from urllib.parse import urlencode

import click
import requests

from tinybird.tb.modules.cli import CLIConfig, cli
from tinybird.tb.modules.common import coro
from tinybird.tb.modules.feedback_manager import FeedbackManager


class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # The access_token is in the URL fragment, which is not sent to the server
        # We'll send a small HTML page that extracts the token and sends it back to the server
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            """
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background: #f5f5f5;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <script>
                const searchParams = new URLSearchParams(window.location.search);
                const code = searchParams.get('code');
                const workspace = searchParams.get('workspace');
                const region = searchParams.get('region');
                const provider = searchParams.get('provider');
                const host = "{auth_host}";
                fetch('/?code=' + code, {{method: 'POST'}})
                    .then(() => {{
                        window.location.href = host + "/" + provider + "/" + region + "/cli-login?workspace=" + workspace;
                    }});
            </script>
        </body>
        </html>
        """.format(auth_host=self.server.auth_host).encode()  # type: ignore
        )

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if "code" in query_params:
            code = query_params["code"][0]
            self.server.auth_callback(code)  # type: ignore
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(400, "Missing 'code' parameter")

        self.server.shutdown()

    def log_message(self, format, *args):
        # Suppress log messages
        return


AUTH_SERVER_PORT = 49160


class AuthServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, auth_callback, auth_host):
        self.auth_callback = auth_callback
        self.auth_host = auth_host
        super().__init__(server_address, RequestHandlerClass)


def start_server(auth_callback, auth_host):
    with AuthServer(("", AUTH_SERVER_PORT), AuthHandler, auth_callback, auth_host) as httpd:
        httpd.timeout = 30
        start_time = time.time()
        while time.time() - start_time < 60:  # Run for a maximum of 60 seconds
            httpd.handle_request()


@cli.command()
@click.option(
    "--host",
    default="https://api.europe-west2.gcp.tinybird.co",
    help="Set custom host if it's different than https://api.tinybird.co. See https://www.tinybird.co/docs/api-reference/overview#regions-and-endpoints for the available list of regions.",
)
@click.option(
    "--auth-host",
    default="https://cloud.tinybird.co",
    help="Set the host to authenticate to. If unset, the default host will be used.",
)
@click.option(
    "--workspace",
    help="Set the workspace to authenticate to. If unset, the default workspace will be used.",
)
@coro
async def login(host: str, auth_host: str, workspace: str):
    """Authenticate using the browser."""
    auth_event = threading.Event()
    auth_code: list[str] = []  # Using a list to store the code, as it's mutable

    def auth_callback(code):
        auth_code.append(code)
        auth_event.set()

    click.echo(FeedbackManager.highlight(message="» Opening browser for authentication..."))

    # Start the local server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(auth_callback, auth_host))
    server_thread.daemon = True
    server_thread.start()

    # Open the browser to the auth page
    callback_url = f"http://localhost:{AUTH_SERVER_PORT}"
    params = {
        "redirect_uri": callback_url,
        "apiHost": host,
    }

    if workspace:
        params["workspace"] = workspace

    auth_url = f"{auth_host}/api/cli-login?{urlencode(params)}"
    webbrowser.open(auth_url)

    # Wait for the authentication to complete or timeout
    if auth_event.wait(timeout=60):  # Wait for up to 60 seconds
        params = {}
        params["code"] = auth_code[0]
        response = requests.get(  # noqa: ASYNC210
            f"{auth_host}/api/cli-login?{urlencode(params)}",
        )

        data = response.json()
        cli_config = CLIConfig.get_project_config()
        cli_config.set_token(data.get("workspace_token", ""))
        cli_config.set_token_for_host(data.get("workspace_token", ""), host)
        cli_config.set_user_token(data.get("user_token", ""))
        cli_config.set_host(host or data.get("api_host", ""))

        ws = await cli_config.get_client(token=data.get("workspace_token", ""), host=host).workspace_info(version="v1")
        for k in ("id", "name", "user_email", "user_id", "scope"):
            if k in ws:
                cli_config[k] = ws[k]

        path = os.path.join(os.getcwd(), ".tinyb")
        cli_config.persist_to_file(override_with_path=path)
        click.echo(FeedbackManager.gray(message="\nWorkspace: ") + FeedbackManager.info(message=ws["name"]))
        click.echo(FeedbackManager.gray(message="User: ") + FeedbackManager.info(message=ws["user_email"]))
        click.echo(FeedbackManager.gray(message="Host: ") + FeedbackManager.info(message=host))
        click.echo(FeedbackManager.success(message="\n✓ Authentication successful!"))
    else:
        click.echo(FeedbackManager.error(message="Authentication failed or timed out."))
