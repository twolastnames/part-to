import React, { useCallback, useEffect, useState } from "react";
import { ActionIcon as MantineButton, Tooltip } from "@mantine/core";

import classes from "./Button.module.scss";
import { IconType, Icon, Size as IconSize } from "../Icon/Icon";
import { requestStateListeners } from "../../api/helpers";
import { debounce } from "lodash";

export interface ButtonProps {
  text: string;
  icon: IconType;
  onClick: () => void;
}

export const Button = ({ onClick, icon, text }: ButtonProps) => {
  const [disabled, setDisabled] = useState<boolean>(false);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debouncedSetDisabled = useCallback(
    debounce(
      (value: boolean) => {
        setDisabled(value);
      },
      50,
      { trailing: true },
    ),
    [disabled],
  );
  useEffect(() => {
    requestStateListeners.add(debouncedSetDisabled);
    return () => {
      requestStateListeners.delete(debouncedSetDisabled);
    };
  }, [debouncedSetDisabled]);
  return (
    <>
      <Tooltip label={text} data-testid="Button">
        <div onClick={onClick} className={classes.container}>
          <MantineButton
            data-testid="Button"
            aria-label={text}
            className={classes.button}
            disabled={disabled}
          >
            <Icon definition={icon} size={IconSize.Small} />
          </MantineButton>
        </div>
      </Tooltip>
    </>
  );
};
