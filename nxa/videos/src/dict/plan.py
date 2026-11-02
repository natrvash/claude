"""Timeline: strike a beat after the AI stops, Ava's line, the ×. Usage: python3 plan.py <id> <ava_seconds>"""
import json, sys, os
D = os.path.dirname(os.path.abspath(__file__)); W = f"{D}/work/{sys.argv[1]}"
tm = json.load(open(f"{W}/timings.json")); ava = float(sys.argv[2])
STRIKE = [tm["end"] + .55, tm["end"] + 1.1]
AVA = [STRIKE[1] + .45, STRIKE[1] + .45 + ava]
plan = {"STRIKE": STRIKE, "AVA": AVA, "TOTAL": round(AVA[1] + 1.3, 3)}
json.dump(plan, open(f"{W}/plan.json", "w")); print(sys.argv[1], plan)
