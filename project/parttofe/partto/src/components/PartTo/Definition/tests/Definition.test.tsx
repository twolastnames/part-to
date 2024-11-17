import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { Definition } from "../Definition";
import { getDuration } from "../../../../shared/duration";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Definition
        description="a simple definition"
        duration={getDuration(0).toMilliseconds().toString()}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Definition");
  expect(component).toMatchSnapshot();
});
