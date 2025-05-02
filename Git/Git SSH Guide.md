# Git SSH Guide

This document covers SSH file structure, cloning repositories via SSH, Git configuration levels (with file paths), and how to push to GitLab and GitHub simultaneously.

---

## .ssh Directory Files Explained

| File              | Description                                                                                             |
| :---------------- | :------------------------------------------------------------------------------------------------------ |
| `id_rsa`          | Your private SSH key. Keep it secret and never share it.                                                |
| `id_rsa.pub`      | Your public SSH key. You can share this with servers like GitHub and GitLab.                            |
| `known_hosts`     | A list of trusted servers. When you connect to a server via SSH, its identity is saved here.            |
| `config`          | Custom SSH configuration file. You can define hosts, usernames, and keys for easier access.             |
| `authorized_keys` | A list of public keys authorized to connect to the server. Used on the server side to grant SSH access. |

All these files are located inside the `~/.ssh/` directory.

---

## Cloning a Project via SSH

### 1. Generate SSH Keys (if you don't have one)

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Keys will be created inside `~/.ssh/`.

### 2. Add Public Key to GitLab and GitHub

* Copy your public key:

```bash
cat ~/.ssh/id_rsa.pub
```

* Add it in:

  * **GitHub**: Settings → SSH and GPG keys → New SSH key
  * **GitLab**: Preferences → SSH Keys → Add key

### 3. Clone the Repository

* GitHub:

```bash
git clone git@github.com:your-username/your-repo.git
```

* GitLab:

```bash
git clone git@gitlab.com:your-username/your-repo.git
```

---

## Git Configuration Levels

| Level  | Scope                                        | Config File Location             | Command Example                                    |
| :----- | :------------------------------------------- | :------------------------------- | :------------------------------------------------- |
| System | Applies to every user and repo on the system | `/etc/gitconfig`                 | `git config --system user.name "Your Name"`        |
| Global | Applies to your user account                 | `~/.gitconfig`                   | `git config --global user.email "you@example.com"` |
| Local  | Applies only to the current repository       | `.git/config` inside repo folder | `git config --local core.editor nano`              |

Local overrides Global, and Global overrides System.

---

## Push to GitLab and GitHub Simultaneously

### 1. Add Both Remotes

```bash
git remote add github git@github.com:your-username/your-repo.git
git remote add gitlab git@gitlab.com:your-username/your-repo.git
```

Alternatively, you can set multiple URLs for the `origin` remote:

```bash
git remote set-url --add origin git@github.com:your-username/your-repo.git
git remote set-url --add origin git@gitlab.com:your-username/your-repo.git
```

### 2. Push to Both Repositories

```bash
git push origin main
```

This will push to both GitHub and GitLab at the same time.

> **Tip:** Ensure you have write access to both repositories!

---

**Now you're fully set to manage projects over SSH with Git like a pro! 🚀**
