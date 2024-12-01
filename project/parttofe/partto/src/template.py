#!/usr/bin/env python3
from jinja2 import Template
import os
import sys
import collections
import re
import pathlib
import subprocess

self_directory = os.path.normpath(
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
).split(os.sep)


class SystemArgumentsParseError(RuntimeError):
    pass


Command = collections.namedtuple("Command", "target parts")


def get_command_from_sysargv():
    if len(sys.argv) != 2:
        print(
            "requires one argument that is a directory/file to template in",
            file=sys.stderr,
        )
        exit(1)
    target = os.path.abspath(sys.argv[1])
    parts = os.path.normpath(target).split(os.sep)
    for directory in self_directory:
        if directory != parts[0]:
            break
        parts = parts[1:]

    return Command(target=target, parts=parts)


class PathPartsValidationError(RuntimeError):
    pass


def validate_parts(parts):
    if not len(parts) > 1:
        raise PathPartsValidationError(
            "the input must be a path with at least, first, a directory to define"
            + " the temlpate to use, and second, the name. Deeper directories can be used"
            + " to be templated with in said directory.",
        )
    if parts[0] not in definitions.keys():
        raise PathPartsValidationError(
            "this tool only knows how to template in the {} directorie(s)".format(
                ", ".join(["src/{}".format(key) for key in definitions.keys()])
            )
        )


Definition = collections.namedtuple("Definitions", "filename definition")

PreTemplate = ""
PostTemplate = ""

ForTestDirectory = "tests"

ForTestFilename = "{{ name.title }}.test.tsx"

ForTestDefinition = """
import React  from 'react';
import {expect, test} from '@jest/globals';
import { render, screen } from '@testing-library/react';
import { ShellProvider } from "{{ depthDots }}providers/ShellProvider";
import { {{ name.title }} } from '../{{ name.title }}';

test('snapshot', () => {
  render(<ShellProvider><{{name.title}}/></ShellProvider>)
  const component = screen.getByTestId("{{ name.title }}")
  expect(component).toMatchSnapshot();
}); """

definitions = {
    "shared": [
        Definition(
            filename=os.path.join("..", "{{ name.camel }}.ts"),
            definition="""
export interface {{ name.title }} {

}

export function get{{ name.title }}() : {{name.title}} {

}
            """,
        ),
        Definition(
            filename=os.path.join("..", "{{ name.camel }}.test.ts"),
            definition="""
import {expect, test} from '@jest/globals';

test('snapshot', () => {
  expect(false).toBeTruthy();
}); """,
        ),
    ],
    "hooks": [
        Definition(
            filename=os.path.join("..", "{{ name.camel }}.ts"),
            definition="""
export function use{{ name.title }} () {
}
            """,
        ),
    ],
    "providers": [
        Definition(
            filename=os.path.join("..", "{{ name.title }}.tsx"),
            definition="""
import React, { createContext } from "react";
import { PropsWithChildren } from "react";

export type {{ name.title }}Type = {}

export const {{ name.title }}Context = createContext<undefined | {{ name.title}}Type>(undefined)

export function {{ name.title }}Provider ({children} : PropsWithChildren) {
    return <{{ name.title }}Context.Provider value={undefined}>
        { children }
    </{{ name.title }}Context.Provider>
}

export function use{{ name.title }}Provider() {
  return useContext({{ name.title }}Context) || ({})
}
""",
        ),
    ],
    "components": [
        Definition(
            filename="{{ name.title }}.tsx",
            definition="""
import React from "react";

import classes from "./{{ name.title }}.module.scss";
import { {{ name.title }}Props } from "./{{ name.title }}Types";

export function {{name.title}} (props: {{ name.title }}Props) {
    return <div className={ classes.{{ name.camel }} } data-testid="{{ name.title }}" ></div>
}; """,
        ),
        Definition(
            filename="{{ name.title }}Types.ts",
            definition="""

export interface {{ name.title }}Props {} """,
        ),
        Definition(
            filename="{{ name.title }}.module.scss",
            definition="""
@import "{{ depthDots }}App.scss";

.{{ name.camel }} {
}
            """,
        ),
        Definition(
            filename="{{ name.title }}.stories.tsx",
            definition="""
import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { {{ name.title }} } from "./{{ name.title }}";
import { ShellProvider } from "{{ depthDots }}providers/ShellProvider"

const meta: Meta<typeof {{ name.title }}> = {
  component: {{ name.title }},
  decorators: (Story) => <ShellProvider><Story/></ShellProvider>
};
export default meta;

type Story = StoryObj<typeof {{ name.title }}>;

export const Simple: Story = {
  args: {
  },
};""",
        ),
        Definition(
            filename=os.path.join(ForTestDirectory, ForTestFilename),
            definition="""
import React  from 'react';
import {expect, test} from '@jest/globals';
import { render, screen } from '@testing-library/react';
import { ShellProvider } from "{{ depthDots }}../providers/ShellProvider";
import { {{ name.title }} } from '../{{ name.title }}';

test('snapshot', () => {
  render(<ShellProvider><{{name.title}}/></ShellProvider>)
  const component = screen.getByTestId("{{ name.title }}")
  expect(component).toMatchSnapshot();
}); """,
        ),
    ],
    "pages": [
        Definition(
            filename="{{ name.title }}.tsx",
            definition="""
import React from "react";

import classes from "./{{ name.title }}.module.scss";
import { Layout } from "{{ depthDots }}components/Layout/Layout";


export function {{name.title}} () {
  return (
    <Layout
      className={ classes.{{ name.camel }} }
      pair={[
        <div>WIP: Put first here</div>,
        <div>WIP: Put second here</div>,
      ]}
    />
  );
}; """,
        ),
        Definition(
            filename="{{ name.title }}.module.scss",
            definition="""
@import "{{ depthDots }}App.scss";

.{{ name.camel }} {
}
            """,
        ),
        Definition(
            filename=os.path.join(ForTestDirectory, ForTestFilename),
            definition="""
import React  from 'react';
import {expect, test} from '@jest/globals';
import { render, screen } from '@testing-library/react';
import { ShellProvider } from "{{ depthDots }}../providers/ShellProvider";
import { {{ name.title }} } from '../{{ name.title }}';

test('snapshot', () => {
  render(<ShellProvider><{{name.title}}/></ShellProvider>)
  const page = screen.getByTestId("Layout")
  expect(page).toMatchSnapshot();
}); """,
        ),
    ],
}


