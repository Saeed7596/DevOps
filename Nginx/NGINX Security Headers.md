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
