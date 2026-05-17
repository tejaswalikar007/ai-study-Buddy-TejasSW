import os
import shutil
import subprocess
import sys

def run_cmd(cmd, desc):
    print(f"🔄 {desc}...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Failed: {res.stderr.strip()}")
        return False, res.stdout, res.stderr
    print(f"✅ Success!")
    if res.stdout.strip():
        print(res.stdout.strip())
    return True, res.stdout, res.stderr

def main():
    workspace = os.path.abspath(os.path.dirname(__file__))
    os.chdir(workspace)
    print(f"📁 Workspace directory: {workspace}\n")

    # 1. Clean up stray Git files in root if they exist (HEAD, config, description, index)
    # These should live in a .git folder, not directly in the root directory.
    stray_files = ["HEAD", "config", "description", "index"]
    for file in stray_files:
        path = os.path.join(workspace, file)
        # Check if they are files (not directories like config.py)
        if os.path.exists(path) and os.path.isfile(path) and not file.endswith(".py"):
            try:
                os.remove(path)
                print(f"🧹 Removed stray file from root: {file}")
            except Exception as e:
                print(f"⚠️ Could not remove stray file {file}: {e}")

    # 2. Check if git is installed
    ok, _, _ = run_cmd("git --version", "Checking if Git is installed")
    if not ok:
        print("❌ Error: Git is not installed or not in your system PATH.")
        sys.exit(1)

    # 3. Initialize git if not already a repository
    git_dir = os.path.join(workspace, ".git")
    if not os.path.exists(git_dir):
        ok, _, _ = run_cmd("git init", "Initializing a clean Git repository")
        if not ok:
            sys.exit(1)
    else:
        print("ℹ️ Git repository already initialized.")

    # 4. Check .gitignore
    gitignore_path = os.path.join(workspace, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            content = f.read()
        if ".env" not in content:
            print("⚠️ Warning: .env is not in .gitignore. Updating it...")
            with open(gitignore_path, 'a') as f:
                f.write("\n.env\n")
    else:
        print("📝 Creating new .gitignore...")
        with open(gitignore_path, 'w') as f:
            f.write(".venv/\n__pycache__/\n.env\n*.pyc\n*.zip\n")

    # 5. Double-check that .env is NOT tracked
    run_cmd("git rm --cached .env", "Ensuring .env is not tracked in index (if previously added)")

    # 6. Add all files
    ok, _, _ = run_cmd("git add .", "Staging all files (respecting .gitignore)")
    if not ok:
        sys.exit(1)

    # 7. Check status to ensure .env is NOT listed under Changes to be committed
    ok, stdout, _ = run_cmd("git status", "Verifying staged files")
    if ".env" in stdout:
        print("🚨 CRITICAL WARNING: .env is still detected in staged files! Aborting push.")
        sys.exit(1)

    # 8. Configure Remote
    remote_url = "https://github.com/tejaswalikar007/ai-study-Buddy-TejasSW.git"
    # Check existing remote
    res_remote = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    stdout = res_remote.stdout
    if "origin" in stdout:
        run_cmd(f"git remote set-url origin {remote_url}", "Updating git remote URL to target repository")
    else:
        run_cmd(f"git remote add origin {remote_url}", "Adding git remote origin pointing to target repository")

    # 9. Create a commit
    ok, _, _ = run_cmd('git commit -m "Configure modern Gemini models and update git ignore rules"', "Creating commit")
    # Note: If no changes, commit might fail but we can still try to push

    # 10. Ensure we are on 'main' branch
    run_cmd("git branch -M main", "Setting default branch name to 'main'")

    # 11. Push changes
    print("\n🚀 Pushing changes to GitHub...")
    print("⚠️  Note: If this is the first push, Windows Git Credential Manager may prompt you to authenticate in a popup window.")
    
    # Run interactive push so user can see prompt / complete auth
    res = subprocess.run("git push -u origin main", shell=True)
    if res.returncode == 0:
        print("\n🎉 SUCCESSFULLY PUSHED CODE TO GITHUB!")
        print("Repository: https://github.com/tejaswalikar007/ai-study-Buddy-TejasSW")
    else:
        print("\n❌ Failed to push. If you got authentication errors, please verify you have access permissions to this repository.")

if __name__ == "__main__":
    main()
