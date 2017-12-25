# -*- coding: utf-8 -*-
import socket, re, sys
import net

def whois_request(domain, server, port=43):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(domain)
	print(server)
	print(port)
	sock.connect((server, port))
	sock.send(("%s\r\n" % domain).encode("utf-8"))
	buff = b""
	while True:
		data = sock.recv(1024)
		if len(data) == 0:
			break
		buff += data
	print buff;
	return buff.decode("utf-8")

def get_server(suffix = ''):
    suffixs = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.internic.net',
        'cn': 'whois.cnnic.net.cn',
        'cc': 'whois.nic.cc'
    }
    if suffixs.has_key(suffix):
        return suffixs[suffix]
    return ''

def get_suffix(domain = ''):
    domain = domain.strip().lower()
    domainSplit = domain.split('.', 1)
    if len(domainSplit) == 2:
        return domainSplit[1]
    return ''

def get_whois(domain = '', timeout = 30):
    data = {'success': 0, 'code': 0, 'info': ''}
    suffix = get_suffix(domain)
    if not suffix:
        data['code'] = 400
        data['info'] = 'Not a domain'
        return data
    server = get_server(suffix)
    if not server:
        data['code'] = 401
        data['info'] = 'Not find a server'
        return data

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        ret = s.connect((server, 43))
	print ret;
    except:
        s.close()
        data['code'] = 500
        data['info'] = 'Can not connect to the server'
        return data
    s.send(domain + 'rn')
    info = ''
    while 1:
        try:
            res = s.recv(1024)
        except:
            s.close()
            data['code'] = 501
            data['info'] = 'Connect to the server timeout'
            return data
        if not res:
            break
        else:
            info += res
    s.close()
    data['success'] = 1
    data['code'] = 200
    data['info'] = info
    return data

def get_reginfo(domain = ''):
    #data = get_whois(domain)
    server = 'whois.verisign-grs.com'
    data = whois_request(domain, )
    if not data['success']:
        return data
    suffix = get_suffix(domain)
    if suffix == 'cn':
        pattern = 'no matching record.'
    else:
        pattern = 'No match for '

    if data['info'].find(pattern) >= 0:
        data['info'] = 'Not be registered'
    else:
        data['code'] = 201
        data['info'] = 'Has be registered'

    return data


def input_command():
    try:
        cmd = raw_input('>')
    except KeyboardInterrupt:
        return ''
    return cmd

def input_filesource():
    try:
        filesource = raw_input('>')
    except KeyboardInterrupt:
        return ''
    if not filesource:
        filesource = './data.txt'
    return filesource

def input_suffix():
    try:
        suffix = raw_input('>')
    except KeyboardInterrupt:
        return ''
    if not suffix:
        suffix = 'com'
    return suffix

def input_domain():
    try:
        domain = raw_input('>')
    except KeyboardInterrupt:
        return ''
    return domain


if __name__ == '__main__':
    import sys, os
    print 'Choose: 1.Domains 2.Keywords  3.Whois'
    cmd = input_command()
    if cmd == '1':
        suffix = ''
    elif cmd == '2':
        print 'Enter suffix for Keywords, leave empty will use "com"'
        while 1:
            suffix = input_suffix()
            if get_server(suffix):
                suffix = '.' + suffix
                break
            else:
                print 'Inviable suffix'
            if not suffix:
                sys.exit(0)
    elif cmd == '3':
        print 'Enter a domain to get the whois info'
        while 1:
            domain = input_domain()
            if not domain:
                sys.exit(0)
            whois = get_whois(domain)
            whois = net.get_whois_raw(domain)
            print whois['info'].decode('utf-8').encode(sys.getfilesystemencoding())
    else:
        print 'Not a valiable command'
        sys.exit(0)
    print 'Enter the path of data file, leave empty will use "./data.txt"'
    while 1:
        filesource = input_filesource()
        if not filesource:
            sys.exit(0)
        if os.path.isfile(filesource):
            break
        else:
            print 'File not exisits'

    filesuccess = './_ok.txt'
    fileerror = './_error.txt'
    fsource = open(filesource, 'r')
    fsuccess = open(filesuccess, 'w')
    ferror = open(fileerror, 'w')

    for line in fsource:
        line = line.strip()
        if not line:
            continue
        domain = line + suffix
        reginfo = get_reginfo(domain)
        if reginfo['success'] and reginfo['code'] == 200:
            fsuccess.write(domain + 'n')
        elif not reginfo['success']:
            ferror.write(domain + ': ' + reginfo['info'] + 'n')
        else:
            continue

    fsource.close()
    fsuccess.close()
    ferror.close()

    print 'Done! Check "_ok.txt" "_error.txt" for detail. Press Enter to exit.'

    try:
        raw_input()
    except KeyboardInterrupt:
        sys.exit(0)
