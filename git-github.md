# git commands
```
>> git clone
>> git pull
>> git status
>> git diff
>> git add
>> git commit
>> git push
>> git stash
>> git log --oneline

>> git branch
>> git checkout branch_name (change to different local branch)
>> git checkout -b branch_name (create new branch from current branch and checkout)
>> git checkout --track origin/branch_name
>> git checkout --track upstream/branch_name
>> git branch -d branch_name (delete local branch)

>> git fetch origin 
>> git merge origin/branch_name
>> git fetch upstream 
>> git merge upstream/branch_name

>> git cherry-pick <commitid>
```

- Release tags: named reference to a specific commit in the project's history

- Git hooks: scripts that run automatically at specific points during the Git workflow, such as when you commit, push, or pull changes from a repository
    - client-side hooks, server-side hooks
    - https://git-scm.com/docs/githooks

- GitHub Actions: makes it easy to automate software development workflows with world-class CI/CD
    - https://learn.microsoft.com/en-us/collections/n5p4a5z7keznp5
    - Workflow triggers are events that initiate a GitHub Actions workflow. They can be scheduled, triggered by code changes, or manually initiated. This allows for automation of tasks based on specific conditions
    - Workflow runners are the environments where GitHub Actions workflows are executed
    - Workflow context in GitHub Actions refers to the environment and variables that are available to a workflow. It includes information about the workflow's execution, such as the event that triggered it, the repository, and the workflow itself
    - secrets and environment variables
    - Caching dependencies to speed up workflows
    - GitHub provides a feature for storing artifacts, which allows you to upload build outputs or other files as part of your workflow
    - Marketplace actions: These actions are created by the GitHub community and can be easily added to your workflow to enhance productivity and efficiency

- GitHub webhooks: allow developers to receive real-time notifications about events happening within their repository, such as commits, pull requests, and issues
    - These webhooks enable users to automate tasks, integrate with other services (ex: slack notifications), and build custom workflows

- GitHub Pages: host and publish web content directly from GitHub repositories. It provides a simple way to create and deploy websites, blogs, or projects without the need for manual configuration or maintenance
    - deploying static websites
    - custom domains
