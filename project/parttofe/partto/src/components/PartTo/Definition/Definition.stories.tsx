import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Definition } from "./Definition";
import { ShellProvider } from "../../../providers/ShellProvider";
import { getDuration } from "../../../shared/duration";

const meta: Meta<typeof Definition> = {
  component: Definition,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Definition>;

export const Simple: Story = {
  args: {
    description: "a simple definition",
    duration: getDuration(0).toMilliseconds().toString(),
  },
};
