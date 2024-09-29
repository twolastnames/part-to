import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Button } from "./Button";
import { ShellProvider } from "../../ShellProvider";
import { Next, Start } from "../Icon/Icon";

const meta: Meta<typeof Button> = {
  component: Button,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Button>;

export const NextButton: Story = {
  args: {
    onClick: () => console.log("clicked"),
    icon: Next,
    children: "Is Complete",
  },
};

export const StartButton: Story = {
  args: {
    onClick: () => console.log("clicked"),
    icon: Start,
    children: "Start Making Dinner",
  },
};
