```cfg
global
  log         127.0.0.1 local2
  pidfile     /var/run/haproxy.pid
  maxconn     4000
  daemon
defaults
  mode                    http
  log                     global
  option                  dontlognull
  option http-server-close
  option                  redispatch
  retries                 3
  timeout http-request    10s
  timeout queue           1m
  timeout connect         10s
  timeout client          1m
  timeout server          1m
  timeout http-keep-alive 10s
  timeout check           10s
  maxconn                 3000
listen api-server-6443 
  bind *:6443
  mode tcp
  option  httpchk GET /readyz HTTP/1.0
  option  log-health-checks
  balance roundrobin
  server bootstrap bootstrap-ip-address:6443 verify none check check-ssl inter 10s fall 2 rise 3 backup 
  server master0 master0-ip-address:6443 weight 1 verify none check check-ssl inter 10s fall 2 rise 3
  server master1 master1-ip-address:6443 weight 1 verify none check check-ssl inter 10s fall 2 rise 3
  server master2 master-ip-address:6443 weight 1 verify none check check-ssl inter 10s fall 2 rise 3
listen machine-config-server-22623 
  bind *:22623
  mode tcp
  server bootstrap bootstrap-ip-address:22623 check inter 1s backup 
  server master0 master0-ip-address:22623 check inter 1s
  server master1 master1-ip-address:22623 check inter 1s
  server master2 master2-ip-address:22623 check inter 1s
listen ingress-router-443 
  bind *:443
  mode tcp
  balance source
  server compute0 compute0-ip-address:443 check inter 1s
  server compute1 compute1-ip-address:443 check inter 1s
listen ingress-router-80 
  bind *:80
  mode tcp
  balance source
  server compute0 compute0-ip-address:80 check inter 1s
  server compute1 compute1-ip-address:80 check inter 1s
```
