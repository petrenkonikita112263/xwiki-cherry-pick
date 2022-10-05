import sys
import git

#####################
## REMOTE PROGRESS
#####################
class MyProgressPrinter(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        if op_code == git.RemoteProgress.COMPRESSING and self.phase != op_code:
            print("Compressing...")
        elif op_code == git.RemoteProgress.COUNTING and self.phase != op_code:
            print("Counting...")
        elif op_code == git.RemoteProgress.RECEIVING:
            sys.stdout.write(
                "Receiving %d/%d (%d%s)%s\r"
                % (
                    cur_count,
                    max_count,
                    int(cur_count / max_count * 100.0),
                    "%",
                    message,
                )
            )
            sys.stdout.flush()
        elif op_code == git.RemoteProgress.RESOLVING and self.phase != op_code:
            sys.stdout.write("\n")
            print("Resolving...")
        self.phase = op_code
