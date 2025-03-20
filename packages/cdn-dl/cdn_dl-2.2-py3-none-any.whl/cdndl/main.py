#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from os import path
import os
import random
import re
import signal
import sys
import threading
from time import sleep, time
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import urllib3
import ipaddress
from urllib.parse import urlparse
from collections import defaultdict
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError

DEBUG = False
# 用这个key 表明可以匹配任意域名
ALL_DOMAIN_KEY = 'all_domain'
# 默认ALI DNS API
DEF_DNS_API = 'https://dns.alidns.com/resolve?name={}&type=1'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
]


urllib3.disable_warnings()

# 注册全局退出监听
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

def is_ip_address(ip_str: str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip is not None
    except ValueError:
        return False

HOSTNAME_PATTERN = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
def is_domain_name(string: str):
    if re.match(HOSTNAME_PATTERN, string) or string == ALL_DOMAIN_KEY:
        return True
    else:
        return False

def is_valid_port(port: int):
    return port > 0 and port < 65535

def parse_str_config(config_str: str):
    def method1():
        parts = config_str.split()
        ip = parts[0]
        hostname = parts[1] if len(parts) == 2 else ALL_DOMAIN_KEY
        port = 443
        return hostname, ip, port

    def method2():
        parts = config_str.split(':')
        ip = parts[0]
        port = 443
        hostname = ALL_DOMAIN_KEY
        if len(parts) >= 2:
            if is_domain_name(parts[1]):
                hostname = parts[1]
            else:
                try:
                    port = int(parts[1])
                except:
                    port =  -1
        if len(parts) >= 3:
            try:
                port = int(parts[1])
            except:
                port = -1
            hostname = parts[2]
        return hostname, ip, port

    for fn in method1, method2:
        hostname, ip, port = fn()
        if is_domain_name(hostname) and is_ip_address(ip) and is_valid_port(port):
            return hostname, ip, port
    return None, None, None


def gen_cdn_map(configs: List[str]):
    cdn_map = defaultdict(list)
    real_configs = []
    for cdn_config in configs:
        file_path = path.join(cdn_config)
        if path.exists(file_path) and path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    real_configs.append(line)
        else:
            real_configs.append(cdn_config)
    for cfg in real_configs:
        hostname, ip, port = parse_str_config(cfg)
        cdn_map[hostname].append((ip, port))
    for k, v in cdn_map.items():
        cdn_map[k] = list(dict.fromkeys(v))
    if DEBUG and cdn_map:
        print()
        print('CDN 配置如下:')
        for k, v in cdn_map.items():
            print('    ',k, v)
        print()
    return cdn_map

class CdnCenter:
    def __init__(self, configs: List[str]):
        self.cdn_map = gen_cdn_map(configs)
        self.choice_map = defaultdict(list)

    def get_all_cdn_for_domain(self, hostname):
        choices = self.choice_map.get(hostname)
        if not choices:
            choices = self.cdn_map.get(hostname, [])
            if not choices:
                all_domain_choices = self.cdn_map.get(ALL_DOMAIN_KEY, [])
                choices.extend(all_domain_choices)
                dns = dns_lookup(hostname)
                for r in dns:
                    choices.append((r, 443))
            choices = list(dict.fromkeys(choices))
            self.choice_map[hostname] = choices
        return choices

def parse_url(url: str):
    parsed_url = urlparse(url)
    return parsed_url.hostname, parsed_url.path

def dns_lookup(domain):
    def dns_lookup_internal():
        has_error = False
        dns = []
        try:
            with requests.get(DEF_DNS_API.format(domain), headers={'accept': 'application/dns-json'}) as res:
                json_data = res.json()
                if 'Answer' in json_data:
                    records = json_data['Answer']
                    for record in records:
                        if record['type'] == 1:
                            dns.append(record['data'])
        except:
            has_error = True
        return has_error, dns

    print(f"Performing DNS lookup for {domain}...")
    has_error, dns = dns_lookup_internal()
    retry_cnt = 0
    while has_error and retry_cnt < 3:
        stay_seconds = round(random.uniform(1, 3), 2)
        print(f"Retrying DNS lookup for {domain} in {stay_seconds}s...")
        sleep(stay_seconds)
        has_error, dns = dns_lookup_internal()
        retry_cnt += 1
    return dns

def show_freshable_content(content: str):
    print(content, end='\r')
    sys.stdout.flush()

class SpeedUpdater:

    def __init__(self, total_size):
        self.total_size = total_size
        self.current_size = 0
        self.last_ts = 0
        self.current_ts = 0
        self.last_size = 0
        self.start_ts = 0
        self.spd_thread = threading.Thread(target=self.__update_spd_info, daemon=True)
        self.running = False

    def __update_spd_info(self):
        self.running = True
        while self.running:
            self.current_ts = time()
            if self.current_ts - self.last_ts > 0.9 and self.current_ts - self.start_ts > 0.9:
                current_speed = int((self.current_size - self.last_size) / ((self.current_ts - self.last_ts) * 1024))
                avg_speed = int(self.current_size / ((self.current_ts - self.start_ts) * 1024))
                self.last_size =  self.current_size
                self.last_ts = self.current_ts
                percent = 0
                if self.total_size > 0:
                    percent = round((self.current_size * 100) / self.total_size, 2)
                spd_info = '    当前下载速度(cur/avg)为: {}/{} kB/s'.format(current_speed, avg_speed)
                if percent:
                    spd_info += ',进度为{}%'.format(percent)
                show_freshable_content(spd_info)
            else:
                sleep(0.1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.running = False
        self.spd_thread.join()

    def update(self, size: int):
        self.current_size += size
        if self.start_ts == 0:
            self.start_ts = time()
            self.spd_thread.start()

def download_file(url: str, save_path: str, cdn_configs: List[str], ua: bool, ts: int, timeout: int, retry: int):

    def get_ip_port(choices: list, used_choices: list):
        available_choices = [choice for choice in choices if choice not in used_choices]
        if available_choices:
            return random.choice(available_choices)
        else:
            return None, None

    res = False
    cdn = CdnCenter(cdn_configs)
    headers = {}
    if ua:
        headers.update({'User-Agent': random.choice(USER_AGENTS)})
    bad_cdn_map = defaultdict(list)
    while True:
        def handle_error():
            print('请求{} 异常\n'.format(url))
            bad_cdn_map[hostname].append((ip, port))

        hostname, _ = parse_url(url)
        ip, port = get_ip_port(cdn.get_all_cdn_for_domain(hostname), bad_cdn_map.get(hostname, []))
        if not ip:
            print('所有CDN 都无法下载, 退出中... ...')
            break
        print('cdn 配置为: {}:{}:{}'.format(hostname, ip, port))
        pool = urllib3.HTTPSConnectionPool(
            ip,
            assert_hostname=hostname,
            server_hostname=hostname,
            port=port,
            cert_reqs='CERT_NONE',
        )
        headers.update({'Host': hostname})
        try:
            with pool.urlopen('GET', url,
                             redirect=False,
                             headers=headers,
                             assert_same_host=False,
                             timeout=timeout,
                             preload_content=False,
                             retries=urllib3.Retry(retry, backoff_factor=2, status_forcelist=[404, 500, 502, 503, 504])) as response:
                # 检查是否为重定向
                print('请求{} 返回 {}\n'.format(url, response.status))
                if response.status in (301, 302, 303, 307, 308) and 'Location' in response.headers:
                    # 获取重定向的 URL
                    url = response.headers['Location']
                    print('重定向为: {}'.format(url))
                    bad_cdn_map.clear()
                    continue
                if response.status == 200:
                    total_size = int(response.headers.get('content-length', 0))
                    with open(save_path, 'wb') as file, SpeedUpdater(total_size) as speed_updater:
                        for data in response.stream(ts):
                            file.write(data)
                            speed_updater.update(len(data))
                        res = True
                        break
                else:
                    handle_error()
                    continue
        except (ConnectTimeoutError, MaxRetryError):
            handle_error()
            continue
        except Exception as e:
            print('下载文件异常:', e)
            break
    return res


def get_cdn():
    def parse_domains():
        domains = []
        for domain in domain_arg:
            if path.exists(domain) and path.isfile(domain):
                with open(domain, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if is_domain_name(line):
                            domains.append(line)
            else:
                if is_domain_name(domain):
                    domains.append(domain)
        if not domains:
            raise RuntimeError('未能读取到有效域名, 请检查参数!')
        domains = list(dict.fromkeys(domains))
        return domains

    def init_cdn_map():
        cdn_map = gen_cdn_map(cdn_configs)
        return cdn_map

    def gen_all_choices_for_domain(hostname):
        if not cdn_map:
            return []
        choices = cdn_map.get(hostname)
        if not choices:
            choices = []
            for _, v in cdn_map.items():
                choices.extend(v)
        return choices

    def get_ip_port(choices: list, used_choices: list):
        available_choices = [choice for choice in choices if choice not in used_choices]
        if available_choices:
            return random.choice(available_choices)
        else:
            return None, None

    def get_dns(domains: List[str]):
        def dns_lookup(domain):
            def dns_lookup_internal():
                dns = []
                used_choices = []
                headers = {'accept': 'application/dns-json'}
                url = api.format(domain)
                hostname, _ = parse_url(url)
                headers.update({'Host': hostname})
                while True:
                    if not choices:
                        print('CDN 为空, 跳过使用CDN 解析')
                        pool = urllib3.HTTPSConnectionPool(
                            hostname,
                            assert_hostname=hostname,
                            server_hostname=hostname,
                            cert_reqs='CERT_NONE',
                        )
                    else:
                        ip, port = get_ip_port(choices, used_choices)
                        if not ip:
                            print('所有CDN 都无法解析, 退出中... ...')
                            break
                        used_choices.append((ip, port))
                        print('使用CDN: {}:{}:{} 解析 {}'.format(hostname, ip, port, domain))
                        pool = urllib3.HTTPSConnectionPool(
                            ip,
                            assert_hostname=hostname,
                            server_hostname=hostname,
                            cert_reqs='CERT_NONE',
                            port=port
                        )
                    try:
                        with pool.urlopen('GET', url,
                                         redirect=False,
                                         headers=headers,
                                         assert_same_host=False,
                                         timeout=timeout,
                                         preload_content=False,
                                         retries=urllib3.Retry(retry, backoff_factor=1)) as response:
                            json_data = json.loads(response.data.decode('utf-8'))
                            if 'Answer' in json_data:
                                records = json_data['Answer']
                                for record in records:
                                    if record['type'] == 1:
                                        dns.append(record['data'])
                            if response.status == 200:
                                break
                    except Exception as e:
                        print('查询DNS 网络错误!')
                        if not cdn_map:
                            break
                        continue
                return dns

            print(f"Performing DNS lookup for {domain}...")
            choices = gen_all_choices_for_domain(domain)
            dns = dns_lookup_internal()
            return domain, dns

        dns_map = defaultdict(list)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_domain = {executor.submit(dns_lookup, domain) for domain in domains}
            for future in as_completed(future_to_domain):
                domain, dns = future.result()
                if dns:
                    dns_map[domain] = dns
            executor.shutdown(wait=True)
        for k, v in dns_map.items():
            dns_map[k] = list(dict.fromkeys(v))
        return dns_map

    def save_or_print_hosts():
        if not dns_map:
            print('DNS 记录为空, 请检查域名是否正确!')
            return
        print('DNS 解析记录如下:')
        for k, v in dns_map.items():
            for ip in v:
                line = '{} {}'.format(ip, k)
                print(line)
        if path_arg:
            save_path = path.join(path_arg)
            with open(save_path, 'w', encoding='utf-8') as f:
                for k, v in dns_map.items():
                    for ip in v:
                        line = '{} {}'.format(ip, k)
                        f.write(line)
                        f.write('\n')
            print('hosts 文件已导出到 {}'.format(save_path))

    parser = argparse.ArgumentParser(description='cdn-get 配置')
    parser.add_argument('-o', '--out', type=str, default=None, help='输出hosts 文件路径')
    parser.add_argument('-c', '--cdn', nargs='+', default=[], help='cdn configs配置,支持ip| ip:port |ip:port:host 字串或文本或host文件')
    parser.add_argument('-T', '--thread', type=int, default=8, help='多线程数量')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='下载请求超时时间, 默认10s')
    parser.add_argument('-r', '--retry', type=int, default=3, help='下载请求重试次数, 默认3')
    parser.add_argument('domain', nargs='+', help='需要获取cdn的域名或者文本')
    # 'https://dns.google/resolve?name={}&type=A'
    parser.add_argument('--api', type=str, default=DEF_DNS_API, help='dns api, 默认ali, 使用CF 使用cf dns')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="是否打印调试信息")
    args = parser.parse_args()
    domain_arg = args.domain
    path_arg = args.out
    api = args.api
    if api == 'CF':
        api = 'https://cloudflare-dns.com/dns-query?name={}&type=A'
    print('DNS API:', api)
    threads = args.thread
    timeout = args.timeout
    retry = args.retry
    global DEBUG
    DEBUG = args.debug
    domains = parse_domains()
    print('待解析域名列表:', domains)
    cdn_configs = args.cdn
    url = api.format(domains[0])
    cdn_map = init_cdn_map()
    dns_map = get_dns(domains)
    save_or_print_hosts()

def main():
    parser = argparse.ArgumentParser(description='cdn-dl 下载配置')
    parser.add_argument('-u', '--url', type=str, required=True, help='文件下载url')
    parser.add_argument('-o', '--out', type=str, required=True, help='文件下载路径')
    parser.add_argument('cdn', nargs='+', help='cdn configs配置,支持ip| ip:port |ip:port:host 字串或文本或host文件')
    parser.add_argument('-ua', '--use_agent', action='store_true', default=False, help='是否使用user agent')
    parser.add_argument('-ts', '--trunk_size', type=int, default=8192, help='下载使用的trunk size, 默认8192')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='下载请求超时时间, 默认10s')
    parser.add_argument('-r', '--retry', type=int, default=3, help='下载请求重试次数, 默认3')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="是否打印调试信息")
    args = parser.parse_args()
    url = args.url
    save_path = path.join(args.out)
    cdn_config = args.cdn
    ua = args.use_agent
    ts = args.trunk_size
    timeout = args.timeout
    retry = args.retry
    global DEBUG
    DEBUG = args.debug
    res = download_file(url, save_path, cdn_config, ua, ts, timeout, retry)
    msg = '从{} 下载文件到{} {}'.format(url, save_path, '成功' if res else '失败')
    print(msg)

if __name__ == '__main__':
    get_cdn()