import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { DetailShell } from "../DetailShell";

test("snapshot", () => {
  render(
    <ShellProvider>
      <DetailShell name="Some Name">
        <div>hello</div>
      </DetailShell>
    </ShellProvider>,
  );
  const component = screen.getByTestId("DetailShell");
  expect(component).toMatchSnapshot();
});
