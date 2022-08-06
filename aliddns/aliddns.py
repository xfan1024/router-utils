#!/usr/bin/env python3
import sys
import re
import ipaddress
import subprocess
import time

from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException


def read_config(config_reader):
    line_pattern = re.compile(r'^\s*(.*?)\s*(?:#.*)?$')
    kv_pattern = re.compile(r'^\s*(.*?)\s*=\s*(.*)\s*$')
    result = {}
    for line in config_reader:
        m = line_pattern.match(line)
        line = m.group(1)
        if len(line) == 0:
            continue
        m = kv_pattern.match(line)
        if not m:
            continue
        result[m.group(1)] = m.group(2)
    return result

def get_ipv6_from_interface(ifname):
    command = f"ip a show {ifname} | egrep 'inet6 .* scope global' | awk '{{print $2}}'"
    lines = subprocess.check_output(command, shell=True).decode().strip().split()
    choose_ip = None
    for ip in lines:
        if len(ip) == 0:
            continue
        ip = ipaddress.ip_interface(ip).ip
        if choose_ip == None or ip < choose_ip:
            choose_ip = ip

    if choose_ip == None:
        return None
    return str(choose_ip)

def get_record_value(config):
    if config['Type'] == 'AAAA':
        return get_ipv6_from_interface(config['Interface'])
    if config['Type'] == 'A':
        return get_ipv4_from_interface(config['Interface'])
    assert(False)

def aliclient(config):
    credentials = AccessKeyCredential(config['AccessKeyId'], config['AccessKeySecret'])
    try:
        region = config['Region']
    except KeyError:
        region = ''
    client = AcsClient(region_id=region, credential=credentials)
    return client

def do_update(config, client, value):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RecordId(config['RecordId'])
    request.set_RR(config['RR'])
    request.set_Type(config['Type'])
    request.set_Value(value)
    try:
        client.do_action_with_exception(request)
        return True
    except ServerException as e:
        if e.get_error_code() == 'DomainRecordDuplicate':
            return True
        print(str(e), file=sys.stderr)
        return False
    except ClientException as e:
        print(str(e), file=sys.stderr)
        return False
    

def start_update(config):
    sleep_value = 10
    if 'Delay' in config:
        sleep_value = float(config['Delay'])

    client = aliclient(config)
    prev_value = None
    while True:
        value = get_record_value(config)
        if value and prev_value != value:
            if do_update(config, client, value):
                prev_value = value
        time.sleep(sleep_value)

def main():
    config_file = sys.argv[1]
    with open(config_file, 'r') as reader:
        config = read_config(reader)
    start_update(config)

if __name__ == '__main__':
    main()
