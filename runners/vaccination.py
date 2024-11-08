import asyncio
import json
import logging
import os
import sys
import datetime
from aiohttp import ClientError
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa

from agent_container import (  # noqa:E402
    arg_parser,
    create_agent_with_args,
    AriesAgent,
)
from support.utils import (  # noqa:E402
    check_requires,
    log_msg,
    log_status,
    log_timer,
    prompt,
    prompt_loop,
)


import random

TAILS_FILE_COUNT = int(os.getenv("TAILS_FILE_COUNT", 100))
CRED_PREVIEW_TYPE = "https://didcomm.org/issue-credential/2.0/credential-preview"
SELF_ATTESTED = os.getenv("SELF_ATTESTED")
TAILS_FILE_COUNT = int(os.getenv("TAILS_FILE_COUNT", 100))

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)


class VaccinationAgent(AriesAgent):
    def __init__(
        self,
        ident: str,
        http_port: int,
        admin_port: int,
        no_auto: bool = False,
        **kwargs,
    ):
        super().__init__(
            ident,
            http_port,
            admin_port,
            prefix="Vaccination",
            no_auto=no_auto,
            **kwargs,
        )
        self.connection_id = None
        self._connection_ready = None
        self.cred_state = {}
        self.cred_attrs = {}

    async def detect_connection(self):
        await self._connection_ready
        self._connection_ready = None

    @property
    def connection_ready(self):
        return self._connection_ready.done() and self._connection_ready.result()

    async def handle_oob_invitation(self, message):
        pass

    async def handle_connections(self, message):
        print(
            self.ident, "handle_connections", message["state"], message["rfc23_state"]
        )
        conn_id = message["connection_id"]
        if (not self.connection_id) and message["rfc23_state"] == "invitation-sent":
            print(self.ident, "set connection id", conn_id)
            self.connection_id = conn_id
        if (
            message["connection_id"] == self.connection_id
            and message["rfc23_state"] == "completed"
            and (self._connection_ready and not self._connection_ready.done())
        ):
            self.log("Connected")
            self._connection_ready.set_result(True)

    async def handle_issue_credential_v2_0(self, message):
        state = message["state"]
        cred_ex_id = message["cred_ex_id"]
        prev_state = self.cred_state.get(cred_ex_id)
        if prev_state == state:
            return  # ignore
        self.cred_state[cred_ex_id] = state

        self.log(f"Credential: state = {state}, cred_ex_id = {cred_ex_id}")

        if state == "request-received":
            # issue credentials based on offer preview in cred ex record
            if not message.get("auto_issue"):
                await self.admin_POST(
                    f"/issue-credential-2.0/records/{cred_ex_id}/issue",
                    {"comment": f"Issuing credential, exchange {cred_ex_id}"},
                )

    async def handle_issue_credential_v2_0_indy(self, message):
        pass  # vaccination id schema does not support revocation

    async def handle_present_proof_v2_0(self, message):
        state = message["state"]
        pres_ex_id = message["pres_ex_id"]
        self.log(f"Presentation: state = {state}, pres_ex_id = {pres_ex_id}")

        if state == "presentation-received":
            log_status("#27 Process the proof provided by X")
            log_status("#28 Check if proof is valid")
            proof = await self.admin_POST(
                f"/present-proof-2.0/records/{pres_ex_id}/verify-presentation"
            )
            self.log("Proof = ", proof["verified"])

            # if presentation is a health schema (proof of health),
            # check values received
            pres_req = message["by_format"]["pres_request"]["indy"]
            pres = message["by_format"]["pres"]["indy"]
            is_proof_of_health = (
                pres_req["name"] == "Proof of Health"
            )
            if is_proof_of_health:
                log_status("#28.1 Received proof of health, check claims")
                for (referent, attr_spec) in pres_req["requested_attributes"].items():
                    if referent in pres['requested_proof']['revealed_attrs']:
                        self.log(
                            f"{attr_spec['name']}: "
                            f"{pres['requested_proof']['revealed_attrs'][referent]['raw']}"
                        )
                    else:
                        self.log(
                            f"{attr_spec['name']}: "
                            "(attribute not revealed)"
                        )
                for id_spec in pres["identifiers"]:
                    # just print out the schema/cred def id's of presented claims
                    self.log(f"schema_id: {id_spec['schema_id']}")
                    self.log(f"cred_def_id {id_spec['cred_def_id']}")
                # TODO placeholder for the next step
            else:
                # in case there are any other kinds of proofs received
                self.log("#28.1 Received ", pres_req["name"])

    async def handle_basicmessages(self, message):
        self.log("Received message:", message["content"])


