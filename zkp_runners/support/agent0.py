import os
import sys
import logging
from aiohttp import ClientSession

AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT")

DEFAULT_POSTGRES = bool(os.getenv("POSTGRES"))
DEFAULT_INTERNAL_HOST = "127.0.0.1"
DEFAULT_EXTERNAL_HOST = "localhost"
DEFAULT_PYTHON_PATH = ".."
PYTHON = os.getenv("PYTHON", sys.executable)

START_TIMEOUT = float(os.getenv("START_TIMEOUT", 30.0))

RUN_MODE = os.getenv("RUNMODE")

# Prompt the user for the genesis file URL
GENESIS_URL = input("Please enter the full URL path to the genesis file: ")
LEDGER_URL = os.getenv("LEDGER_URL", "192.168.178.133:9000")
GENESIS_FILE = os.getenv("GENESIS_FILE")

if RUN_MODE == "docker":
    DEFAULT_INTERNAL_HOST = os.getenv("DOCKERHOST") or "host.docker.internal"
    DEFAULT_EXTERNAL_HOST = DEFAULT_INTERNAL_HOST
    DEFAULT_PYTHON_PATH = "."
elif RUN_MODE == "pwd":
    # DEFAULT_INTERNAL_HOST =
    DEFAULT_EXTERNAL_HOST = os.getenv("DOCKERHOST") or "host.docker.internal"
    DEFAULT_PYTHON_PATH = "."

WALLET_TYPE_INDY = "indy"
WALLET_TYPE_ASKAR = "askar"
WALLET_TYPE_ANONCREDS = "askar-anoncreds"

CRED_FORMAT_INDY = "indy"

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)

# Functions from agent.py
async def default_genesis_txns():
    genesis = None
    try:
        if GENESIS_URL:
            async with ClientSession() as session:
                async with session.get(GENESIS_URL) as resp:
                    genesis = await resp.text()
        elif RUN_MODE == "docker":
            async with ClientSession() as session:
                async with session.get(
                    f"http://{DEFAULT_EXTERNAL_HOST}:9000/genesis"
                ) as resp:
                    genesis = await resp.text()
        elif GENESIS_FILE:
            with open(GENESIS_FILE, "r") as genesis_file:
                genesis = genesis_file.read()
        elif LEDGER_URL:
            async with ClientSession() as session:
                async with session.get(LEDGER_URL.rstrip("/") + "/genesis") as resp:
                    genesis = await resp.text()
        else:
            with open("local-genesis.txt", "r") as genesis_file:
                genesis = genesis_file.read()
    except Exception:
        LOGGER.exception("Error loading genesis transactions:")
    return genesis

class FaberAgent(AriesAgent):
    def __init__(
        self,
        ident: str,
        http_port: int,
        admin_port: int,
    ):
        super().__init__(ident, http_port, admin_port)
        # Additional initialization code here

    async def generate_invitation(self):
        # Example method to generate an invitation
        pass

    async def handle_connections(self):
        # Example method to handle connections
        pass

    async def issue_credential(self):
        # Example method to issue a credential
        pass

    async def verify_proof(self):
        # Example method to verify a proof
        pass

async def main(args):
    agent = FaberAgent(
        ident="Faber.Agent",
        http_port=args.http_port,
        admin_port=args.admin_port,
    )
    await agent.listen_webhooks()
    await agent.register_did()
    await agent.start_process()

    try:
        while True:
            await agent.handle_connections()
            await agent.issue_credential()
            await agent.verify_proof()
            time.sleep(1)
    except KeyboardInterrupt:
        await agent.terminate()

if __name__ == "__main__":
    args = arg_parser.parse_args()
    try:
        asyncio.run(main(args))
    except Exception as e:
        LOGGER.exception("Error running Faber agent: %s", str(e))