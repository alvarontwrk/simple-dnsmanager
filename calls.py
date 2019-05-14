#!/usr/bin/env python

import subprocess

def get_hosts_file():
    hosts = []

    with open('/etc/hosts', 'r') as f:
        hosts = f.readlines();

    return hosts


def get_domains():
    hosts = get_hosts_file()

    for line in hosts:
        if "# TDRC" in line:
            line_number = hosts.index(line)

    return hosts[line_number+1:]


def get_blacklist():
    hosts = get_hosts_file()

    for line in hosts:
        if "# Blacklist" in line:
            blacklist_line = hosts.index(line)
        if "# TDRC" in line:
            tdrc_line = hosts.index(line)

    return hosts[blacklist_line+1:tdrc_line-1]


def get_template_file(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


def block_domain(domain):
    blacklist = get_blacklist()
    domains = get_domains()
    with open('/etc/hosts', 'w') as f:
        f.writelines(get_template_file('template'))
        f.write('\n# Blacklist\n')
        f.writelines(blacklist)
        f.write('0.0.0.0\t\t{}\n'.format(domain))
        f.write('\n# TDRC\n')
        f.writelines(domains)


def unblock_domain(domain):
    domains = get_domains()
    blacklist = get_blacklist()
    new_blacklist = [blocked for blocked in blacklist if
            blocked.split('\t\t')[1].split()[0] != domain]
    with open('/etc/hosts', 'w') as f:
        f.writelines(get_template_file('template'))
        f.write('\n# Blacklist\n')
        f.writelines(new_blacklist)
        f.write('\n# TDRC\n')
        f.writelines(domains)


def add_domain(domain, ip):
    blacklist = get_blacklist()
    domains = get_domains()
    with open('/etc/hosts', 'w') as f:
        f.writelines(get_template_file('template'))
        f.write('\n# Blacklist\n')
        f.writelines(blacklist)
        f.write('\n# TDRC\n')
        f.writelines(domains)
        f.write('{}\t{}\n'.format(ip, domain))


def remove_domain(domain):
    blacklist = get_blacklist()
    domains = get_domains()
    new_domains = [site for site in domains if
            site.split('\t')[1].split()[0] != domain]
    with open('/etc/hosts', 'w') as f:
        f.writelines(get_template_file('template'))
        f.write('\n# Blacklist\n')
        f.writelines(blacklist)
        f.write('\n# TDRC\n')
        f.writelines(new_domains)


def reload_dns():
    subprocess.call(['sudo', 'systemctl', 'reload', 'dnsmasq'])


if __name__ == '__main__':
    block_domain('google.es')
    reload_dns()
