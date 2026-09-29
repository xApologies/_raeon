#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_spec import build_render_spec

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("manifold_id")
    ap.add_argument("-o","--output",required=True)
    args=ap.parse_args()
    spec=build_render_spec(args.manifold_id)
    Path(args.output).write_text(json.dumps(spec,indent=2),encoding="utf-8")
    print(args.output)

if __name__=="__main__":
    main()
