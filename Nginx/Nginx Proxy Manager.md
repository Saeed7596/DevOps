[Official Document](https://nginxproxymanager.com/guide)

---

# Nginx Proxy Manager
Nginx Proxy Manager is a powerful and easy-to-use reverse proxy manager that simplifies the process of managing Nginx proxy configurations. It offers a web-based interface to manage your Nginx server configurations, SSL certificates, and more, making it much easier for both beginners and advanced users

# Features of Nginx Proxy Manager
- User-friendly web interface to manage reverse proxy settings.
- SSL Certificate Management with support for automatic Let's Encrypt SSL certificates.
- Access Control: Ability to manage permissions and restrict access to your services.
- HTTP/HTTPS support with automatic redirection.
- Docker Support for easy deployment and integration.
- Custom Nginx configuration: Allows you to add advanced custom configurations if necessary.

# Installing 
#### `Step 1`: Install Docker and Docker Compose
#### `Step 2`: Create a Docker Compose file
Create a `docker-compose.yml` file to deploy Nginx Proxy Manager.
```yaml
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```
- `80` and `443`: These ports are for HTTP and HTTPS traffic.
- `81`: This port is for the web interface of Nginx Proxy Manager.
#### `Step 3`: Start the Docker Container
```bash
docker-compose up -d

# If using docker-compose-plugin
docker compose up -d
```
#### `Step 4`: Access the Web Interface
Once the container is up and running, you can access the Nginx Proxy Manager web interface by going to:

```arduino
http://<your-server-ip>:81
```
By default, the login credentials are:
- Username: `admin@example.com`
- Password: `changeme`
You should change these credentials as soon as possible for security purposes.

---

# Important Cloudflare Configuration for SSL
When using Cloudflare as a CDN and reverse proxy for your website, you need to set the SSL mode to "Full" in Cloudflare's SSL/TLS settings to ensure proper handling of HTTPS traffic between Cloudflare and your origin server.

SSL Mode: In the Cloudflare dashboard, navigate to SSL/TLS settings and make sure the SSL mode is set to `Full`.
- Full mode ensures that Cloudflare will connect to your origin server using HTTPS, but Cloudflare's SSL certificate does not need to match the one on the origin server.

Disable Cloudflare CDN Temporarily for SSL Setup:
- Before setting up SSL certificates via Nginx Proxy Manager (or Let's Encrypt), temporarily disable the Cloudflare CDN (orange cloud icon) for your domain.
- This prevents Cloudflare from caching content during the SSL certificate issuance process and allows Nginx Proxy Manager to properly communicate with your origin server to fetch the certificate.
- Once the SSL certificate is successfully created, you can re-enable the CDN (orange cloud icon).

---

# Using Nginx Proxy Manager
Once logged in, you can:

1. Add Proxy Hosts
- Go to Proxy Hosts in the sidebar.
- Click on Add Proxy Host.
- Fill in the required details such as the domain name, scheme (HTTP or HTTPS), and the destination IP/port of the service you want to reverse proxy.
- You can also configure SSL settings to enable Let's Encrypt SSL certificates.
2. Manage SSL Certificates
- Go to SSL Certificates in the sidebar.
- You can create new SSL certificates using Let's Encrypt or upload your own certificates.
3. Access Lists & Permissions
- You can manage user access to different services through Access Lists.
- Restrict access by IP addresses or define rules for user authentication.
4. View Logs
- You can view logs for each proxy host directly in the web interface.

#### Configuring SSL Certificates with Let's Encrypt
Nginx Proxy Manager allows you to easily configure SSL certificates for your services using Let's Encrypt:

- When creating a Proxy Host, check the box to enable SSL.
- Choose Request a new SSL certificate from Let's Encrypt.
- If needed, enable Force SSL to redirect HTTP traffic to HTTPS automatically.

#### Auto-Renewal of SSL Certificates
Nginx Proxy Manager automatically renews SSL certificates issued by Let's Encrypt, so you don’t need to worry about expiration.

#### Advanced Configuration
If needed, you can add custom Nginx configurations by:

1. Going to the Proxy Host settings.
2. Adding custom configuration options under the Advanced tab.
You can add settings like headers, redirects, and more, depending on your requirements.

---

# Conclusion
Nginx Proxy Manager simplifies the management of Nginx proxies, SSL certificates, and web services through an intuitive web interface. With Docker support, you can easily deploy it and start managing your reverse proxies without the hassle of manually editing Nginx configuration files.

By using this tool, you can easily manage your reverse proxies, SSL certificates, and much more, all from a single interface. Make sure your Cloudflare SSL setting is set to "Full" and temporarily disable the CDN during SSL setup for smooth operation.
