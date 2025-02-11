import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if(storedUser){
            setUser(JSON.parse(storedUser));
            console.log("🔹 User aus Local Storage geladen:", JSON.parse(storedUser));
        }
    }, []);

    const login = async(email, password) => {
        try{
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({email, password}),
            });
            const data = await response.json();
            console.log("🔹 Login API Response:", data);

            if(data.success && data.user_id){
                const userData = { id: data.user_id, email };
                setUser(userData);
                localStorage.setItem("user", JSON.stringify(userData));
                console.log("✅ User gespeichert:", userData);
                return{success: true};
            }
            else{
                return{success: false, message: data.message};
            }
        }
        catch(error){
            console.error("Login failed:", error);
            return { success: false, message: "Server error" };
        }
    };

    const logout = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/logout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            const data = await response.json();
            if (data.success) {
                setUser(null);
                localStorage.removeItem("user");
                console.log("User successfully logged out.");
            }
            else {
                console.error("Logout failed:", data.message);
            }
        }
        catch (error) {
            console.error("Error during logout:", error);
        }
    };

    return(
        <AuthContext.Provider value={{user, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
};