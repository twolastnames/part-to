import type { Meta, StoryObj } from "@storybook/react";

import { JobPost } from "./JobPost";

const meta: Meta<typeof JobPost> = {
  component: JobPost,
};
export default meta;

type Story = StoryObj<typeof JobPost>;

export const Post: Story = {
  args: {},
};
