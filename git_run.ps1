Set-Location "D:\claude projects folder\Agents Team UI"
$log = @()
$log += "=== Git Push Started: $(Get-Date) ==="

# Set user identity
git config user.email "anuj.baral69@gmail.com" 2>&1 | Out-Null
git config user.name "Anuj Baral" 2>&1 | Out-Null

git init 2>&1 | ForEach-Object { $log += "init: $_" }
git remote remove origin 2>&1 | Out-Null
git remote add origin "https://github.com/anuj123345/Agents-Team-.git" 2>&1 | ForEach-Object { $log += "remote: $_" }
git branch -M main 2>&1 | ForEach-Object { $log += "branch: $_" }
git add . 2>&1 | ForEach-Object { $log += "add: $_" }
git commit -m "Agent Teams UI - chat, PDF export, refinement, proxy server" 2>&1 | ForEach-Object { $log += "commit: $_" }
$push = git push -u origin main --force 2>&1
$push | ForEach-Object { $log += "push: $_" }

$log += "=== Done: $(Get-Date) ==="
$log | Out-File "D:\claude projects folder\Agents Team UI\git_result.txt" -Encoding utf8
