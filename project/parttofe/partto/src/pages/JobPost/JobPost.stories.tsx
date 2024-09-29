import type { Meta, StoryObj } from "@storybook/react";

import { JobPost } from "./JobPost";
import { MemoryRouter } from "react-router-dom";
import { MantineProvider } from "@mantine/core";

const meta: Meta<typeof JobPost> = {
  component: JobPost,
  decorators: [
    (Story) => (
      <MantineProvider>
        <MemoryRouter initialEntries={["/"]}>
          <Story />
        </MemoryRouter>
        ,
      </MantineProvider>
    ),
  ],
};
export default meta;

type Story = StoryObj<typeof JobPost>;

export const Post: Story = {
  args: {},
};
