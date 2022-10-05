#####################
## IMPORTS
#####################
import sys
import os
import git
from pathlib import Path
from utils.progress_printer import MyProgressPrinter
from utils import print_help

#####################
## GLOBALS
#####################
work_dir = os.path.expanduser("~") + "/xwiki/backports"
projects = {
    "commons": "git@github.com:xwiki/xwiki-commons.git",
    "rendering": "git@github.com:xwiki/xwiki-rendering.git",
    "platform": "git@github.com:xwiki/xwiki-platform.git",
    "enterprise": "git@github.com:xwiki/xwiki-enterprise.git",
}


def rmdir(directory):
    """Delete folders recursively."""
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


#####################
## GET ACTIVE REPOSITORY
#####################
def get_active_repository():
    path = os.getcwd()
    while not os.path.exists(path + "/.git") and path != "/":
        path = os.path.dirname(path)
    if path == "/":
        print("[Error] There is not git repository in the current directory.")
        sys.exit(1)
    return git.Repo(path)


#####################
## GET ACTIVE PROJECT
#####################
def get_active_project(active_repo):
    project_url = active_repo.git().config("--get", "remote.origin.url")
    for project in projects:
        if projects[project] == project_url:
            return project
    print("[Error] The current working directory is not a valid project.")
    sys.exit(1)


#####################
## CONTROLLER
#####################
project_name = None
branch_name = None
commit_id = None
if len(sys.argv) == 2:
    branch_name = sys.argv[1]
    active_repo = get_active_repository()
    project_name = get_active_project(active_repo)
    commit_id = active_repo.head.ref.commit.hexsha
    print(
        f"* The script is going to cherry-pick the commit {commit_id} from the project {project_name} to the branch {branch_name}."
    )
elif len(sys.argv) == 4:
    project_name = sys.argv[1]
    branch_name = sys.argv[2]
    commit_id = sys.argv[3]
    if project_name not in projects.keys():
        print(
            f"[Error] The project {project_name} is not defined. Possible values are {', '.join(projects.keys())}"
        )
else:
    print("[Error] Missing arguments.")
    print_help()
    sys.exit(1)

##
## First, create the working directory if it does not exist yet.
## Note: we do not use the directory used by the user because if an IDE is open and we checkout a branch, the IDE
## reloads all its indices which is a loud process.
##
project_directory = work_dir + "/" + project_name
Path(project_directory).mkdir(parents=True, exist_ok=True)
##
## Init the repository if it is not already
##
if not os.path.exists(project_directory + "/.git"):
    print(f"* Clone the repository from {projects[project_name]}")
    print("Please wait, it could take some time.")
    ## Clone
    repo = git.Repo.clone_from(
        projects[project_name], project_directory, progress=MyProgressPrinter()
    )
else:
    repo = git.Repo(project_directory)
##
## The work dir needs to be clean
##
if repo.is_dirty():
    print("* Verify the workign directory is clean")
    print(f"[Error] The working directory {project_directory} must be clean.")
    sys.exit(1)
##
## Fetch the data
##
print("* Fetch the last commits")
print("Plaise wait, it could take some time.")
remote = repo.remote()
remote.fetch(progress=MyProgressPrinter())
##
## Verify there is a branch
##
if branch_name not in repo.branches:
    print(f"* Create the branch branch_name locally")
    repo.git().checkout("origin/" + branch_name)
    repo.git().checkout("-b", branch_name)
##
## Switch to this branch
##
if repo.active_branch != branch_name:
    print(f"* Checkout the branch {branch_name}")
    repo.branches[branch_name].checkout()
##
## Pull the last changes
##
print(f"* Pull the last changes on the branch {branch_name}")
repo.git().pull("--rebase", "origin", branch_name)
##
## Perform the cherry-pick
##
print(f"* Perform the cherry-pick of commit {commit_id}")
try:
    repo.git.cherry_pick("-x", commit_id)
except git.exc.GitCommandError as e:
    print(f"[Error] {e.stderr}")
    sys.exit(1)
print("Commit cherry-picked:")
print("-" * 60)
print(repo.active_branch.commit.message)
print("-" * 60)
##
## Push the new commit
##
push = input("Do you want to push? (y/n) ").lower()
if push == "y":
    print(f"* Push the commit to {projects[project_name]}")
    ## It seems remote.push() pushes everything, but we only want to push the branch
    repo.git().push("origin", branch_name)
    print("Done.")
else:
    print("Exit.")
