import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Timer } from "../Timer";
import { getDuration } from "../../../shared/duration";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Timer duration={getDuration(5000)} />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Ring");
  expect(component).toMatchSnapshot();
});
