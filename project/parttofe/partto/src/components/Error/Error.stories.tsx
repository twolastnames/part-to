import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Error } from "./Error";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof Error> = {
  component: Error,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Error>;

export const Simple: Story = {
  args: { code: 400 },
};
