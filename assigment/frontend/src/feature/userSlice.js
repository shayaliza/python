import { createSlice } from "@reduxjs/toolkit";
import { setCookie, getCookie, removeCookie } from "../cookie";

const initialState = {
  userData: null,
  isLoggedIn: false,
  authType: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    loadUserFromCookie: (state) => {
      const userData = getCookie("userData");
      if (userData) {
        const parsedData = JSON.parse(userData);
        state.userData = parsedData;
        state.isLoggedIn = !!parsedData.accessToken;
        state.authType = parsedData.authType || null;
      }
    },
    setUser: (state, action) => {
      const { email, accessToken, authType } = action.payload;
      state.userData = { email, accessToken, authType };
      state.isLoggedIn = true;
      state.authType = authType;
      setCookie("userData", JSON.stringify({ email, accessToken, authType }));
    },
    clearUser: (state) => {
      state.userData = null;
      state.isLoggedIn = false;
      state.authType = null;
      removeCookie("userData");
    },
    setAuthType: (state, action) => {
      state.authType = action.payload;
      if (state.userData) {
        state.userData.authType = action.payload;
        setCookie("userData", JSON.stringify(state.userData));
      }
    },
  },
});

export const { loadUserFromCookie, setUser, clearUser, setAuthType } =
  userSlice.actions;

export const initializeUser = () => (dispatch) => {
  dispatch(loadUserFromCookie());
};

export default userSlice.reducer;
