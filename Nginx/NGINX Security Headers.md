# NGINX Security Headers

Here is a collection of security headers you can add to NGINX to protect your website. These headers help safeguard your site from various attacks.

## Security Headers:

```nginx
# Prevent MIME type sniffing
add_header X-Content-Type-Options nosniff;

# Prevent Cross-Site Scripting (XSS) attacks
add_header X-XSS-Protection "1; mode=block";

# Prevent site from being loaded in an iframe (Clickjacking attack)
add_header X-Frame-Options SAMEORIGIN;

# Enforce HTTPS usage (Strict Transport Security)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Prevent content from being loaded in certain formats like ZIP or EXE
add_header X-Permitted-Cross-Domain-Policies none;

# Disable Cross-Origin Resource Sharing (CORS)
add_header Access-Control-Allow-Origin "null";

# Prevent sending browser-related referrer information
add_header Referrer-Policy no-referrer-when-downgrade;

# Disable sending information about server version
server_tokens off;

# Prevent potential HTTP-related attacks
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';";

# Prevent browser feature access such as microphone and camera
add_header Feature-Policy "microphone 'none'; camera 'none';";

# Prevent sending content security headers for self-hosted resources
add_header X-Content-Security-Policy "default-src 'self'";

# Prevent files from opening automatically
add_header X-Download-Options noopen;

# Prevent unnecessary DNS prefetching
add_header X-DNS-Prefetch-Control "off";
```
```nginx
# جلوگیری از حدس زدن نوع MIME
add_header X-Content-Type-Options nosniff;

# جلوگیری از حملات Cross-Site Scripting (XSS)
add_header X-XSS-Protection "1; mode=block";

# جلوگیری از بارگذاری سایت در داخل iframe (حمله Clickjacking)
add_header X-Frame-Options SAMEORIGIN;

# اطمینان از استفاده از HTTPS (Strict Transport Security)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# جلوگیری از ارسال محتوا در قالب فایل‌های ZIP و EXE و ...
add_header X-Permitted-Cross-Domain-Policies none;

# جلوگیری از اشتراک‌گذاری منابع بین دامنه‌ای (CORS)
add_header Access-Control-Allow-Origin "null";

# جلوگیری از ارسال هدرهای مربوط به انواع مختلف مرورگر
add_header Referrer-Policy no-referrer-when-downgrade;

# جلوگیری از ارسال اطلاعات درباره نسخه سرور
server_tokens off;

# جلوگیری از حملات احتمالی به تنظیمات HTTP
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';";

# جلوگیری از ارسال هدرهای مرتبط با اشکال‌زدایی مرورگر
add_header Feature-Policy "microphone 'none'; camera 'none';";

# جلوگیری از درخواست‌های محتوای خود (X-Content-Security-Policy)
add_header X-Content-Security-Policy "default-src 'self'";

# جلوگیری از ارسال هدرهای ارتباطی برای URLهای درخواست شده
add_header X-Download-Options noopen;

# جلوگیری از ارسال هدرهای امنیتی مربوط به کانال‌ها
add_header X-DNS-Prefetch-Control "off";
```
```nginx
server_tokens off; # Disables displaying the Nginx version in HTTP headers to prevent attackers from exploiting known vulnerabilities.

add_header X-Content-Type-Options nosniff; # Prevents browsers from interpreting files as a different MIME type, enhancing security against MIME sniffing attacks.

add_header X-XSS-Protection "1; mode=block"; # Enables browser's built-in XSS protection and blocks the page if an attack is detected.

add_header X-Robots-Tag "index, follow"; # Allows search engines to index the page and follow its links for better SEO.

add_header X-Download-Options noopen; # Prevents files downloaded from being automatically executed in some browsers (e.g., Internet Explorer).

add_header X-Permitted-Cross-Domain-Policies none; # Blocks access to Adobe cross-domain policy files, restricting resource sharing from unauthorized domains.

add_header Referrer-Policy "strict-origin-when-cross-origin"; # Controls how much referrer information is sent with requests to enhance privacy while maintaining analytics.

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always; 
# Enforces HTTPS by instructing browsers to only connect over HTTPS for the specified duration (1 year here). 
# Use `preload` only if you intend to submit your domain to the HSTS preload list.

add_header Content-Security-Policy "default-src 'self'; script-src 'self'; object-src 'none'; style-src 'self'; frame-ancestors 'none';" always;
# Restricts the sources from which content like scripts, styles, and frames can be loaded.
# Adjust the policy based on your website's needs to prevent XSS and data injection attacks.

add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()";
# Restricts access to browser features like geolocation, microphone, camera, and payment APIs.

add_header Cross-Origin-Embedder-Policy "require-corp"; 
# Ensures resources loaded into the page are same-origin or explicitly allowed (mitigates side-channel attacks).

add_header Cross-Origin-Opener-Policy "same-origin"; 
# Prevents other domains from accessing your pages in the same browser context, enhancing isolation.

add_header Cross-Origin-Resource-Policy "same-origin"; 
# Restricts cross-origin resource sharing to mitigate resource-based attacks.

add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
# Prevents caching of sensitive content to avoid exposing private data in shared environments.

add_header Expect-CT "enforce, max-age=86400"; 
# Helps detect and prevent misissued TLS certificates for your domain.

add_header X-Frame-Options "DENY"; 
# Prevents the site from being embedded in iframes to protect against clickjacking attacks.

add_header Set-Cookie "Secure; HttpOnly; SameSite=Strict"; 
# Ensures cookies are sent only over HTTPS, inaccessible to JavaScript, and limited to the same site for CSRF prevention.

```
```nginx
server_tokens off;

add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header X-Robots-Tag "index, follow";
add_header X-Download-Options noopen;
add_header X-Permitted-Cross-Domain-Policies none;
add_header Referrer-Policy "strict-origin-when-cross-origin";

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; object-src 'none'; style-src 'self'; frame-ancestors 'none';" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()";
add_header Cross-Origin-Embedder-Policy "require-corp";
add_header Cross-Origin-Opener-Policy "same-origin";
add_header Cross-Origin-Resource-Policy "same-origin";
add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
add_header Expect-CT "enforce, max-age=86400";
add_header X-Frame-Options "DENY";
add_header Set-Cookie "Secure; HttpOnly; SameSite=Strict";
```

