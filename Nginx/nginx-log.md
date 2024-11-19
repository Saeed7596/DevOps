# Enabling Debug Mode in NGINX Logging

NGINX allows detailed logging for debugging purposes. By enabling the `debug` level, all log levels (`debug`, `info`, `warn`, `error`, etc.) will be included in the logs, providing comprehensive insights into the server's operation.

## Log Levels in NGINX
Log levels in NGINX, ordered from the most detailed to the most critical, are as follows:
1. `debug`: Logs extensive details about requests, responses, and server behavior.
2. `info`: Logs general information like connections and keep-alive handling.
3. `notice`: Logs noteworthy events that are not errors.
4. `warn`: Logs warnings that do not affect functionality but may require attention.
5. `error`: Logs errors causing failures in processing requests.
6. `crit`, `alert`, `emerg`: Logs critical errors requiring immediate action.

## Steps to Enable Debug Logging

1. **Edit the NGINX Configuration File**  
   Open the NGINX configuration file and set the `error_log` directive to `debug` level:
   ```nginx
   error_log /var/log/nginx/error.log debug;
2. Enable Debug for Specific Locations (Optional)
   To limit debugging to a specific `location` block:
   ```nginx
   location /test {
    error_log /var/log/nginx/test-debug.log debug;
   }
   ```
3. Check Debug Support in NGINX
Ensure that NGINX is compiled with debug support. Run the following command:
   ```bash
   nginx -V
   nginx -t
   ```
Look for the `--with-debug` flag in the output. If it’s present, your NGINX supports debug logging.
4. Reload NGINX Configuration
After making changes, test and reload the configuration:
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  # if using docker
  docker exec -it nginx /bin/bash
  nginx -t
  docker compose -f docker-nginx.yml restart nginx
  # or
  docker exec nginx nginx -t
  docker exec nginx nginx -s reload
  ```
# Example Configuration
### Below is an example of enabling debug logging globally and for a specific location:
```nginx
# Global debug logging
error_log /var/log/nginx/error.log debug;

# Debug logging for a specific location
location /test {
    error_log /var/log/nginx/test-debug.log debug;
}
```
