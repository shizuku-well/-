#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
马良 AI (mlai.online) 纯协议注册机
流程：注册账号(不验证邮箱) -> 登录态直接创建 API Key（默认选 Grok 分组 id=5）
Key 自动保存到文件（一行一个，纯 key）

用法：
  python3 register_bot.py                     # 注册 1 个，随机邮箱，Grok 分组
  python3 register_bot.py -n 60               # 批量注册 60 个
  python3 register_bot.py -d 10               # 间隔 10 秒一个（防限流）
  python3 register_bot.py -r 3                # 撞限流(429)自动等 30s 重试，最多 3 次
  python3 register_bot.py -e my@mail.com -p MyPass123 -c 邀请码
  python3 register_bot.py -g 79               # 指定其它分组 id（如 79=Claude反重力）
  python3 register_bot.py --proxy "http://1.2.3.4:8080"          # 走单个代理
  python3 register_bot.py --proxy-file proxylist.txt             # 代理列表轮换（一行一个）
"""
import argparse
import json
import os
import random
import string
import sys
import time
import urllib.request
import urllib.error

BASE = "https://www.mlai.online/api/v1"
UA = "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
GROK_GROUP_ID = 5   # 🛡️ Grok 稳定渠道 · 中国最低价

# 保存文件：Android 上写 /storage/emulated/0/，PC 上写脚本当前目录
DEFAULT_OUT = "/storage/emulated/0/mlai_keys.txt" if os.path.exists("/storage/emulated/0/") else os.path.join(os.path.dirname(os.path.abspath(__file__)), "mlai_keys.txt")


class ProxyPool:
    """代理池：轮换取代理，None 表示直连"""
    def __init__(self, proxies=None):
        self.proxies = [p for p in (proxies or []) if p]
        self.idx = 0

    def next(self):
        if not self.proxies:
            return None
        p = self.proxies[self.idx % len(self.proxies)]
        self.idx += 1
        return p


def load_proxies(proxy, proxy_file):
    """返回代理列表；proxy 优先，其次读文件（一行一个，忽略 # 注释和空行）"""
    if proxy:
        return [proxy]
    if proxy_file:
        out = []
        with open(proxy_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "://" not in line:
                        line = "http://" + line
                    out.append(line)
        return out
    return []


def http(method, path, body=None, token=None, timeout=30, proxy=None):
    url = BASE + path
    headers = {
        "User-Agent": UA,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.mlai.online",
        "Referer": "https://www.mlai.online/",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = None
    if proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    try:
        if opener:
            with opener.open(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode())
        else:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="ignore")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw[:300]}


def rand_email():
    s = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domains = ["example.com", "mail.com", "test.com", "proton.me"]
    return f"{s}@{random.choice(domains)}"


def register(email, password, invite_code=None, proxy=None):
    body = {"email": email, "password": password}
    if invite_code:
        body["invitation_code"] = invite_code
    status, data = http("POST", "/auth/register", body, proxy=proxy)
    if status != 200 or data.get("code") != 0:
        return None, f"注册失败: HTTP {status} {json.dumps(data, ensure_ascii=False)[:200]}"
    d = data["data"]
    return {
        "email": email,
        "password": password,
        "access_token": d.get("access_token"),
        "refresh_token": d.get("refresh_token"),
        "expires_in": d.get("expires_in"),
        "user_id": d.get("user", {}).get("id") if isinstance(d.get("user"), dict) else None,
    }, None


def create_key(token, name, group_id, proxy=None):
    body = {"name": name, "group_id": group_id}
    status, data = http("POST", "/keys", body, token=token, proxy=proxy)
    if status != 200 or data.get("code") != 0:
        return None, f"创建密钥失败: HTTP {status} {json.dumps(data, ensure_ascii=False)[:200]}"
    return data["data"].get("key"), None


def save_key(out_path, api_key):
    """把成功创建的 key 追加写入 txt 文件（只写 key，一行一个）"""
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(api_key + "\n")


