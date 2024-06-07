import re
from datetime import datetime
from git import Repo
from .application import SemanticVersion

MAIN_BRANCH_REGEX = r"^master$|^main$"
FEATURE_BRANCH_REGEX = r"^feature[/-][a-z]{2,}[a-zA-Z0-9._-]+$"
PR_BRANCH_REGEX = r"^(pull|pull\-requests|pr)[/-]"

MAJOR_REGEX = r"\+(breaking|major)\b"
MINOR_REGEX = r"\+(feature|minor)\b"
PATCH_REGEX = r"\+(fix|patch|docs|ci)\b"
SKIP_REGEX = r"\+(none|skip)\b"

SEMVER_TAG_REGEX = r"[vV]?([\d]+.[\d]+.[\d]+)"

branch_name = "feature/init-repo"
is_feature_branch = re.search(FEATURE_BRANCH_REGEX, branch_name)

def get_semver(path) -> SemanticVersion:
    repo = Repo(path)

    commits_to_read = []
    latest_semver_tag = None

    for cmt in repo.iter_commits():
        cur_cmt = {
            "ref": cmt.hexsha,
            "dt": cmt.committed_datetime,
            "msg": cmt.message,
            "tags": [tag.name for tag in repo.tags if tag.commit.hexsha == cmt.hexsha]
        }
        
        commits_to_read.append(cur_cmt)
        if len(cur_cmt["tags"]) > 0:
            latest_semver_tag = next((re.search(SEMVER_TAG_REGEX, tag).group(1) for tag in cur_cmt["tags"] if re.search(SEMVER_TAG_REGEX, tag)), None)
            if not latest_semver_tag:
                continue
            commits_to_read.remove(cur_cmt)
            print(f"Most recent git tag: {latest_semver_tag}")
            break
  
    semver = None
    if latest_semver_tag:
        splitted = latest_semver_tag.split(".")
        semver = SemanticVersion(major=splitted[0], minor=splitted[1], patch=splitted[2])
    else:
        semver = SemanticVersion()

    print(f"Number of commits to read: {len(commits_to_read)}")
    if len(commits_to_read) == 0:
        return semver
    
    commits_to_read.sort(key=lambda cmt: cmt["dt"])
    for cmt in commits_to_read:
        print(f"Current version: {semver}")
        print(f"Current commit message: '{cmt['msg']}'")

        if re.search(MAJOR_REGEX, cmt["msg"]):
            print(f"Bumping major version")
            semver.bump_major()
        elif re.search(MINOR_REGEX, cmt["msg"]):
            print(f"Bumping minor version")
            semver.bump_minor()
        elif re.search(PATCH_REGEX, cmt["msg"]):
            print(f"Bumping patch version")
            semver.bump_patch()
        else:
            print(f"Bumping commits version")
            semver.bump_commits()

    return semver
