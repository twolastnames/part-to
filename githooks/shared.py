class VersionMutator:
    def __init__(self, name):
        self.name = name


minorVersionMutator = VersionMutator("Minor")
fixVersionMutator = VersionMutator("Fix")
buildVersionMutator = VersionMutator("Build")
errorVersionMutator = VersionMutator("Error")


class SemanticPrefixUnknown(RuntimeError):
    pass


class SemanticPrefix:
    def __init__(self, name, description, mutator):
        self.name = name
        self.description = description
        self.mutator = mutator

    def validate_commit_message(self, message):
        if message.startswith("{}:".format(self.name)):
            return
        raise SemanticPrefixUnknown()

    def __str__(self):
        return "{:<11}: {}".format(self.name, self.description)


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
