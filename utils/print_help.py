#####################
## HELP
#####################
def print_help():
  print("""[Usage] xwiki-cherry-pick [project] branch [commit].
Where: 
* project is the name of the project (e.g. platform). If not specified, the script will try to guess from the repository
of the current folder. If specified, the commit id must be specified too.
* branch is the name of the branch on which the cherry-pick should be done (e.g. stable-7.2.x)
* commit is the id of the commit (e.g. 363229743aa5a209e6e4c34ffa4a241b1ddc5a24). If not specified, the script will take
# the last commit of the repository of the current folder. If specified, the project must be specified too.""")