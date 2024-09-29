import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Button } from "../Button";
import { MantineProvider } from "@mantine/core";
import { Next } from "../../Icon/Icon";

describe("Button", () => {
  beforeAll(() => {});

  test("snapshot", () => {
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
    render(
      <MantineProvider>
        <Button icon={Next} onClick={() => undefined}>
          Hello
        </Button>
      </MantineProvider>,
    );
    const component = screen.getByTestId("Button");
    expect(component).toMatchSnapshot();
  });
});
