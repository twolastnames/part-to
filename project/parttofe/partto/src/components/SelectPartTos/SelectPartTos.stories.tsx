import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { SelectPartTos } from "./SelectPartTos";
import { ShellProvider } from "../../providers/ShellProvider";

const meta: Meta<typeof SelectPartTos> = {
  component: SelectPartTos,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof SelectPartTos>;

export const Simple: Story = {
  args: {},
};
