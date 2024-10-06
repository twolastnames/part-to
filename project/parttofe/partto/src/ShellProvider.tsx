import React from "react";

import { MantineProvider, createTheme } from "@mantine/core";
import { PropsWithChildren } from "react";
import "@mantine/core/styles.layer.css";
import "./App.scss";

const theme = createTheme({
  primaryColor: "red",
});

export const ShellProvider = ({ children }: PropsWithChildren) => (
  <MantineProvider theme={theme}>{children}</MantineProvider>
);
