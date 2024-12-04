#!/usr/bin/env python3

from git import Repo
from jinja2 import Template
import os
import sys
import toml
import shared
from datetime import datetime, timezone

VersionFileTemplate = """
##################################################
# DO NOT EDIT THIS FILE MANUALLY
# use the release tool by executing `make release`
# on the master branch or a release branch
##################################################

[version]
major=2
minor={{ minor }}
fix={{ fix }}
build={{ build }}
variant="alpha"
timestamp="{{ timestamp }}"

"""


def exit_with_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(1)


self_directory = os.path.dirname(os.path.abspath(__file__))


def get_filename(name):
    return os.path.join(self_directory, "..", name)


def write_notes(filename, version, commits):
    new_content = [
        "## {major}.{minor}.{fix}.{build}-{variant}".format(**version),
        datetime.now(timezone.utc).strftime("*released: %b %d, %Y %I:%M %p UTC*"),
    ]

    for commit in commits:
        tag, content = commit.message.split(":", 1)
        if tag == "release":
            break
        new_content.append("- {} *({})*".format(content.strip(), tag))
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write("\n".join(new_content) + "\n\n" + content)


class VersionFile:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "r") as file:
            return toml.load(file)

    def write(self, context):
        with open(self.filename, "w") as file:
            file.write(Template(VersionFileTemplate).render(context))


TRUNK_BRANCH = "master"

known_prefixes = set(["release"] + [prefix.name for prefix in shared.semanticPrefixes])


class Release:
    def __init__(self, repo, error, version_filename, notes_filename):
        self.repo = repo
        self.error = error
        self.version_filename = version_filename
        self.notes_filename = notes_filename
        self.start_branch = self.repo.active_branch.name

    def _tag(self, version):
        self.repo.create_tag(
            "release_{major}.{minor}.{fix}.{build}-{variant}".format(**version)
        )

    def _handle_a_feat(self, version):
        push_branch = "release_{major}.{minor}".format(**version)
        self.repo.git.checkout("-b", push_branch)
        self._tag(version)
        self.repo.remote("origin").push("--set-upstream", "origin", push_branch)
        self.repo.git.checkout(TRUNK_BRANCH)

    def _handle_a_non_feat(self, version):
        self._tag(version)
        self.repo.remote("origin").push("origin", self.start_branch)

    def __call__(self):
        version_file = VersionFile(self.version_filename)
        version = version_file.read()["version"]
        if self.repo.bare:
            self.error("This should be in a repository")
        if self.repo.is_dirty():
            self.error("The repo should not be dirty")
        if self.start_branch != TRUNK_BRANCH and not self.start_branch.startswith(
            "release_"
        ):
            self.error(
                'The active branch "{}" needs to be "master" or start with "release-"'.format(
                    self.start_branch
                )
            )
        prefixes = shared.semanticPrefixes.copy()
        prefixes.sort()
        largest_prefix = None
        for prefix in prefixes:
            for commit in self.repo.iter_commits():
                if ":" not in commit.message:
                    self.error(
                        'can not find recognizable semantic prefix for commit "{}"'.format(
                            commit.message
                        )
                    )
                semantic_prefix = commit.message.split(":")[0]
                if semantic_prefix not in known_prefixes:
                    self.error('unknown semantic prefix "{}"'.format(semantic_prefix))
                if semantic_prefix == "release":
                    break
                if commit.message.startswith("wip:"):
                    self.error('"wip:" commit semantics are not allowed in a release')
                if commit.message.startswith("{}:".format(prefix.name)):
                    largest_prefix = prefix
                    break
        if not largest_prefix.mutator.is_allowed_branch(self.start_branch):
            self.error(
                'Additional features can only go on the "master" '
                + "branch while a release branch is checked out"
            )
        version["timestamp"] = datetime.now(timezone.utc).isoformat()
        largest_prefix.mutator(version)
        version_file.write(version)
        write_notes(self.notes_filename, version, self.repo.iter_commits())
        self.repo.index.add([self.version_filename, self.notes_filename])
        self.repo.index.commit(
            "release: {major}.{minor}.{fix}.{build}-alpha".format(**version)
        )
        if largest_prefix.name == "feat":
            self._handle_a_feat(version)
        else:
            self._handle_a_non_feat(version)


if __name__ == "__main__":
    Release(
        Repo(os.path.join(self_directory, "..")),
        exit_with_error,
        get_filename("version.toml"),
        get_filename("releasenotes.md"),
    )()
