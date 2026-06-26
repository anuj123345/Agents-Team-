import subprocess, os, sys

DIR = r"D:\claude projects folder\Agents Team UI"
os.chdir(DIR)

LOG = []

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=DIR)
    LOG.append(f">>> {' '.join(cmd)}")
    if r.stdout.strip(): LOG.append(r.stdout.strip())
    if r.stderr.strip(): LOG.append(r.stderr.strip())
    LOG.append(f"exit: {r.returncode}\n")
    return r.returncode

run(["git", "init"])
run(["git", "remote", "remove", "origin"])
run(["git", "remote", "add", "origin", "https://github.com/anuj123345/Agents-Team-.git"])
run(["git", "branch", "-M", "main"])
run(["git", "add", "."])
run(["git", "commit", "-m", "Agent Teams UI - chat, PDF export, refinement, proxy server"])
code = run(["git", "push", "-u", "origin", "main", "--force"])

LOG.append("SUCCESS" if code == 0 else "PUSH FAILED")

with open(DIR + r"\git_result.txt", "w") as f:
    f.write("\n".join(LOG))
