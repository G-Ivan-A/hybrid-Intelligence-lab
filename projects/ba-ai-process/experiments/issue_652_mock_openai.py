#!/usr/bin/env python3
"""Scripted OpenAI-compatible streaming server for OpenCode end-to-end experiments.

The script is a JSON list of steps; each step is {"tool": name, "args": {...}} or {"text": "..."}.
The step is chosen by the number of tool results already present in the conversation, so every
request of one session advances the script. Requests without tools (title generation) get a title.
Every request is appended to the log file as one JSON line.
"""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path


def chunk(delta: dict, finish: str | None = None) -> bytes:
    body = {"id": "mock", "object": "chat.completion.chunk", "created": 0, "model": "mock-model",
            "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
    return f"data: {json.dumps(body)}\n\n".encode()


def make_handler(script: list, log: Path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"data": [{"id": "mock-model", "object": "model"}]}).encode())

        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            messages = request.get("messages", [])
            tools = [item.get("function", {}).get("name") for item in request.get("tools", [])]
            done = sum(1 for message in messages if message.get("role") == "tool")
            if not tools:
                step = {"text": "BCREQ mock session"}
            else:
                step = script[done] if done < len(script) else {"text": "done"}
            with log.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"tools": tools, "messages": messages, "step": step}, ensure_ascii=False) + "\n")
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(chunk({"role": "assistant", "content": ""}))
            if "tool" in step:
                call = {"index": 0, "id": f"call_{done}", "type": "function",
                        "function": {"name": step["tool"], "arguments": json.dumps(step["args"], ensure_ascii=False)}}
                self.wfile.write(chunk({"tool_calls": [call]}))
                self.wfile.write(chunk({}, "tool_calls"))
            else:
                self.wfile.write(chunk({"content": step["text"]}))
                self.wfile.write(chunk({}, "stop"))
            usage = {"id": "mock", "object": "chat.completion.chunk", "created": 0, "model": "mock-model",
                     "choices": [], "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}
            self.wfile.write(f"data: {json.dumps(usage)}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("log", type=Path)
    parser.add_argument("--port-file", type=Path, required=True)
    args = parser.parse_args()
    script = json.loads(args.script.read_text(encoding="utf-8"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(script, args.log))
    args.port_file.write_text(str(server.server_address[1]), encoding="utf-8")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
