import {describe, expect, test} from '@jest/globals';
import {Button} from '../Button';
import { render, screen } from '@testing-library/react';

describe('Button', () => {
    beforeAll(() => {
        render(<Button onClick={() => undefined}/>)
    })
  test('snapshot', () => {
    const component = screen.getByTestId('Button')
    expect(component).toMatchSnapshot();
  });
});
