import React, { useEffect } from "react";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";
import { getRoute } from "./routes";
import { StartMeal } from "./pages/StartMeal/StartMeal";
import { StageMeal } from "./pages/StageMeal/StageMeal";
import { Noted } from "./components/Layout/NavigationBar/Noted/Noted";

const BaseRedirect = () => {
  const navigate = useNavigate();
  useEffect(() => {
    navigate(getRoute("StartMeal"));
  });
  return <>Redirecting ...</>;
};

export function ApplicationRouter() {
  return (
    <BrowserRouter>
      <Noted />
      <Routes>
        <Route path={getRoute("StageMeal")} element={<StageMeal />} />
        <Route path={getRoute("StartMeal")} element={<StartMeal />} />
        <Route path="/" element={<BaseRedirect />} />
        <Route path="*" element={<>404</>} />
      </Routes>
    </BrowserRouter>
  );
}
