"""Run CovenantFuse happy path with two non-deployer wallets on StudioNet."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC = "https://studio.genlayer.com/api"
EXPLORER = "https://explorer-studio.genlayer.com"
ROOT = Path(__file__).resolve().parents[1]


def load_wallets():
    path = ROOT.parent / "secrets" / "genlayer-test-wallets.env"
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\"").strip("<>"))


def plain(value):
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)


def signals(info):
    status = str(info.get("status_name") or info.get("statusName") or info.get("status") or "UNKNOWN").upper()
    consensus = str(info.get("result_name") or info.get("consensus_result_name") or info.get("consensus_result") or "UNKNOWN").upper()
    data = info.get("consensus_data") if isinstance(info.get("consensus_data"), dict) else {}
    receipts = data.get("leader_receipt") or data.get("validators") or []
    if isinstance(receipts, dict): receipts = [receipts]
    leader = next((r for r in receipts if isinstance(r, dict) and str(r.get("mode", "")).lower() == "leader"), receipts[0] if receipts else {})
    execution = str(leader.get("execution_result") or info.get("execution_result") or "UNKNOWN").upper()
    result = leader.get("result") if isinstance(leader.get("result"), dict) else {}
    payload = result.get("payload") if isinstance(result.get("payload"), dict) else {}
    readable = payload.get("readable") or result.get("readable")
    return status, consensus, execution, readable


def wait(client, tx):
    for _ in range(200):
        info = plain(client.get_transaction(tx)); status, consensus, execution, returned = signals(info)
        if status == "FINALIZED":
            if consensus not in {"MAJORITY_AGREE", "AGREE", "ACCEPTED"} or execution != "SUCCESS":
                raise AssertionError({"tx": tx, "status": status, "consensus": consensus, "execution": execution})
            return {"hash": tx, "url": f"{EXPLORER}/tx/{tx}", "status": status, "consensus": consensus, "execution": execution, "returned": returned}
        time.sleep(3)
    raise TimeoutError(tx)


def send(client, address, account, method, args):
    tx = str(client.write_contract(address=address, function_name=method, account=account, args=args, value=0))
    print(json.dumps({"submitted": tx, "method": method}), flush=True)
    return wait(client, tx)


def read(client, address, account, method, args):
    return plain(client.read_contract(address=address, function_name=method, args=args, account=account))


def main():
    if len(sys.argv) != 2: raise SystemExit("usage: run_studionet_e2e.py CONTRACT_ADDRESS")
    address = sys.argv[1]; load_wallets()
    wallet_a = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    wallet_b = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    client = create_client(chain=studionet, account=wallet_a, endpoint=RPC)
    cfg = read(client, address, wallet_a, "get_config", [])
    if cfg.get("version") != "COVENANT_FUSE_V2" or cfg.get("deployer_authority") != "NONE": raise AssertionError(cfg)
    action = hashlib.sha256(b"pay rpc invoice 42").hexdigest()
    args = ["TREASURY_WAIT", "Treasury transfers require a seven-day waiting period.", "Emergency RPC invoices may be paid after the same seven-day waiting period.", "RPC infrastructure invoice payments.", action, str(wallet_b.address), 0]
    create_tx = send(client, address, wallet_a, "create_docket", args)
    docket_id = int(str(create_tx["returned"]).strip('"'))
    sealed = read(client, address, wallet_a, "get_docket", [docket_id])
    if sealed["state"] != "SEALED" or sealed["creator"].lower() != str(wallet_a.address).lower(): raise AssertionError(sealed)
    review_tx = send(client, address, wallet_b, "review_docket", [docket_id])
    active = read(client, address, wallet_b, "get_docket", [docket_id])
    if active["state"] != "ACTIVE" or active["reviewer"].lower() != str(wallet_b.address).lower(): raise AssertionError(active)
    consume_tx = send(client, address, wallet_b, "consume_permit", [docket_id, action])
    consumed = read(client, address, wallet_b, "get_docket", [docket_id])
    if consumed["state"] != "CONSUMED": raise AssertionError(consumed)
    evidence = {"network": "studionet", "contract": address, "contract_url": f"{EXPLORER}/address/{address}", "wallet_a_creator": str(wallet_a.address), "wallet_b_reviewer_consumer": str(wallet_b.address), "config": cfg, "create": create_tx, "review": review_tx, "consume": consume_tx, "sealed_readback": sealed, "active_readback": active, "consumed_readback": consumed}
    (ROOT / "docs" / "studionet-e2e.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__": main()
