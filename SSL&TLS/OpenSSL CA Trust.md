# Create Root CA

This Root CA becomes the primary trust authority for the cluster:
```bash
mkdir -p /etc/nginx/certs && cd /etc/nginx/certs

openssl genrsa -out rootCA.key 4096

openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.crt -subj "/C=IR/ST=Tehran/L=Tehran/O=CompanyName/OU=DevOps/CN=CompanyName-Root-CA"
```

📌 The `rootCA.crt` file is the one that should ultimately go into the additionalTrustBundle.

```bash
openssl genrsa -out nexus.key 4096

cat > nexus-openssl.cnf <<EOF
[ req ]
default_bits       = 4096
prompt             = no
default_md         = sha256
req_extensions     = req_ext
distinguished_name = dn

[ dn ]
C=IR
ST=Tehran
L=Tehran
O=CompanyName
OU=DevOps
CN=nexus.example.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = nexus.example.com
DNS.2 = docker.example.com
EOF

openssl req -new -key nexus.key -out nexus.csr -config nexus-openssl.cnf

openssl x509 -req -in nexus.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial \
-out nexus.crt -days 1095 -sha256 -extensions req_ext -extfile nexus-openssl.cnf
```
