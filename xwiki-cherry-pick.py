#####################
## IMPORTS
#####################
import sys
import os
import git
#####################
## GLOBALS
#####################
home       = os.path.expanduser("~")
sources    = home    + "/xwiki"
work_dir   = sources + "/backports"
projects   = {
  'commons'    : 'git@github.com:xwiki/xwiki-commons.git',
  'rendering'  : 'git@github.com:xwiki/xwiki-rendering.git',
  'platform'   : 'git@github.com:xwiki/xwiki-platform.git',
  'enterprise' : 'git@github.com:xwiki/xwiki-enterprise.git'
}
#####################
## HELP
#####################
def print_help():
  print """[Usage] xwiki-cherry-pick project branch commit.
Where: 
* project is the name of the project (e.g. platform)
* branch is the name of the branch on which the cherry-pick should be done (e.g. stable-7.2.x)
* commit is the id of the commit (e.g. 363229743aa5a209e6e4c34ffa4a241b1ddc5a24)"""
#####################
## ASSERTS
#####################
if len(sys.argv) < 4:
  print "[Error] Missing arguments."
  print_help()
  sys.exit(1)
if sys.argv[1] not in projects.keys():
  print "[Error] The project [%s] is not defined. Possible values are [%s]" % (sys.argv[1], ', '.join(projects.keys()))
#####################
## CONTROLLER
#####################
project_name = sys.argv[1]
branch_name  = sys.argv[2]
commit_id    = sys.argv[3]
#####################
## REMOTE PROGRESS
#####################
class MyProgressPrinter(git.RemoteProgress):
  def update(self, op_code, cur_count, max_count=None, message=''):
    if op_code == git.RemoteProgress.COMPRESSING and self.phase != op_code:
      print "Compressing..."
    elif op_code == git.RemoteProgress.COUNTING and self.phase != op_code:
      print "Counting..."
    elif op_code == git.RemoteProgress.RECEIVING:
      sys.stdout.write("Receiving %d/%d (%d%s)%s\r" % (cur_count, max_count, int(cur_count / max_count * 100.0), '%', message))
      sys.stdout.flush()
    elif op_code == git.RemoteProgress.RESOLVING:
      sys.stdout.write("\n")
      print "Resolving..."
    self.phase = op_code
##
## First, create the working directory if it does not exist yet.
## Note: we do not use the directory used by the user because if an IDE is open and we checkout a branch, the IDE 
## reloads all its indices which is a loud process.
##
if not os.path.exists(work_dir):
  print "* Create the working directory"
  os.makedirs(work_dir)
##
## Same with the project directory
##
project_directory = work_dir + "/" + project_name
if not os.path.exists(project_directory):
  print "* Create the git working directory"
  os.makedirs(project_directory)
##
## Init the repository if it is not already
##
if not os.path.exists(project_directory + "/.git"):
  print "* Clone the repository from [%s]" % projects[project_name]
  print "Please wait, it could take some time."
  ## Clone
  repo = git.Repo.clone_from(projects[project_name], project_directory, progress=MyProgressPrinter())
else:
  repo = git.Repo(project_directory)
##
## The work dir needs to be clean
##
if repo.is_dirty():
  print "* Verify the workign directory is clean"
  print "[Error] The working directory [%s] must be clean." % project_directory
  sys.exit(1)
##
## Fetch the data
##
print "* Fetch the last commits"
print "Plaise wait, it could take some time."
remote = repo.remote()
remote.fetch(progress=MyProgressPrinter())
##
## Verify there is a branch
##
if branch_name not in repo.branches:
  print "* Create the branch [%s]" % branch_name
  repo.create_head(branch_name, remote.refs[branch_name]).set_tracking_branch(remote.refs[branch_name])
##
## Switch to this branch
##
if repo.active_branch != branch_name:
  print "* Checkout the branch [%s]" % branch_name
  repo.branches[branch_name].checkout()
##
## Pull the last changes
##
print "* Pull the last changes on the branch [%s]" % branch_name
remote.pull(progress=MyProgressPrinter())
##
## Perform the cherry-pick
##
print "* Perform the cherry-pick of commit [%s]" % commit_id
try:
  repo.git.cherry_pick('-x', commit_id)
except git.exc.GitCommandError as e:
  print "[Error] %s" % e.stderr
  sys.exit(1)
print "Commit cherry-picked:"
print "-"*60
print repo.active_branch.commit.message
print "-"*60
##
## Push the new commit
##  
print "* Push the commit to [%s]" % projects[project_name]
#remote.push()
print "Done."