async def main(args):
    vaccination_agent = await create_agent_with_args(args, ident="vaccination")
    # ADDED
    age = 18
    d = datetime.date.today()
    birth_date = datetime.date(d.year - age, d.month, d.day)
    birth_date_format = "%Y%m%d"


    try:
        log_status(
            "#1 Provision an agent and wallet, get back configuration details"
            + (
                f" (Wallet type: {vaccination_agent.wallet_type})"
                if vaccination_agent.wallet_type
                else ""
            )
        )
        agent = VaccinationAgent(
            "vaccination.agent",
            vaccination_agent.start_port,
            vaccination_agent.start_port + 1,
            genesis_data=vaccination_agent.genesis_txns,
            genesis_txn_list=vaccination_agent.genesis_txn_list,
            no_auto=vaccination_agent.no_auto,
            tails_server_base_url=vaccination_agent.tails_server_base_url,
            timing=vaccination_agent.show_timing,
            multitenant=vaccination_agent.multitenant,
            mediation=vaccination_agent.mediation,
            wallet_type=vaccination_agent.wallet_type,
            seed=vaccination_agent.seed,
        )

        vaccination_agent.public_did = True
        vaccination_schema_name = "vaccination id schema"
        vaccination_schema_attrs = ["patient_id", "name", "date", "position"]
        await vaccination_agent.initialize(
            the_agent=agent,
            schema_name=vaccination_schema_name,
            schema_attrs=vaccination_schema_attrs,
        )

        with log_timer("Publish schema and cred def duration:"):
            # define schema
            version = format(
                "%d.%d.%d"
                % (
                    random.randint(1, 101),
                    random.randint(1, 101),
                    random.randint(1, 101),
                )
            )
            # register schema and cred def
            (schema_id, cred_def_id) = await agent.register_schema_and_creddef(
                "vaccination id schema",
                version,
                ["patient_id", "name", "date", "position"],
                support_revocation=False,
                revocation_registry_size=TAILS_FILE_COUNT,
            )

        # generate an invitation for Alice
        await vaccination_agent.generate_invitation(display_qr=True, wait=True)

        options = (
            "    (1) Issue Credential\n"
            "    (2) Send Proof Request\n"
            "    (3) Send Message\n"
            "    (4) Create New Invitation\n"
            "    (X) Exit?\n"
            "[1/2/3/X]"
        )
        async for option in prompt_loop(options):
            if option is not None:
                option = option.strip()

            if option is None or option in "xX":
                break

            elif option == "1":
                log_status("#13 Issue credential offer to X")
                agent.cred_attrs[cred_def_id] = {
                    "patient_id": "ACME0009",
                    "name": "Alice Smith",
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    "position": "APPROVED"
                }
                cred_preview = {
                    "@type": CRED_PREVIEW_TYPE,
                    "attributes": [
                        {"name": n, "value": v}
                        for (n, v) in agent.cred_attrs[cred_def_id].items()
                    ],
                }
                offer_request = {
                    "connection_id": agent.connection_id,
                    "comment": f"Offer on cred def id {cred_def_id}",
                    "credential_preview": cred_preview,
                    "filter": {"indy": {"cred_def_id": cred_def_id}},
                }
                await agent.admin_POST(
                    "/issue-credential-2.0/send-offer", offer_request
                )

            elif option == "2":
                log_status("#20 Request proof of health from alice")
                req_attrs = [
                    {
                        "name": "name",
                        "restrictions": [{"schema_name": "health schema"}]
                    },
                    {
                        "name": "date",
                        "restrictions": [{"schema_name": "health schema"}]
                    },
                    {
                        "name": "condition",
                        "restrictions": [{"schema_name": "health schema"}]
                    }
                ]
                req_preds = [
                    # ADDED
                    # test zero-knowledge proofs
                    {
                        "name": "birthdate_dateint",
                        "p_type": "<=",
                        "p_value": int(birth_date.strftime(birth_date_format)),
                        "restrictions": [{"schema_name": "health schema"}],
                    },
                    {
                        "name": "condition",
                        "p_type": ">=",
                        "p_value": 1,
                        "restrictions": [{"schema_name": "health schema"}],
                    }]
                indy_proof_request = {
                    "name": "Proof of Health",
                    "version": "1.0",
                    "nonce": str(uuid4().int),
                    "requested_attributes": {
                        f"0_{req_attr['name']}_uuid": req_attr
                        for req_attr in req_attrs
                    },
                    "requested_predicates": {
                        f"0_{req_pred['name']}_GE_uuid": req_pred
                        for req_pred in req_preds}
                }
                proof_request_web_request = {
                    "connection_id": agent.connection_id,
                    "presentation_request": {"indy": indy_proof_request},
                }
                # this sends the request to our agent, which forwards it to Alice
                # (based on the connection_id)
                log_msg(f"Proof request sent: {json.dumps(proof_request_web_request, indent=4)}")
                await agent.admin_POST(
                    "/present-proof-2.0/send-request",
                    proof_request_web_request
                )

            elif option == "3":
                msg = await prompt("Enter message: ")
                await agent.admin_POST(
                    f"/connections/{agent.connection_id}/send-message", {"content": msg}
                )
            elif option == "4":
                log_msg(
                    "Creating a new invitation, please receive "
                    "and accept this invitation using Alice agent"
                )
                await vaccination_agent.generate_invitation(
                    display_qr=True,
                    reuse_connections=vaccination_agent.reuse_connections,
                    multi_use_invitations=vaccination_agent.multi_use_invitations,
                    public_did_connections=vaccination_agent.public_did_connections,
                    wait=True,
                )

        if vaccination_agent.show_timing:
            timing = await vaccination_agent.agent.fetch_timing()
            if timing:
                for line in vaccination_agent.agent.format_timing(timing):
                    log_msg(line)

    finally:
        terminated = await vaccination_agent.terminate()

    await asyncio.sleep(0.1)

    if not terminated:
        os._exit(1)


