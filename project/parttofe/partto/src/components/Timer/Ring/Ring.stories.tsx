import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Ring } from "./Ring";
import { ShellProvider } from "../../../providers/ShellProvider";

const meta: Meta<typeof Ring> = {
  component: Ring,
  decorators: (Story) => (
    <ShellProvider>
      <div style={{ width: "200px", height: "200px" }}>
        <Story />
      </div>
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Ring>;

export const Simple: Story = {
  args: {
    magnitude: 40,
    label: "world hello",
  },
};

export const First: Story = {
  args: {
    magnitude: 70,
    label: "hello world",
  },
};

export const Second: Story = {
  args: {
    magnitude: 160,
    label: "good bye",
  },
};

export const Third: Story = {
  args: {
    magnitude: 250,
    label: "bye good",
  },
};
