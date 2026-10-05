"""Run CovenantFuse adversarial paths with complete pre/post readback."""
from __future__ import annotations
import hashlib, json, os, sys, time
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC="https://studio.genlayer.com/api"; EX="https://explorer-studio.genlayer.com"; ROOT=Path(__file__).resolve().parents[1]

def load_wallets():
    for raw in (ROOT.parent/"secrets"/"genlayer-test-wallets.env").read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            k,v=raw.split("=",1);os.environ.setdefault(k.strip(),v.strip().strip("'\"").strip("<>"))

def plain(v):
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [plain(x) for x in v]
    return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)

def signals(x):
    status=str(x.get("status_name") or x.get("statusName") or x.get("status") or "UNKNOWN").upper()
    consensus=str(x.get("result_name") or x.get("consensus_result_name") or x.get("consensus_result") or "UNKNOWN").upper()
    data=x.get("consensus_data") if isinstance(x.get("consensus_data"),dict) else {};rows=data.get("leader_receipt") or data.get("validators") or []
    if isinstance(rows,dict):rows=[rows]
    leader=next((r for r in rows if isinstance(r,dict) and str(r.get("mode","")).lower()=="leader"),rows[0] if rows else {})
    execution=str(leader.get("execution_result") or x.get("execution_result") or "UNKNOWN").upper();result=leader.get("result") if isinstance(leader.get("result"),dict) else {}
    payload=result.get("payload");readable=payload.get("readable") if isinstance(payload,dict) else payload
    return status,consensus,execution,readable

def wait(client,tx,success):
    for _ in range(200):
        status,consensus,execution,returned=signals(plain(client.get_transaction(tx)))
        if status=="FINALIZED":
            ok=consensus in {"MAJORITY_AGREE","AGREE","ACCEPTED"} and execution=="SUCCESS"
            if ok!=success:raise AssertionError({"tx":tx,"status":status,"consensus":consensus,"execution":execution,"expected_success":success})
            return {"hash":tx,"url":f"{EX}/tx/{tx}","status":status,"consensus":consensus,"execution":execution,"returned":returned}
        time.sleep(3)
    raise TimeoutError(tx)

def send(client,address,account,method,args,success=True):
    tx=str(client.write_contract(address=address,function_name=method,account=account,args=args,value=0));print(json.dumps({"submitted":tx,"method":method}),flush=True);return wait(client,tx,success)

def read(client,address,account,method,args):return plain(client.read_contract(address=address,function_name=method,args=args,account=account))

def snapshot(client,address,account,ids):return {"config":read(client,address,account,"get_config",[]),"dockets":[read(client,address,account,"get_docket",[i]) for i in ids]}

def main():
    if len(sys.argv)!=2:raise SystemExit("usage: run_studionet_adversarial.py CONTRACT_ADDRESS")
    address=sys.argv[1];load_wallets();a=create_account(os.environ["SERVICE_LEDGER_KEY_A"]);b=create_account(os.environ["SERVICE_LEDGER_KEY_B"]);client=create_client(chain=studionet,account=a,endpoint=RPC)
    if read(client,address,a,"get_config",[]).get("version")!="COVENANT_FUSE_V2":raise AssertionError("wrong version")
    action=hashlib.sha256(b"pay rpc invoice 42").hexdigest();happy_args=["TREASURY_WAIT","Treasury transfers require a seven-day waiting period.","Emergency RPC invoices may be paid after the same seven-day waiting period.","RPC infrastructure invoice payments.",action,str(b.address),0]
    cases=[]
    for name,account,method,args in [("REPLAY_CONSUME",b,"consume_permit",[1,action]),("DUPLICATE_BUNDLE",a,"create_docket",happy_args)]:
        before=snapshot(client,address,account,[1]);tx=send(client,address,account,method,args,False);after=snapshot(client,address,account,[1]);
        if before!=after:raise AssertionError({"name":name,"before":before,"after":after})
        cases.append({"name":name,"transaction":tx,"pre_post_equal":True})
    conflict_action=hashlib.sha256(b"bypass rpc waiting period").hexdigest();conflict_args=["TREASURY_WAIT","Treasury transfers require a seven-day waiting period.","Emergency RPC invoices may bypass the waiting period and execute immediately.","RPC infrastructure invoice payments.",conflict_action,str(b.address),0]
    created=send(client,address,a,"create_docket",conflict_args,True);docket_id=int(str(created["returned"]).strip('"'));sealed=read(client,address,a,"get_docket",[docket_id])
    before=snapshot(client,address,a,[1,docket_id]);self_tx=send(client,address,a,"review_docket",[docket_id],False);after=snapshot(client,address,a,[1,docket_id])
    if before!=after:raise AssertionError("self review mutated state")
    reviewed=send(client,address,b,"review_docket",[docket_id],True);blocked=read(client,address,b,"get_docket",[docket_id])
    if blocked["state"]!="BLOCKED":raise AssertionError(blocked)
    before=snapshot(client,address,b,[1,docket_id]);consume_tx=send(client,address,b,"consume_permit",[docket_id,conflict_action],False);after=snapshot(client,address,b,[1,docket_id])
    if before!=after:raise AssertionError("blocked consume mutated state")
    cases += [{"name":"CREATOR_SELF_REVIEW","transaction":self_tx,"pre_post_equal":True},{"name":"CONFLICT_REVIEW","create":created,"review":reviewed,"docket":blocked},{"name":"CONSUME_BLOCKED_DOCKET","transaction":consume_tx,"pre_post_equal":True}]
    evidence={"network":"studionet","contract":address,"contract_url":f"{EX}/address/{address}","wallet_a":str(a.address),"wallet_b":str(b.address),"cases":cases,"final":snapshot(client,address,b,[1,docket_id])}
    (ROOT/"docs"/"studionet-adversarial.json").write_text(json.dumps(evidence,indent=2)+"\n",encoding="utf-8");print(json.dumps(evidence,indent=2))

if __name__=="__main__":main()
