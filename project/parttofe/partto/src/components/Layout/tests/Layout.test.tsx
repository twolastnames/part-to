import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../ShellProvider";
import { Layout } from "../Layout";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Layout />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Layout");
  expect(component).toMatchSnapshot();
});
