import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { EmptySimpleView } from "../EmptySimpleView";

test("snapshot", () => {
  render(
    <ShellProvider>
      <EmptySimpleView content="Hello World" />
    </ShellProvider>,
  );
  const component = screen.getByTestId("EmptySimpleView");
  expect(component).toMatchSnapshot();
});
