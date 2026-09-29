#!/usr/bin/env python3
import json, sqlite3
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
DB=Path(__file__).resolve().parent.parent/"database"/"PROPAGATION_GIRL_PROJECT_FULL_CONTINUITY_v8.sqlite"
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
class H(BaseHTTPRequestHandler):
    def sendj(self,x,status=200):
        b=json.dumps(x,indent=2).encode()
        self.send_response(status); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        c=conn()
        try:
            if self.path=="/":
                return self.sendj({"version":"8.0","status":"CLOSED_THROUGH_R87_R88_BRANCH_ROADBLOCK","current_qmo":"@qmo/environment_to_bandwidth_generator_map"})
            if self.path=="/qmos":
                return self.sendj([dict(r) for r in c.execute("select * from qmos")])
            if self.path=="/chronology":
                return self.sendj([dict(r) for r in c.execute("select * from chronology")])
            if self.path=="/receipts":
                return self.sendj([dict(r) for r in c.execute("select * from receipts")])
            return self.sendj({"error":"not found"},404)
        finally: c.close()
if __name__=="__main__":
    ThreadingHTTPServer(("127.0.0.1",8808),H).serve_forever()
