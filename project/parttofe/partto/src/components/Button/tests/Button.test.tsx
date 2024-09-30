import React from "react";
import { describe, expect, test } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { Button } from "../Button";
import { MantineProvider } from "@mantine/core";
import { Next } from "../../Icon/Icon";

describe("Button", () => {
  beforeAll(() => {});

  test("snapshot", () => {
    render(
      <MantineProvider>
        <Button icon={Next} text={"Hello"} onClick={() => undefined} />
      </MantineProvider>,
    );
    const component = screen.getByTestId("Button");
    expect(component).toMatchSnapshot();
  });
});
