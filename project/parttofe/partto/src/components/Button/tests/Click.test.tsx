import React from "react";
import { describe, expect, test } from "@jest/globals";
import { fireEvent, render, screen } from "@testing-library/react";
import { Button } from "../Button";
import { MantineProvider } from "@mantine/core";
import { Next } from "../../Icon/Icon";

describe("Button", () => {
  beforeAll(() => {});

  test("snapshot", async () => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: jest.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // Deprecated
        removeListener: jest.fn(), // Deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    });
    const onClick = jest.fn();
    render(
      <MantineProvider>
        <Button icon={Next} text="Hello" onClick={onClick} />
      </MantineProvider>,
    );
    const button = screen.getByTestId("Button");
    await fireEvent.click(button);
    expect(onClick).toBeCalledTimes(1);
  });
});
