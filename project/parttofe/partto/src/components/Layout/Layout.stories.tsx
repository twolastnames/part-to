import React from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { Layout } from "./Layout";
import { ShellProvider } from "../../providers/ShellProvider";
import { Next, Start } from "../Icon/Icon";

const meta: Meta<typeof Layout> = {
  component: Layout,
  decorators: (Story) => (
    <ShellProvider>
      <Story />
    </ShellProvider>
  ),
};
export default meta;

type Story = StoryObj<typeof Layout>;

export const Simple: Story = {
  args: {
    pair: [
      {
        items: [],
        setOperations: [
          {
            icon: Start,
            text: "start cooking",
            onClick: () => console.log("clicked"),
          },
          {
            icon: Next,
            text: "mark complete",
            onClick: () => console.log("clicked"),
          },
        ],
        emptyPage: <div>Empty Yo</div>,
      },
      {
        items: [],
        setOperations: [
          {
            icon: Start,
            text: "start cooking",
            onClick: () => console.log("clicked"),
          },
          {
            icon: Next,
            text: "mark complete",
            onClick: () => console.log("clicked"),
          },
        ],
        emptyPage: <div>Empty Yo</div>,
      },
    ],
  },
};
