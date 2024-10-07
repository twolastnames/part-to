import React from "react";

import classes from "./Logo.module.scss";

export enum Size {
  Small = 60,
  Medium = 120,
  Large = 240,
}

export interface LogoProps {
  size?: Size;
}

export function Logo({ size: rawSize }: LogoProps) {
  const size = rawSize || Size.Medium;
  return (
    <div
      className={classes.logo}
      data-testid="Logo"
      style={{
        display: "inline-block",
        height: `${size * 0.5}px`,
        overflow: "hidden",
        width: `${size * 1.5}px`,
        fontFamily: '"Courier New", Courier, monospace',
        fontSize: `${size}px`,
        lineHeight: `${size * 1.5}px`,
      }}
    >
      <div
        style={{
          position: "relative",
          top: `-${size * 0.4}px`,
        }}
      >
        <div
          style={{
            height: `${size * 0.65}px`,
            overflow: "hidden",
          }}
        >
          <div>T</div>
        </div>
        <div
          style={{
            height: `${size * 0.6}px`,
            overflow: "hidden",
            position: "relative",
            top: `-${size * 0.4}px`,
            left: `${size * 0.2}px`,
          }}
        >
          <div
            style={{
              position: "relative",
              top: `-${size * 0.2}px`,
            }}
          >
            o
          </div>
        </div>
      </div>
    </div>
  );
}
