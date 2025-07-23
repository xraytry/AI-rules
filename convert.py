import json
from pathlib import Path

INPUT_FILE = "sing-box-ai-rules.json"
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

def load_rules():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("route", {}).get("rules", [])

def save(name: str, content: str):
    with open(OUT_DIR / name, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✔️ 已生成 {name}")

def extract_domains(rules):
    domains = set()
    for rule in rules:
        for k in ["domain_keyword", "domain_suffix"]:
            domains.update(rule.get(k, []))
    return sorted(domains)

def convert_to_clash(domains):
    lines = [f"- DOMAIN-KEYWORD,{d},AI" if "." not in d else f"- DOMAIN-SUFFIX,{d},AI" for d in domains]
    return "\n".join(lines)

def convert_to_surge(domains):
    lines = [f"DOMAIN-KEYWORD,{d},AI" if "." not in d else f"DOMAIN-SUFFIX,{d},AI" for d in domains]
    return "\n".join(lines)

def convert_to_loon(domains):
    lines = [f"DOMAIN-KEYWORD,{d},AI" if "." not in d else f"DOMAIN-SUFFIX,{d},AI" for d in domains]
    return "\n".join(lines)

def convert_to_shadowrocket(domains):
    lines = [f"DOMAIN-KEYWORD,{d},AI" if "." not in d else f"DOMAIN-SUFFIX,{d},AI" for d in domains]
    return "\n".join(lines)

def convert_to_singbox(rules):
    return json.dumps({"route": {"rules": rules}}, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    rules = load_rules()
    domains = extract_domains(rules)

    save("singbox.json", convert_to_singbox(rules))
    save("clash.yaml", convert_to_clash(domains))
    save("surge.conf", convert_to_surge(domains))
    save("loon.conf", convert_to_loon(domains))
    save("shadowrocket.conf", convert_to_shadowrocket(domains))
