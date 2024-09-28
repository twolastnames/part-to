import React from 'react'

import { MantineProvider } from "@mantine/core";
import '@mantine/core/styles.layer.css';
import { PropsWithChildren } from 'react';

export const ShellProvider = (
    {children}: PropsWithChildren) => <MantineProvider>{children}</MantineProvider>
