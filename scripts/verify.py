"""End-to-end verification: drives a full workflow run and answers the approval gate.

Usage:  python scripts/verify.py [base_url]
Exits non-zero if any node fails or the run does not complete.
"""

from __future__ import annotations

import asyncio
import json
import sys

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
TIMEOUT = httpx.Timeout(connect=30.0, read=900.0, write=30.0, pool=30.0)


async def answer_gate(client: httpx.AsyncClient, run_id: str, option_id: str) -> None:
    await asyncio.sleep(1.0)
    response = await client.post(
        f"{BASE}/api/runs/{run_id}/decision",
        json={
            "optionId": option_id,
            "approver": "Chief Supply Chain Officer",
            "notes": "Approved via automated end-to-end verification.",
        },
    )
    print(f"    -> decision POST {response.status_code}: {response.text[:200]}")


async def main() -> int:
    states: dict[str, str] = {}
    tokens = 0
    run_id = ""
    summary = None
    gate_task = None

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        health = await client.get(f"{BASE}/api/health")
        print("health:", json.dumps(health.json()))

        async with client.stream("POST", f"{BASE}/api/runs/stream", json={}) as response:
            if response.status_code != 200:
                print(f"FAILED: stream returned {response.status_code}")
                return 1

            buffer = ""
            async for chunk in response.aiter_text():
                buffer += chunk
                while "\n\n" in buffer:
                    raw, buffer = buffer.split("\n\n", 1)
                    raw = raw.strip()
                    if not raw.startswith("data:"):
                        continue
                    try:
                        event = json.loads(raw[5:].strip())
                    except json.JSONDecodeError:
                        continue

                    kind = event.get("type")
                    if kind == "run_started":
                        run_id = event["runId"]
                        print(f"run_started {run_id} incident={event.get('incidentId')}")
                    elif kind == "node_started":
                        print(f"  > {event['nodeId']} ({event.get('hostingMode')}) ...")
                    elif kind == "node_completed":
                        result = event.get("result", {})
                        states[event["nodeId"]] = "completed"
                        tokens += result.get("totalTokens", 0)
                        print(
                            f"    OK {event['nodeId']} "
                            f"{result.get('durationMs')}ms "
                            f"tokens={result.get('totalTokens')} "
                            f"tools={len(result.get('toolCalls', []))}"
                        )
                    elif kind == "node_failed":
                        states[event["nodeId"]] = "failed"
                        print(f"    FAIL {event['nodeId']}: {event.get('error')}")
                    elif kind == "node_skipped":
                        states[event["nodeId"]] = "skipped"
                        print(f"    SKIP {event['nodeId']}: {event.get('reason')}")
                    elif kind == "gate_awaiting":
                        rec = event.get("recommendation", {})
                        option_id = rec.get("optionId", "A")
                        print(f"    GATE awaiting; recommendation={option_id}")
                        gate_task = asyncio.create_task(
                            answer_gate(client, event["runId"], option_id)
                        )
                    elif kind == "run_completed":
                        summary = event.get("summary", {})
                        print("run_completed")
                    elif kind == "run_failed":
                        print(f"run_failed: {event.get('error')}")
                        return 1

    if gate_task:
        await asyncio.gather(gate_task, return_exceptions=True)

    failed = [n for n, s in states.items() if s == "failed"]
    skipped = [n for n, s in states.items() if s == "skipped"]
    completed = [n for n, s in states.items() if s == "completed"]

    print("\n=== SUMMARY ===")
    print(f"completed : {len(completed)}")
    print(f"skipped   : {len(skipped)} {skipped}")
    print(f"failed    : {len(failed)} {failed}")
    print(f"tokens    : {tokens}")
    if summary:
        print(f"durationMs: {summary.get('durationMs')}")
        decision = summary.get("decision") or {}
        print(f"decision  : {decision.get('optionId')} by {decision.get('approver')}")

    if summary is None:
        print("RESULT: FAIL (run did not complete)")
        return 1
    if failed:
        print("RESULT: FAIL (node failures)")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
