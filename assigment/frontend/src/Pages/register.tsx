import React, { useState } from "react";
import axios from "axios";
import { useToast } from "../components/ui/use-toast";
import { useNavigate } from "react-router-dom";

function Register() {
  const { toast } = useToast();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      console.log(username, email, password);
      const response = await axios.post(
        "http://localhost:8000/auth/register",
        {
          username: username,
          email: email,
          password: password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Registration successful:", response.data);
      toast({
        title: "Registration successful",
      });

      navigate("/login");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(
          "Registration failed:",
          error.response?.data || error.message
        );
      } else {
        console.error("Registration failed:", error);
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-shayalizaskin">
      <div className="bg-shayalizablue p-8 rounded-lg shadow-md w-full max-w-sm font-quicksand">
        <h2 className="text-2xl font-bold mb-6 text-center text-shayalizaskin">
          Register
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="username" className="block text-shayalizaskin">
              Username
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-2 p-2 border-4 border-shayalizaskin bg-transparent rounded-md w-full text-shayalizaskin"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="email" className="block text-shayalizaskin">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-2 p-2 border-4 border-shayalizaskin bg-transparent rounded-md w-full text-shayalizaskin"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="block text-shayalizaskin">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-2 p-2 border-4 border-shayalizaskin bg-transparent rounded-md w-full text-shayalizaskin"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-shayalizaskin text-shayalizablue font-bold py-2 px-4 rounded-md w-full hover:bg-shayalizablue hover:text-shayalizaskin"
          >
            Register
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
