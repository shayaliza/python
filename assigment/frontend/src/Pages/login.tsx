import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./../components/ui/tabs";
import JwtLogin from "./jwLogin";
import SessionLogin from "./sessionLogin";

function Login() {
  return (
    <div className="flex flex-col items-center justify-between h-screen">
      <Tabs defaultValue="jwt" className="w-full  mt-4">
        <TabsList className="flex justify-center">
          <TabsTrigger value="jwt">Login with Jwt</TabsTrigger>
          <TabsTrigger value="session">Login with Session</TabsTrigger>
        </TabsList>
        <TabsContent value="jwt">
          <JwtLogin />
        </TabsContent>
        <TabsContent value="session">
          <SessionLogin />
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default Login;