# SSL Cipher
### If your goal is to have a more precise choice of algorithms, it makes more sense to use the first setting (ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';).
### If you want to use a generic and secure setting, the second setting (ssl_ciphers HIGH:!aNULL:!MD5;) would be more appropriate.
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
```
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers HIGH:!aNULL:!MD5;
```
# HTTP2
### Add in default.conf in any server block:
```nginx
listen 443 ssl http2;
```
- ### Check HTTP2
  ```bash
  curl -I --http2 https://yourdomain.com
  ```
  Output:
  ```bash
  HTTP/2 200
  server: nginx
  date: Mon, 18 Nov 2024 10:00:00 GMT
  content-type: text/html; charset=UTF-8
  ```
# File Locations:
- `/etc/nginx/nginx.conf:` This file is the main Nginx configuration file. You can add global SSL settings here, but it’s generally better to modify the specific server block files if you have multiple sites.
- `/etc/nginx/sites-available/yourdomain.conf:` If you're using a configuration structure with separate site configuration files, you can add these settings in the specific configuration file for your domain.
- `/etc/nginx/conf.d/:` This directory may contain general configuration files for your server. You could add the SSL settings and security headers in a file here, such as ssl-settings.conf.
## Restart nginx
```bash
docker compose -f docker-nginx.yml restart nginx
# or
docker exec nginx nginx -t
docker exec nginx nginx -s reload
```
# Using Online Tools for Checking:
- [SSL Server Test](https://www.ssllabs.com/ssltest/)
- [Key CDN](https://www.keycdn.com/features)
