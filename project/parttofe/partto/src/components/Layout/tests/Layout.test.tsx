import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Layout } from "../Layout";
import { Next, Start } from "../../Icon/Icon";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Layout
        pair={[
          {
            items: [],
            setOperations: [
              {
                icon: Start,
                text: "start cooking",
                onClick: () => console.log("clicked"),
              },
              {
                icon: Next,
                text: "mark complete",
                onClick: () => console.log("clicked"),
              },
            ],
            emptyPage: <div>Empty Yo</div>,
          },
          {
            items: [],
            setOperations: [
              {
                icon: Start,
                text: "start cooking",
                onClick: () => console.log("clicked"),
              },
              {
                icon: Next,
                text: "mark complete",
                onClick: () => console.log("clicked"),
              },
            ],
            emptyPage: <div>Empty Yo</div>,
          },
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Layout");
  expect(component).toBeTruthy();
});
