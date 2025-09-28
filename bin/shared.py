import functools


class VersionMutator:
    def __init__(self, name, branch_starts, zeroables):
        self.name = name
        self.branch_starts = branch_starts
        self.zeroables = zeroables

    def is_allowed_branch(self, branch):
        return branch.startswith(tuple(self.branch_starts))

    def __call__(self, version):
        version[self.name] = version[self.name] + 1
        for zeroable in self.zeroables:
            version[zeroable] = 0


minorVersionMutator = VersionMutator("minor", ["master"], ["fix", "build"])
fixVersionMutator = VersionMutator("fix", ["release", "master"], ["build"])
buildVersionMutator = VersionMutator("build", ["release", "master"], [])
errorVersionMutator = VersionMutator("error", [], [])


class SemanticPrefixUnknown(RuntimeError):
    pass


MutatorSeverities = {
    "error": 0,
    "minor": 1,
    "fix": 2,
    "build": 3,
}


@functools.total_ordering
class SemanticPrefix:
    def __init__(self, name, description, mutator):
        self.name = name
        self.description = description
        self.mutator = mutator

    def validate_commit_message(self, message):
        if message.startswith("{}:".format(self.name)):
            return
        raise SemanticPrefixUnknown()

    def __eq__(self, other):
        return self.mutator.name == self.mutator.name

    def __lt__(self, other):
        return (
            MutatorSeverities[other.mutator.name] < MutatorSeverities[self.mutator.name]
        )

    def __str__(self):
        return "{:<9} {}".format("{}:".format(self.name), self.description)


semanticPrefixes = [
    SemanticPrefix("feat", "A new feature a user will see", minorVersionMutator),
    SemanticPrefix("fix", "A bug fix a user will see", fixVersionMutator),
    SemanticPrefix("docs", "A change to project documentation", buildVersionMutator),
    SemanticPrefix("style", "A code styling change", fixVersionMutator),
    SemanticPrefix("refactor", "Restructuring of the code", fixVersionMutator),
    SemanticPrefix("test", "Addition to codebase testing", buildVersionMutator),
    SemanticPrefix("chore", "Updating grunt tasks", buildVersionMutator),
    SemanticPrefix("wip", "Will error if put in a release", errorVersionMutator),
]
