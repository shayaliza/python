// store.js
import { configureStore } from "@reduxjs/toolkit";
import userReducer, { initializeUser } from "./feature/userSlice";

const store = configureStore({
  reducer: {
    user: userReducer,
  },
});
store.dispatch(initializeUser());

export default store;
