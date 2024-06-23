import { useEffect } from "react";
import { Button } from "../components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../components/ui/card";

import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import { clearUser } from "./../feature/userSlice";
import { toast, useToast } from "../components/ui/use-toast";
import axios from "axios";

function Home() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    if (!email) {
      navigate("/login");
    }
  }, []);

  const AuthType = useSelector((state: any) => state.user.authType);
  const access_token = useSelector(
    (state: any) => state.user.userData.accessToken
  );
  const email = useSelector((state: any) => state.user.userData.email);

  const handleLogout = () => {
    dispatch(clearUser());
    navigate("/login");
  };

  const handleCheckAuth = async () => {
    try {
      console.log(email, access_token);
      const response = await axios.post("http://localhost:8000/auth/verify", {
        email,
        token: access_token || null,
      });
      console.log(response.data);
      toast({
        title: "Yes you are authenticated",
      });
    } catch (error) {}
  };
  return (
    <div className="bg-shayalizaskin h-screen font-quicksand">
      <div className="flex justify-between p-4">
        <div className="text-lg  text-shayalizablue font-bold ">
          Hello, User ! You are Authenticated with{" "}
          {AuthType == "JWT" ? "JWT" : "Session"}{" "}
        </div>
        <Button variant={"destructive"} onClick={handleLogout}>
          Logout
        </Button>
      </div>
      <div className="m-auto w-full mt-20 flex justify-center items-center ">
        <Card className="w-[350px]">
          <CardHeader>
            <CardTitle>Test Validation</CardTitle>
            <CardDescription>
              Send an Api Request to backend to check if user is Authenticated
            </CardDescription>
          </CardHeader>
          <CardFooter className="flex justify-end">
            <Button
              className="text-shayalizablue bg-shayalizaskin font-semibold"
              onClick={handleCheckAuth}
            >
              Send Request
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

export default Home;
