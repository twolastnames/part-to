import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { FourOhFour } from "../FourOhFour";

test("snapshot", () => {
  render(
    <ShellProvider>
      <FourOhFour />
    </ShellProvider>,
  );
  const page = screen.getByTestId("Layout");
  expect(page).toMatchSnapshot();
});
