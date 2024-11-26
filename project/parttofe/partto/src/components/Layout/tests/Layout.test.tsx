import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../providers/ShellProvider";
import { Layout } from "../Layout";
import { Next, Start } from "../../Icon/Icon";
import { DynamicItemSet } from "../../DynamicItemSet/DynamicItemSet";
import {
  LeftContext,
  RightContext,
} from "../../../providers/DynamicItemSetPair";

test("snapshot", () => {
  render(
    <ShellProvider>
      <Layout
        pair={[
          <DynamicItemSet
            items={[]}
            context={LeftContext}
            setOperations={[
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
            ]}
            emptyPage={<div>Empty Yo</div>}
          />,
          <DynamicItemSet
            items={[]}
            context={RightContext}
            setOperations={[
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
            ]}
            emptyPage={<div>Empty Yo</div>}
          />,
        ]}
      />
    </ShellProvider>,
  );
  const component = screen.getByTestId("Layout");
  expect(component).toBeTruthy();
});
