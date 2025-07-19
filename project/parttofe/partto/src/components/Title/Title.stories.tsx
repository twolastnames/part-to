import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Title } from "./Title";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Title> = {
  component: Title,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Title>;

export const Simple: Story = {
  args: {},
};
