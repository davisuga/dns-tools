#!/bin/python3
import os, sys
domainName=sys.argv[1]
ip=sys.argv[2]
reverseIp=str(sys.argv[2]).split('.')
reverseIp.pop()
reverseIp=(reverseIp[::-1])

a=""
for i in reverseIp:
	a+=i+"."

reverseIp=a+"in-addr.arpa"
template='''zone "{}" {{
    	type master;
    	file "/etc/bind/for.{}";
    	allow-transfer {{ {}; }};
    	also-notify {{ {}; }};
 }};
zone "{}" {{
    	type master;
    	file "/etc/bind/rev.{}";
    	allow-transfer {{ {}; }};
    	also-notify {{ {}; }};
 }};'''.format(domainName, domainName, ip, ip, reverseIp, domainName, ip, ip)
print(template)
os.system("echo "+template+" >> /etc/bind/named.conf.local")
#ip=ip[:-1]
forDomain='''$TTL 86400
@   IN  SOA     pri.{}. root.{}. (
        2011071001  ;Serial
        3600        ;Refresh
        1800        ;Retry
        604800      ;Expire
        86400       ;Minimum TTL
)
@       IN  NS          pri.{}.
@       IN  NS          sec.{}.
@       IN  A           {}
pri     IN  A           {}
sec     IN  A           {}
client  IN  A           {}
'''.format(domainName, domainName, domainName, domainName, ip, ip, ip, ip)
print(forDomain)
os.system("echo '"+forDomain+"' >> /etc/bind/for."+domainName)
revDomain='''$TTL 86400
@   IN  SOA     pri.{}. root.{}. (
        2011071002  ;Serial
        3600        ;Refresh
        1800        ;Retry
        604800      ;Expire
        86400       ;Minimum TTL
)
@       IN  NS          pri.{}.
@       IN  NS          sec.{}.
@       IN  PTR         {}.
pri     IN  A           {}
sec     IN  A           {}
client  IN  A           {}
200     IN  PTR         pri.{}.
201     IN  PTR         sec.{}.
202     IN  PTR         client.{}.
'''.format(domainName, domainName, domainName, domainName, domainName, ip, ip, ip, domainName, domainName, domainName)
print(revDomain)
os.system("echo '"+revDomain+"' >> /etc/bind/rev."+domainName)
