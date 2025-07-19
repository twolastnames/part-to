import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Notes } from "../Notes";
import { TimeToLive } from "../NotesTypes";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Notes
        notes={[
          {
            detail: "may be in the middle of the keyboard",
            heading: "C",
            timeToLive: TimeToLive.NOTICABLE,
          },
          {
            detail: "high pitched, but there could be higher octaves",
            heading: "F",
            timeToLive: TimeToLive.NOTICABLE,
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Notes");
  expect(component).toMatchSnapshot();
});
