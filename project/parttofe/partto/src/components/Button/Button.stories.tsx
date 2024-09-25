import type { Meta, StoryObj } from "@storybook/react";
import '@mantine/core/styles.layer.css';
import { MantineProvider } from "@mantine/core";

import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  component: Button,
  decorators: (Story) => <MantineProvider><Story/></MantineProvider>
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Fetching: Story = {
  args: {
    children: <div>&lt;</div>
  },
};

