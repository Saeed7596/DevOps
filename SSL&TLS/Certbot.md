# SSL and TLS Guide with Certbot Installation

This document provides an overview of SSL/TLS and explains how to obtain SSL certificates using Certbot, both via Linux commands and Docker Compose.

---

## What are SSL and TLS?

| Term                               | Description                                                                                                    |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| **SSL (Secure Sockets Layer)**     | An older protocol for encrypting data over the internet, now deprecated.                                       |
| **TLS (Transport Layer Security)** | The modern, more secure version of SSL, used to protect the integrity and privacy of data during transmission. |

TLS ensures that communications between clients (like browsers) and servers remain private and tamper-proof.

---

## How SSL/TLS Certificates Work

* SSL/TLS certificates verify the identity of a website.
* They enable encrypted HTTPS connections.
* Certificates are issued by trusted Certificate Authorities (CAs).

---

## HTTP-01 vs DNS-01 Challenge

| Method            | Explanation                                                                                  | Requires DNS TXT? |
| :---------------- | :------------------------------------------------------------------------------------------- | :---------------- |
| HTTP-01 Challenge | Certbot proves domain ownership by placing a file on your web server (accessible over HTTP). | No                |
| DNS-01 Challenge  | Certbot proves domain ownership by requiring you to create a DNS TXT record.                 | Yes               |

* **HTTP-01** is simpler for basic SSL certificates and requires ports 80/443 to be accessible.
* **DNS-01** is necessary for **wildcard certificates** (like `*.yourdomain.com`) or when you cannot serve HTTP challenges.

---

## HTTP-01 Challenge Example (No DNS Record Needed)

Already explained above.
Certbot places a validation file inside your webroot folder.

---

## DNS-01 Challenge Example (Needs DNS TXT Record)

1. Install Certbot with DNS plugin (example for Cloudflare):

```bash
sudo apt install certbot python3-certbot-dns-cloudflare
```

2. Run Certbot with DNS Challenge:

```bash
sudo certbot -a dns-cloudflare --dns-cloudflare-credentials ~/.secrets/certbot/cloudflare.ini -d '*.yourdomain.com' -d yourdomain.com --agree-tos --no-eff-email --email your-email@example.com
```

3. Certbot will:

   * Create a special DNS TXT record request.
   * Wait for DNS propagation (you may need to manually create the TXT record if your provider is not automated).

4. After successful validation, Certbot generates your wildcard SSL certificate.

---

## Why Certificate Renewal Should Run More Frequently?

Even though SSL certificates issued by Let's Encrypt are valid for **90 days**, best practice is:

* **Check for renewal at least every 12 hours**.
* Certbot automatically renews certificates when **less than 30 days remain**.


## Obtaining an SSL Certificate with Certbot (Linux Commands)

### 1. Install Certbot

For Ubuntu/Debian:

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

For CentOS/RHEL:

```bash
sudo yum install epel-release
sudo yum install certbot python3-certbot-nginx
```

### 2. Request an SSL Certificate

For a website served by Nginx:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

For standalone (no web server running):

```bash
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

### 3.1. Auto-Renewal

To ensure certificates renew automatically:

```bash
sudo crontab -e
```

Add this line:
Every 12 Hours
```bash
0 0 * * * certbot renew --quiet
```

### 3.2. Verify Automatic Renewal:

```bash
sudo certbot renew --dry-run
```

### 3.2.1. Setup Auto-Renewal:

Certbot installs a cron job or systemd timer automatically that runs twice a day to renew certificates before they expire.

You can check the cron job using:

```bash
cat /etc/cron.d/certbot
```

Typically, it runs every 12 hours.

---

## Obtaining an SSL Certificate with Certbot (Docker Compose)

### 1. Docker Compose File Example

```yaml
version: '3'

services:
  certbot:
    image: certbot/certbot
    container_name: certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c '
      certbot certonly --webroot \
      --webroot-path=/var/www/certbot \
      --email your-email@example.com \
      --agree-tos \
      --no-eff-email \
      -d yourdomain.com -d www.yourdomain.com
    '"
```

> **Note:**
>
> * Make sure ports 80 and 443 are open.
> * You must serve the `./certbot/www` directory over HTTP during the challenge.

### 2. Running Certbot via Docker Compose

```bash
docker compose up certbot
```
Certificates will be saved under `./certbot/conf`.

---

## Automatic Obtaining an SSL Certificate with Certbot (Docker Compose)

### 1. Create a `docker-compose.yml`

```yaml
version: '3'
services:
  certbot:
    image: certbot/certbot
    volumes:
      - ./letsencrypt:/etc/letsencrypt
      - ./webroot:/var/www/html
    entrypoint: ""
    command: >
      bash -c "certbot certonly --webroot -w /var/www/html \
      -d yourdomain.com -d www.yourdomain.com \
      --email your-email@example.com --agree-tos --no-eff-email && \
      trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done"
```

### 2. Explanation:

* `certonly`: Only fetch certificates without trying to install them.
* `--webroot`: Use webroot for authentication.
* `trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done`: A small loop that keeps running inside the container to renew certificates every 12 hours.

Thus, **inside Docker Compose**, the certificate will be automatically renewed twice a day.

> **Tip:** Make sure your web server (e.g., Nginx) reloads its configuration after a certificate is renewed.

Example for Nginx reload in Docker Compose:

```yaml
command: bash -c "while :; do sleep 12h && nginx -s reload; done"
```

---

**Congratulations! 🎉 Now you understand SSL/TLS and can easily obtain certificates using Certbot.**
