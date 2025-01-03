import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Notes } from "./Notes";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { TimeToLive } from "./NotesTypes";

const meta: Meta<typeof Notes> = {
  component: Notes,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Notes>;

export const Simple: Story = {
  args: {
    notes: [
      {
        heading: "heading",
        detail: "some stuff",
        timeToLive: TimeToLive.NOTICABLE,
      },
    ],
  },
};

export const TimerAlert: Story = {
  args: {
    notes: [
      {
        heading: "heading",
        detail: "some stuff",
        timeToLive: TimeToLive.NOTICABLE,
      },
    ],
  },
};
