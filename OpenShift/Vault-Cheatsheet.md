| Vault Command | Example Usage / Arguments |
|---------------|---------------------------|
| `vault status` | Check Vault status |
| `vault login` | `vault login <token>` — Authenticate to Vault |
| `vault server` | `vault server -config=/path/to/config.hcl` — Start Vault server with config |
| `vault secrets enable` | `vault secrets enable pki` — Enable PKI secrets engine |
| `vault secrets list` | List all enabled secrets engines |
| `vault write` | `vault write pki/root/generate/internal common_name="example.com" ttl=8760h` — Write data or create resources |
| `vault read` | `vault read pki/cert/my-cert` — Read data from Vault |
| `vault delete` | `vault delete pki/cert/my-cert` — Delete a secret or resource |
| `vault policy write` | `vault policy write my-policy /path/to/policy.hcl` — Create/update a policy |
| `vault policy list` | List all policies |
| `vault auth enable` | `vault auth enable kubernetes` — Enable authentication method |
| `vault auth list` | List all enabled authentication methods |
| `vault token create` | `vault token create -policy=my-policy -ttl=24h` — Create a new token |
| `vault token lookup` | Get information about current token |
| `vault lease revoke` | `vault lease revoke <lease_id>` — Revoke a specific lease |
| `vault operator init` | Initialize a new Vault cluster |
| `vault operator unseal` | `vault operator unseal <unseal_key>` — Unseal Vault |
| `vault operator seal` | Seal Vault manually |
| `vault operator raft join` | `vault operator raft join http://<other-node>:8200` — Join a Vault HA cluster |
| `vault operator raft list-peers` | List Raft cluster peers |
| `vault pki tidy` | `vault write pki/tidy tidy_cert_store=true tidy_revoked_certs=true` — Clean up expired certificates |
