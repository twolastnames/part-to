import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Note } from "./Note";
import { ShellProvider } from "../../../../ShellProvider";

const meta: Meta<typeof Note> = {
  component: Note,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Note>;

export const Simple: Story = {
  args: {},
};
