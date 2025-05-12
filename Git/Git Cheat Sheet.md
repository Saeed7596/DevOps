# 🧠 Git Cheat Sheet

## 🛠️ Initial Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor vim
git config --list
```

---

## 📁 Starting a Repository

```bash
git init                     # Initialize a new local repo
git clone <url>             # Clone a remote repo
git status                  # Show status of changes
git add <file>              # Stage specific file
git add .                   # Stage all changes
git commit -m "message"     # Commit with message
git commit -am "message"    # Add and commit tracked files
```

---

## 🔄 Remote Repositories

```bash
git remote -v                            # Show remotes
git remote add origin <url>             # Add new remote
git push -u origin main                 # Push main branch
git push                                # Push changes
git pull                                # Pull and merge changes
```

---

## 🌿 Branching & Merging

```bash
git branch                              # List branches
git branch <name>                       # Create branch
git checkout <name>                     # Switch branch
git checkout -b <name>                  # Create and switch
git merge <branch>                      # Merge into current branch
git branch -d <name>                    # Delete local branch
git push origin --delete <branch>      # Delete remote branch
```

---

## 🔍 Viewing Changes

```bash
git log                                 # View commit history
git log --oneline --graph               # Compact graph view
git diff                                # View unstaged changes
git show <commit>                       # Show commit details
```

---

## ⏪ Undoing & Resetting

```bash
git checkout <commit>                   # Temporarily checkout
git reset --hard <commit>               # Reset to commit (⚠️ destructive)
git revert <commit>                     # Revert a specific commit
```

---

## 🧼 Cleanup & Debugging

```bash
git stash                               # Save temporary changes
git stash pop                           # Reapply stashed changes
git clean -fd                           # Remove untracked files
git cherry-pick <commit>                # Apply specific commit
```

---

## 🔖 Tagging

```bash
git tag                                 # List tags
git tag v1.0                            # Create lightweight tag
git tag -a v1.0 -m "Message"            # Annotated tag
git push origin v1.0                    # Push tag to remote
```

---

## ✅ Useful Tips

- Use `.gitignore` to avoid tracking unwanted files.
- Use `git log --graph --all --decorate` to visualize history.
- Use `git blame <file>` to track who last changed each line.

---

## Git Bisect
### What is `git bisect`?
`git bisect` helps you find the commit that introduced a bug by performing a binary search between known good and bad commits.
### How to use `git bisect`
```bash
git bisect start
git bisect bad        # mark the current commit as bad
git bisect good <commit-hash>  # mark a known good commit
```
Then follow the testing prompts (`good`/`bad`) until the problematic commit is found.

Finally, reset:
```bash
git bisect reset
```
Example Workflow:
```bash
git bisect start
git bisect bad
git bisect good a1b2c3d4
git bisect bad
git bisect good
git bisect bad
git bisect reset
```

---

## GPG --gen-key
### What is `gpg --gen-key`?
The `gpg --gen-key` command generates a new GPG key pair for encrypting, signing, and verifying files and commits.
### How to generate a GPG key
```bash
gpg --full-generate-key
```
Follow the interactive prompts to complete setup.
### List and export your GPG key
```bash
gpg --list-secret-keys --keyid-format LONG
```
```bash
gpg --list-keys
gpg --armor --export <Key-ID>
```

---

## Signing Git Commits and Tags
### Sign a Git Commit
To sign a commit manually:
```bash
git commit -S -m "Your signed commit message"
```
* `-S` option tells Git to sign the commit with your GPG key.

Set your signing key in Git:
```bash
git config --global user.signingkey YOUR_KEY_ID
```
To configure Git to always sign commits:
```bash
git config --global commit.gpgSign true
```
### Sign a Git Tag
Create and sign an annotated tag:
```bash
git tag -s v1.0.0 -m "Signed version 1.0.0"
```
### Push the tag to the remote repository:
```bash
git push origin v1.0.0
```
### Verify a Signed Commit or Tag
To verify a signed commit:
```bash
git log --show-signature
```
To verify a signed tag:
```bash
git tag -v <tagname>
```

You will see the signature verification output.

### Important Notes:
- Always push your signed commits and tags (`git push` and `git push origin --tags`).
- Ensure your GPG key is not expired.
- If GitHub/GitLab does not recognize your signature, check that the correct email and key are uploaded.

---

## Git Blame
### What is `git blame`?
`git blame` shows you who last modified each line of a file and when.
This is useful for tracking changes and understanding the history behind each line.
### How to use `git blame`
```bash
git blame <filename>
```
Example:
```bash
git blame main.py
```
You can also blame a specific line range:
```bash
git blame -L 10,20 <filename>
```

---

## LICENSE File in Projects
### What is a LICENSE file?
The LICENSE file in a project defines the legal terms under which the project's source code can be used, modified, and distributed.

It informs users about:
* Their rights to use the code.
* Any limitations or requirements (e.g., attribution).
* Liability disclaimers.

### Common Open-Source Licenses
* MIT License
* Apache License 2.0
* GNU GPL v3
* BSD License

### Why should you include a LICENSE?
* To legally protect yourself and contributors.
* To inform users of their rights and responsibilities.
* To make your project open-source in a standardized way.

A project without a LICENSE file means users technically have **no right** to use, copy, modify, or distribute the code!

---

Happy Git-ing! 🚀