if __name__ == "__main__":
    parser = arg_parser(ident="vaccination", port=8040)
    args = parser.parse_args()

    ENABLE_PYDEVD_PYCHARM = os.getenv("ENABLE_PYDEVD_PYCHARM", "").lower()
    ENABLE_PYDEVD_PYCHARM = ENABLE_PYDEVD_PYCHARM and ENABLE_PYDEVD_PYCHARM not in (
        "false",
        "0",
    )
    PYDEVD_PYCHARM_HOST = os.getenv("PYDEVD_PYCHARM_HOST", "localhost")
    PYDEVD_PYCHARM_CONTROLLER_PORT = int(
        os.getenv("PYDEVD_PYCHARM_CONTROLLER_PORT", 5001)
    )

    if ENABLE_PYDEVD_PYCHARM:
        try:
            import pydevd_pycharm

            print(
                "Acme remote debugging to "
                f"{PYDEVD_PYCHARM_HOST}:{PYDEVD_PYCHARM_CONTROLLER_PORT}"
            )
            pydevd_pycharm.settrace(
                host=PYDEVD_PYCHARM_HOST,
                port=PYDEVD_PYCHARM_CONTROLLER_PORT,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False,
            )
        except ImportError:
            print("pydevd_pycharm library was not found")

    check_requires(args)

    try:
        asyncio.get_event_loop().run_until_complete(main(args))
    except KeyboardInterrupt:
        os._exit(1)