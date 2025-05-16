# GitLab API Overview

GitLab provides a powerful REST API and GraphQL API to interact with your GitLab instance programmatically. You can automate tasks, query data, and integrate GitLab into your tools and workflows.

## 🔑 Authentication

Most API calls require authentication using a **Personal Access Token** or a **Job Token** (in CI/CD). Include it in your header:

```http
PRIVATE-TOKEN: <your_access_token>
```

Alternatively, you can use it as a query parameter:

```http
https://gitlab.example.com/api/v4/projects?private_token=<your_access_token>
```

## 🌐 Base URL

The base URL for the GitLab API (v4) is:

```
https://gitlab.example.com/api/v4/
```

If you're using GitLab.com:

```
https://gitlab.com/api/v4/
```

## 📘 Common Endpoints

### Get User Info

```bash
GET /user
```

### List All Projects

```bash
GET /projects
```

### Get Project Details

```bash
GET /projects/:id
```

> Use `url-encoded` project path like `group%2Fproject`.

### Trigger a Pipeline

```bash
POST /projects/:id/trigger/pipeline
```

Payload example:

```json
{
  "token": "TRIGGER_TOKEN",
  "ref": "main"
}
```

### List Project Variables

```bash
GET /projects/:id/variables
```

## 📦 API Clients

You can use `curl`, `Postman`, or libraries like:

- Python: `python-gitlab`
- Node.js: `node-gitlab`
- Go: `go-gitlab`

## 📎 Resources

- [GitLab REST API Docs](https://docs.gitlab.com/ee/api/)
- [GitLab GraphQL API Docs](https://docs.gitlab.com/ee/api/graphql/)
- [Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

---

✅ **Pro Tip:** Always use pagination (`?per_page=100&page=2`) when retrieving large lists of data.
