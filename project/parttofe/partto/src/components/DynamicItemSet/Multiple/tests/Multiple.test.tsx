import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../providers/ShellProvider";
import { Multiple } from "../Multiple";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Multiple
        items={[
          {
            key: "9",
            listView: <div>first list view</div>,
            detailView: <div>first detail view</div>,
            itemOperations: [],
          },
          {
            key: "4",
            listView: <div>second list view</div>,
            detailView: <div>second detail view</div>,
            itemOperations: [],
          },
        ]}
      />
      ,
    </ShellProvider>,
  );

  const component = screen.getByTestId("Multiple");
  expect(component).toMatchSnapshot();
});
