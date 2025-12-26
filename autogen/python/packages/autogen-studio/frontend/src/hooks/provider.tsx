import React, { useState, useEffect } from "react";
import { AuthProvider, useAuth } from "../auth/context";
import { getLocalStorage, setLocalStorage } from "../components/utils/utils";
import { User } from "../auth/api";
import { useHydrateStore } from "./store";

export interface AppContextType {
  darkMode: string;
  setDarkMode: any;
  user: User | null;
  setUser: any;
  logout: any;
  cookie_name: string;
}

export const appContext = React.createContext<AppContextType>(
  {} as AppContextType
);

const AppProvider = ({ children }: any) => {
  // Trigger manual rehydration of Zustand store on client mount
  useHydrateStore();

  // Dark mode handling
  const [darkMode, setDarkMode] = useState("light");

  useEffect(() => {
    const storedValue = getLocalStorage("darkmode", false);
    if (storedValue) {
      setDarkMode(storedValue === "dark" ? "dark" : "light");
    }
  }, []);

  const updateDarkMode = (darkMode: string) => {
    setDarkMode(darkMode);
    setLocalStorage("darkmode", darkMode, false);
  };

  // We'll use auth context to get user and logout function
  const { user, logout } = useAuth();

  return (
    <appContext.Provider
      value={{
        user,
        setUser: () => { },
        logout,
        cookie_name: "coral_app_cookie_",
        darkMode,
        setDarkMode: updateDarkMode,
      }}
    >
      {children}
    </appContext.Provider>
  );
};

// Combined provider that includes both Auth and App context
export default ({ element }: any) => (
  <AuthProvider>
    <AppProvider>{element}</AppProvider>
  </AuthProvider>
);
