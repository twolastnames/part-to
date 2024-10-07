import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../ShellProvider";
import { Logo } from "../Logo";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Logo />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Logo");
  expect(component).toMatchSnapshot();
});
