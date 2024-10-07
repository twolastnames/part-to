
import React from 'react';
 
import type { Preview } from '@storybook/react';
import { MemoryRouter } from "react-router";

export const parameters = { layout: 'fullscreen' }

export const preview: Preview = {
  decorators:[
    (Story) => <MemoryRouter initialEntries={['/']}>
       <Story/> 
    </MemoryRouter>,
  ],
}

