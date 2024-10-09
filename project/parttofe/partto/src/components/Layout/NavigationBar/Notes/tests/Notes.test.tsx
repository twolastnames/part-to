import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../ShellProvider";
import { Notes } from "../Notes";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Notes
        notes={[
          { detail: "may be in the middle of the keyboard", heading: "C" },
          {
            detail: "high pitched, but there could be higher octaves",
            heading: "F",
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Notes");
  expect(component).toMatchSnapshot();
});