def format_file(filename):
    process = subprocess.Popen(
        os.path.join(
            ".",
            "node_modules",
            ".bin",
            'prettier -w "{}"'.format(filename),
        ),
        shell=True,
        cwd=os.sep.join(self_directory + [".."]),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in process.stdout.readlines():
        print(str(line))
    process.wait()


def get_name_types(name):
    return {
        "title": name[0].upper() + name[1:],
        "camel": name[0].lower() + name[1:],
    }


def get_single_test_context(parts):
    context = {
        "name": get_name_types(parts[-3]),
        "filename": get_name_types(parts[-1]),
        "depthDots": "../" * (len(parts) - 1),
    }
    return context


def get_context(parts):
    context = {
        "name": get_name_types(parts[-1]),
        "depthDots": "../" * len(parts),
    }
    return context


def render_definition(context, definition):
    return Definition(
        filename=Template(definition.filename).render(context),
        definition=Template(PreTemplate + definition.definition + PostTemplate).render(
            context
        ),
    )


def execute_definition(context, target, definition):
    print(context, definition)
    rendered = render_definition(context, definition)
    absolute_filename = os.path.normpath(os.sep.join([target, rendered.filename]))
    pathlib.Path(os.path.dirname(absolute_filename)).mkdir(parents=True, exist_ok=True)
    print("Generating File: {}".format(absolute_filename))
    if os.path.isfile(absolute_filename):
        print("Not generating file {} because it exists".format(absolute_filename))
        return
    with open(absolute_filename, "w") as handle:
        handle.write(rendered.definition)
    format_file(absolute_filename)


def create(command):
    validate_parts(command.parts)
    context = get_context(command.parts)
    if command.parts[-2] == ForTestDirectory:
        execute_definition(
            get_single_test_context(command.parts),
            command.target,
            Definition(
                filename=os.path.join("..", "{{ filename.title }}.test.tsx"),
                definition=ForTestDefinition,
            ),
        )
        return
    for definition in definitions[command.parts[0]]:
        execute_definition(context, command.target, definition)


if __name__ == "__main__":
    try:
        create(get_command_from_sysargv())
    except RuntimeError as e:
        print("Error: {}".format(e), file=sys.stderr)
        exit(1)
