import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Carousel } from "../Carousel";

test("snapshot", async () => {
  jest.useFakeTimers();
  render(
    <ShellProvider>
      <Carousel
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
  expect(screen.getByText("hello")).toBeTruthy();
  expect(screen.queryByText("world")).toBeFalsy();
  const pauseButton = screen.getByTitle("Pause");
  await pauseButton.click();
  jest.advanceTimersByTime(9000);
  expect(screen.getByText("hello")).toBeTruthy();
  expect(screen.queryByText("world")).toBeFalsy();
  const unpauseButton = screen.getByTitle("Unpause");
  await unpauseButton.click();
  jest.advanceTimersByTime(6000);
  expect(await screen.findByText("world")).toBeTruthy();
  expect(screen.queryByText("hello")).toBeFalsy();
});
