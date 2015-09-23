xwiki-cherry-pick
=================

Description
-----
Utility to help you to cherry-pick a commit to the desired branch.

Why?
-----
In XWiki, I often need to cherry-pick a commit from the master branch to a stable branch. To avoid having my IDE updating its indices during the operation (which happens if it detects changes on the file system), I am used to do it in an other working directory. The process is the following:

1. clone the repository in a new directory if it is not already done
1. checkout the branch from the remote repository
1. fetch all the last commits from every branches
1. pull the last commits from the remote branch
1. cherry-pick the desired commit
1. push to the correct remote branch

From time to time, I do some mistakes during this process. So to avoid this problem, and to make the cherry-pick operations easier to do, I have created this script.

Finally, if you had to remember one thing only, it allows you to backport a commit to any branch without touching anything on your current working directory.

Configuration
-----
You should edit `xwiki-cherry-pick.py` and look in the "Globals" section. Here, you can define `workdir` which is the place where this script clones the repostories and does its job. By default, the value is `~/xwiki/backports`. You should keep the directory and not remove it to make future cherry-picks quicker.

Installation
-----
You need Python 2 and the module GitPython:

```
sudo pip install GitPython
```

Put this script anywhere you want, then I suggest you to add an alias in `~/.bash_aliases`, like this:

```
alias xwiki-cherry-pick='python /home/gdelhumeau/dev/xwiki-cherry-pick/xwiki-cherry-pick.py'
```

So then you just have to tip `xwiki-cherry-pick` to be able to use it.

Usage
-----
`xwiki-cherry-pick [project] branch [commit]`

Where:

* `project` is the name of the project (e.g. `platform`). If not specified, the script will try to guess from the repository
of the current folder. If specified, the commit id must be specified too.
* `branch` is the name of the branch on which the cherry-pick should be done (e.g. `stable-7.2.x`).
* `commit` is the id of the commit (e.g. `363229743aa5a209e6e4c34ffa4a241b1ddc5a24`). If not specified, the script will take
the last commit of the repository of the current folder. If specified, the project must be specified too.

Note: you need to push the commit to the remote repository (if it is not already there) before processing.

ToDo
-----
Update this script for Python 3.

