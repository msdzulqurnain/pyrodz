import sys
import json
import subprocess
import re
from urllib.request import Request, urlopen
from urllib.error import URLError

from framework.console.style import Style

GIT_REPO_URL = "https://github.com/msdzulqurnain/pyrodz.git"
API_LATEST = "https://api.github.com/repos/msdzulqurnain/pyrodz/releases/latest"
RELEASES_URL = "https://github.com/msdzulqurnain/pyrodz/releases/tag"


class Update:
    def handle(self, *args):
        check_only = "--check" in args
        local_version = Style.FRAMEWORK_VERSION

        print()

        remote_info = self._check_via_github_api()

        if remote_info:
            latest_tag = remote_info["tag_name"]
            remote_ver = latest_tag.lstrip("v")
        else:
            print(Style.warn("Could not reach GitHub API"))
            print(Style.muted("  Falling back to git fetch..."))
            print()

            if not self._git_available():
                print(Style.error("Git is not available"))
                print()
                return

            if not self._is_git_repo():
                print(Style.error("Not a git repository"))
                print(Style.muted(f"  Re-clone: git clone {GIT_REPO_URL}"))
                print()
                return

            latest_tag = self._get_latest_tag_via_git()

            if not latest_tag:
                print(Style.error("Could not retrieve latest version"))
                print()
                return

            remote_ver = latest_tag.lstrip("v")

        needs_update = self._compare_versions(local_version, remote_ver)

        print(f"  Current:  {Style.text('v' + local_version, Style.CYAN, Style.BOLD)}")
        print(f"  Latest:   {Style.text(latest_tag, Style.GREEN, Style.BOLD)}")
        print()

        if not needs_update:
            print(Style.success("Already up to date!"))
            print()
            return

        if check_only:
            print(Style.info(f"Update available: v{local_version} → {latest_tag}"))
            print(Style.muted("  Run 'pyrodz update' to update"))
            print()
            return

        self._perform_update(latest_tag)

    def _check_via_github_api(self):
        try:
            req = Request(API_LATEST, headers={"User-Agent": "PyroDZ/1.0"})
            with urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                return {
                    "tag_name": data["tag_name"],
                    "body": data.get("body", ""),
                    "html_url": data.get("html_url", ""),
                }
        except (URLError, json.JSONDecodeError, KeyError):
            return None

    def _git_available(self):
        try:
            subprocess.run(
                ["git", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _is_git_repo(self):
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.SubprocessError:
            return False

    def _git_status_porcelain(self):
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def _get_latest_tag_via_git(self):
        try:
            subprocess.run(
                ["git", "fetch", "--tags", "--quiet", GIT_REPO_URL],
                capture_output=True,
                check=True,
            )

            result = subprocess.run(
                ["git", "tag", "-l", "--sort=-version:refname"],
                capture_output=True,
                text=True,
                check=True,
            )

            tags = [
                t.strip()
                for t in result.stdout.strip().split("\n")
                if t.strip()
            ]

            if not tags:
                return None

            def tag_key(tag):
                ver = tag.lstrip("v")
                parts = re.split(r"[.-]", ver)
                key = []
                for part in parts:
                    if part.isdigit():
                        key.append((0, int(part)))
                    elif part in ("beta", "alpha", "rc"):
                        key.append((1, part))
                    else:
                        key.append((2, part))
                return tuple(key)

            return max(tags, key=tag_key)

        except subprocess.SubprocessError:
            return None

    def _compare_versions(self, local, remote):
        local_parts = [p for p in re.split(r"[.-]", local) if p]
        remote_parts = [p for p in re.split(r"[.-]", remote) if p]

        for i in range(max(len(local_parts), len(remote_parts))):
            l = local_parts[i] if i < len(local_parts) else "0"
            r = remote_parts[i] if i < len(remote_parts) else "0"

            if l.isdigit() and r.isdigit():
                if int(l) < int(r):
                    return True
                elif int(l) > int(r):
                    return False
            else:
                if l != r:
                    if l.isdigit():
                        return False
                    if r.isdigit():
                        return True
                    return l < r

        return False

    def _perform_update(self, latest_tag):
        if not self._is_git_repo():
            print(Style.error("Not a git repository"))
            print(Style.muted(f"  Re-clone: git clone {GIT_REPO_URL}"))
            print()
            return

        has_stash = False
        porcelain = self._git_status_porcelain()

        if porcelain:
            print(Style.warn("Uncommitted changes detected — stashing..."))
            subprocess.run(["git", "stash", "push", "-m", "pyrodz-update-auto-stash"], capture_output=True, check=True)
            has_stash = True

        print(Style.muted("  Fetching latest framework code..."))

        try:
            subprocess.run(
                ["git", "fetch", "--tags", "--quiet", GIT_REPO_URL, "master"],
                capture_output=True,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(Style.error(f"  Fetch failed: {e.stderr.strip() or 'unknown error'}"))
            if has_stash:
                subprocess.run(["git", "stash", "pop"], capture_output=True)
            print()
            return

        print(Style.muted("  Updating framework/ folder..."))

        result = subprocess.run(
            ["git", "checkout", "FETCH_HEAD", "--", "framework/"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(Style.error(f"  Update failed: {result.stderr.strip()}"))
            if has_stash:
                subprocess.run(["git", "stash", "pop"], capture_output=True)
            print()
            return

        print(Style.success(f"  Updated to {latest_tag}"))
        print()

        if has_stash:
            stash_pop = subprocess.run(
                ["git", "stash", "pop"],
                capture_output=True,
                text=True,
            )

            if stash_pop.returncode != 0:
                print(Style.warn("  Could not auto-restore stashed changes"))
                print(Style.muted("  Run: git stash pop"))
                print()
            else:
                print(Style.success("  Stashed changes restored"))
                print()

        print(Style.info("Updating dependencies..."))

        try:
            result = subprocess.run(
                [
                    sys.executable, "-m", "pip", "install",
                    "-r", "requirements.txt", "--quiet",
                ],
                capture_output=True,
                check=True,
            )
            print(Style.success("  Dependencies updated"))
        except subprocess.CalledProcessError:
            print(Style.warn("  Could not auto-update dependencies"))
            print(Style.muted("  Run: pip install -r requirements.txt"))

        print()

        print(Style.info("Running pending migrations..."))

        try:
            from framework.console.commands.migrate import Migrate
            Migrate().handle()
        except Exception:
            print(Style.warn("  Could not auto-run migrations"))
            print(Style.muted("  Run: pyrodz migrate"))

        print()
        print(Style.success("Update complete!"))
        print()

        self._show_changelog(latest_tag)

    def _show_changelog(self, latest_tag):
        print(Style.info("What's new:"))
        print()

        try:
            result = subprocess.run(
                [
                    "git", "log", "--oneline", "--no-decorate",
                    "FETCH_HEAD", "--not", "HEAD",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            if result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    print(f"    {Style.text(line, Style.GRAY)}")
            else:
                print(f"    {Style.muted(f'See: {RELEASES_URL}/{latest_tag}')}")

            print()
        except subprocess.SubprocessError:
            print(f"    {Style.muted(f'See: {RELEASES_URL}/{latest_tag}')}")
            print()
