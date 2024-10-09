import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../ShellProvider";
import { Menu } from "../Menu";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Menu />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Menu");
  expect(component).toMatchSnapshot();
});
