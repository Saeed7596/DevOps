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
