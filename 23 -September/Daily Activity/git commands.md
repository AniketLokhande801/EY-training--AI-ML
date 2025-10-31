1. Setting Up Git
Before using Git, configure your identity:
Shell
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
 ```
  
2. Creating a Repository
Local Repository
To create a new Git repository locally:
Shell
```bash
git init
 ```
This initializes a new Git repository in the current directory.

3.Clone an Existing Repository
To clone a remote repository:
Shell
```bash
git clone https://github.com/username/repo-name.git
 ```


4. Staging and Committing Changes
Add Files to Staging Area
Shell
git add filename
To add all files:
Shell
```bash
git add .
 ```
Commit Changes
Shell
```bash
git commit -m "Your commit message"
 ```

5. Working with Remote Repositories
Add Remote Repository
Shell
```bash
git remote add origin https://github.com/username/repo-name.git
 ```
Push Changes to Remote
Shell
```bash
git push origin main
```
Replace main with your branch name if different.
Pull Changes from Remote
Shell
```bash
git pull origin main
```
This fetches and merges changes from the remote repository.
Fetch Changes Without Merging
Shell
```bash
git fetch origin
```
This downloads changes but doesn’t merge them into your local branch.

  
6. Branching and Merging
Create a New Branch
Shell
```bash
git branch new-branch-name
```
Switch to a Branch
Shell
```bash
git checkout new-branch-name
```
Merge a Branch
Shell
```bash
git checkout main
git merge new-branch-name
```

  
7. Viewing History and Status
Check Status
Shell
```bash
git status
View Commit History
```
