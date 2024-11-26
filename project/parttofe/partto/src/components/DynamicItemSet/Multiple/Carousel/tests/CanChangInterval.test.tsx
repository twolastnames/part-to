import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Carousel } from "../Carousel";
import { RightContext } from "../../../../../providers/DynamicItemSetPair";

test("snapshot", async () => {
  render(
    <ShellProvider>
      <Carousel
        context={RightContext}
        items={[
          {
            key: "9",
            detailView: <div>hello</div>,
            listView: <div>hello</div>,
            itemOperations: [],
          },
          {
            key: "7",
            detailView: <div>world</div>,
            listView: <div>world</div>,
            itemOperations: [],
          },
        ]}
      />
    </ShellProvider>,
  );
  const slow = screen.getByTitle("8 Seconds");
  await slow.click();
  jest.advanceTimersByTime(1000);
  const slower = screen.getByTitle("16 Seconds");
  expect(slower).toBeTruthy();
});
