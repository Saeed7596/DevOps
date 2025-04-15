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

Happy Git-ing! 🚀
