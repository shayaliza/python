import React, { useState } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { useToast } from "../components/ui/use-toast";
import { setUser } from "../feature/userSlice";
import { useNavigate } from "react-router-dom";

function JwtLogin() {
  const dispatch = useDispatch();
  const { toast } = useToast();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      console.log(email, password);

      // Create a FormData object and append the email and password
      const formData = new FormData();
      formData.append("username", email);
      formData.append("password", password);

      // Log the form data contents
      for (let pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }

      const response = await axios.post(
        "http://localhost:8000/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      console.log("Registration successful:", response.data);
      // dispatch(setUser({ accessToken: response.data.access_token }));
      // dispatch(
      //   setUser({
      //     email: email,
      //     password: password,
      //     accessToken: response.data.access_token,
      //   })
      // );
      dispatch(
        setUser({
          email: email,
          // password: password,
          accessToken: response.data.access_token,
          authType: "JWT",
        })
      );

      navigate("/");

      toast({
        title: "Login successful with JWT",
      });
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
    <>
      <div className="min-h-screen flex items-center justify-center bg-shayalizaskin">
        <div className="bg-shayalizablue p-8 rounded-lg shadow-md w-full max-w-sm font-quicksand">
          <h2 className="text-2xl font-bold mb-6 text-center text-shayalizaskin">
            Login with JWT
          </h2>
          <form onSubmit={handleSubmit}>
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
              Login
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
export default JwtLogin;
