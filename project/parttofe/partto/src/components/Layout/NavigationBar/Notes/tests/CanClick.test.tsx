import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Notes } from "../Notes";

test("snapshot", async () => {
  const onClick = jest.fn();
  render(
    <ShellProvider>
      <Notes
        notes={[
          {
            heading: "my heading",
            detail: <span data-testid="bubbleup">my detail</span>,
            onClick,
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("bubbleup");
  await component.click();
  expect(onClick).toBeCalledTimes(1);
});
