
# OpenSSL Overview

OpenSSL is a robust, full-featured open-source toolkit that implements the Secure Sockets Layer (SSL) and Transport Layer Security (TLS) protocols. It also provides a full-strength general-purpose cryptography library.

---

## 📦 What is OpenSSL?
OpenSSL is used for:
- Creating SSL/TLS certificates
- Encrypting and decrypting data
- Generating private and public key pairs
- Creating certificate signing requests (CSRs)
- Verifying certificates

---

## 🔧 Common OpenSSL Commands

### 1. Generate a Private Key
```bash
openssl genpkey -algorithm RSA -out private.key -aes256
```

### 2. Generate a Public Key from a Private Key
```bash
openssl rsa -pubout -in private.key -out public.key
```

### 3. Create a Certificate Signing Request (CSR)
```bash
openssl req -new -key private.key -out request.csr
```

### 4. Generate a Self-Signed Certificate
```bash
openssl req -x509 -key private.key -in request.csr -out certificate.crt -days 365
```

### 5. Convert PEM to DER Format
```bash
openssl x509 -outform der -in certificate.crt -out certificate.der
```

### 6. Check a Certificate
```bash
openssl x509 -in certificate.crt -text -noout
```

### 7. Verify a Certificate
```bash
openssl verify -CAfile ca_bundle.crt certificate.crt
```

---

## 🔒 File Formats

| Format | Description                   |
|--------|-------------------------------|
| .key   | Private key                   |
| .csr   | Certificate signing request   |
| .crt   | Public certificate            |
| .pem   | Container format              |
| .der   | Binary form of .pem           |

---

## 📚 Additional Info

- Website: https://www.openssl.org/
- Docs: https://wiki.openssl.org/

OpenSSL is widely used in web servers (e.g., Apache, Nginx), VPNs, and other secure applications. Understanding its basics is essential for system administrators and developers alike.