def main():
    ap = argparse.ArgumentParser(description="马良 AI 纯协议注册机")
    ap.add_argument("-n", "--number", type=int, default=1, help="注册数量（默认1）")
    ap.add_argument("-e", "--email", help="指定邮箱（不指定则随机）")
    ap.add_argument("-p", "--password", default="TestPass12345", help="密码（默认 TestPass12345）")
    ap.add_argument("-c", "--invite", help="邀请码（可选）")
    ap.add_argument("-g", "--group", type=int, default=GROK_GROUP_ID, help="分组id（默认5=Grok）")
    ap.add_argument("-k", "--keyname", default="auto-key", help="密钥名称前缀")
    ap.add_argument("-o", "--out", default=DEFAULT_OUT, help="保存文件路径")
    ap.add_argument("--no-key", action="store_true", help="只注册不创建密钥")
    ap.add_argument("-d", "--delay", type=float, default=5.0, help="每个号之间的间隔秒数（默认5，防限流）")
    ap.add_argument("-r", "--retry", type=int, default=3, help="撞429限流后自动重试次数（默认3）")
    ap.add_argument("-w", "--retry-wait", type=int, default=30, help="429重试等待秒数（默认30，每次翻倍）")
    ap.add_argument("--proxy", help="单个代理，如 http://ip:port 或 https://ip:port")
    ap.add_argument("--proxy-file", help="代理列表文件，一行一个，自动轮换")
    args = ap.parse_args()

    pool = ProxyPool(load_proxies(args.proxy, args.proxy_file))
    if pool.proxies:
        print(f"使用代理池: {len(pool.proxies)} 个代理，自动轮换", flush=True)
    else:
        print("直连模式（未配置代理）", flush=True)

    results = []
    for i in range(args.number):
        proxy = pool.next()
        if proxy:
            print(f"[{i+1}/{args.number}] 注册 {rand_email()} (代理 {proxy}) ...", flush=True)
        else:
            print(f"[{i+1}/{args.number}] 注册 ...", flush=True)

        email = args.email if (args.email and i == 0) else rand_email()
        acct, err = register(email, args.password, args.invite, proxy=proxy)

        # 429 自动退避重试：等 30s/60s/120s，并换下一个代理
        retries = 0
        while err and "429" in err and retries < args.retry:
            wait = args.retry_wait * (2 ** retries)
            print(f"  !! 限流，等待 {wait}s 后重试（换代理）...", flush=True)
            time.sleep(wait)
            proxy = pool.next()
            acct, err = register(email, args.password, args.invite, proxy=proxy)
            retries += 1

        if err:
            print("  !!" + err, flush=True)
            results.append({"email": email, "error": err})
            continue
        print(f"  注册成功 user_id={acct['user_id']}", flush=True)

        if args.no_key:
            results.append({**acct, "api_key": None})
        else:
            key, kerr = create_key(acct["access_token"], f"{args.keyname}-{i+1}", args.group, proxy=proxy)
            if kerr:
                print("  !!" + kerr, flush=True)
                results.append({**acct, "api_key": None, "key_error": kerr})
            else:
                print(f"  密钥创建成功: {key[:12]}...", flush=True)
                results.append({**acct, "api_key": key})
                try:
                    save_key(args.out, key)
                    print(f"  已保存到: {args.out}", flush=True)
                except Exception as e:
                    print(f"  !! 保存失败: {e}", flush=True)
        time.sleep(args.delay)

    print("\n========== 结果 ==========")
    print(f"保存文件: {args.out}")
    ok = 0
    for r in results:
        if r.get("api_key"):
            ok += 1
            print(f"OK   {r['email']}  {r['api_key'][:16]}...")
        elif r.get("error"):
            print(f"FAIL {r['email']}  {r['error'][:80]}")
        else:
            print(f"FAIL {r['email']}  {r.get('key_error', '')[:80]}")
    print(f"\n成功 {ok}/{len(results)}")
    if ok:
        print(f"全部 Key 已写入: {args.out}（一行一个，可直接上传平台）")


if __name__ == "__main__":
    sys.exit(main())
