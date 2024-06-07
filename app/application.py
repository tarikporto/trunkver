class SemanticVersion:
  def __init__(self, major=0, minor=0, patch=1, commits=0):
    self.major = int(major)
    self.minor = int(minor)
    self.patch = int(patch)
    self.commits = int(commits)

    print(type(self.patch))
  
  def __str__(self):
    return f"{self.major}.{self.minor}.{self.patch}-{self.commits}"

  def bump_commits(self):
    self.commits = self.commits + 1
  
  def bump_patch(self):
    self.patch = self.patch + 1
    self.commits=0

  def bump_minor(self):
    self.minor = self.minor + 1
    self.patch = 0
    self.commits = 0
  
  def bump_major(self):
    self.major = self.major + 1
    self.minor = 0
    self.patch = 0
    self.commits = 0


