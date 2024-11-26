import React from "react";
import { expect, test } from "@jest/globals";
import { render, screen, waitFor } from "@testing-library/react";
import { ShellProvider } from "../../../../../providers/ShellProvider";
import { Carousel } from "../Carousel";
import { RightContext } from "../../../../../providers/DynamicItemSetPair";

test("snapshot", async () => {
  jest.useFakeTimers();
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
  expect(screen.getByText("hello")).toBeTruthy();
  expect(screen.queryByText("world")).toBeFalsy();
  const pauseButton = screen.getByTitle("Unpaused");
  await pauseButton.click();
  jest.advanceTimersByTime(9000);
  expect(screen.getByText("hello")).toBeTruthy();
  expect(screen.queryByText("world")).toBeFalsy();
  // eslint-disable-next-line testing-library/prefer-find-by
  const unpauseButton = await waitFor(() => screen.getByTitle("Paused"));
  expect(unpauseButton).toBeTruthy();
});
