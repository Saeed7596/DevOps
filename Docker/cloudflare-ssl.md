# NGINX Configuration with Cloudflare SSL (Flexible Mode)

This guide explains how to set up NGINX to use Cloudflare’s SSL without requiring an SSL certificate on your server. By enabling **Flexible SSL** on Cloudflare, HTTPS traffic will be secured between the user and Cloudflare, while HTTP will be used between Cloudflare and your server.

---

## 1. Add Your Domain to Cloudflare (If Not Already Done)

1. Log in to your [Cloudflare dashboard](https://dash.cloudflare.com/).
2. Select **Add Site** and enter your domain name (e.g., `example.com`).
3. Choose a Cloudflare plan and continue with the setup.
4. Follow the instructions to update your domain’s nameservers to the ones provided by Cloudflare. 

---

## 2. Create a DNS Record for the Subdomain

1. In your Cloudflare dashboard, go to your domain’s **DNS** settings.
2. Click **Add Record** and enter the following details:

   - **Type**: Select **A** if pointing to an IP address, or **CNAME** if pointing to another domain.
   - **Name**: `@` (This represents the root domain, like `example.com`)
   - **Name**: Enter the subdomain (e.g., `subdomain` for `subdomain.example.com`).
   - **IPv4 address**: Enter the server’s IP address if using an A record.
   - **Proxy Status**: Set to **Proxied** (orange cloud icon) to enable CDN and SSL.

3. Click **Save**.

---

## 3. Enable SSL and CDN

1. Go to the **SSL/TLS** section in Cloudflare’s dashboard.
2. Set the SSL mode to **Flexible**. This mode encrypts traffic between users and Cloudflare, but not between Cloudflare and your origin server.
3. Cloudflare CDN is now active, as indicated by the **Proxied** setting on the DNS record.

> **Note:** Flexible SSL mode does not require an SSL certificate on your server. If you need full end-to-end encryption, consider switching to **Full SSL** (requires an SSL certificate on your server).

---

## 4. Verify Cloudflare CDN and SSL Are Active

1. Once DNS propagation completes (usually within a few minutes to an hour), your subdomain (`subdomain.example.com`) should be accessible over HTTPS.
2. To confirm Cloudflare is serving the content, inspect the response headers. You should see headers such as `cf-cache-status` and `server: cloudflare`, which indicate Cloudflare is active.

---

With these steps, Cloudflare is set up to provide both SSL and CDN for your subdomain.

---

## 5. Configure NGINX to Listen on Port 80 Only

Since Cloudflare handles SSL, you only need to configure NGINX to listen on port 80 (HTTP) and proxy the traffic to your Docker container.

### Example NGINX Configuration

Replace `example.com` with your subdomain and `172.17.0.1:3033` with the IP address and port of your Docker container.

```nginx
server {
    listen 80;
    server_name example.com;

    client_max_body_size 32M;

    location / {
        proxy_read_timeout      300;
        proxy_connect_timeout   300;
        proxy_redirect          off;

        proxy_set_header        Host                $http_host;
        proxy_set_header        X-Real-IP           $remote_addr;
        proxy_set_header        X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto   http;
        proxy_set_header        X-Frame-Options     SAMEORIGIN;
        proxy_pass http://172.17.0.1:<port-number>;
    }
}
```
