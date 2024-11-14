import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { SelectPartTos } from "./SelectPartTos";
import { ShellProvider } from "../../providers/ShellProvider";
import { MemoryRouter } from "react-router-dom";

const meta: Meta<typeof SelectPartTos> = {
  component: SelectPartTos,
  decorators: (Story) => (
    <ShellProvider>
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof SelectPartTos>;

export const Simple: Story = {
  args: {},
};
