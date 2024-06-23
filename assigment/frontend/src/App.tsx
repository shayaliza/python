import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";

const Register = React.lazy(() => import("./Pages/register"));
const Login = React.lazy(() => import("./Pages/login"));
const Home = React.lazy(() => import("./Pages/home"));

const App: React.FC = () => {
  return (
    <React.Suspense fallback={<div className="loading-container">Loading</div>}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </React.Suspense>
  );
};

export default App;
