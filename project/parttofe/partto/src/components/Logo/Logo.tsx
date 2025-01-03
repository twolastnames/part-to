import React from "react";

import classes from "./Logo.module.scss";
import { LogoProps, Size } from "./LogoTypes";

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
        width: `${size * 0.8}px`,
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
            height: `${size * 0.8}px`,
            overflow: "hidden",
          }}
        >
          <div>T</div>
        </div>
        <div
          style={{
            height: `${size * 0.42}px`,
            overflow: "hidden",
            position: "relative",
            top: `-${size * 0.4}px`,
            left: `${size * 0.2}px`,
          }}
        >
          <div
            style={{
              position: "absolute",
              top: `-${size * 0.34}px`,
              width: `${size * 0.67}px`,
            }}
          >
            o
          </div>
        </div>
      </div>
    </div>
  );
}
