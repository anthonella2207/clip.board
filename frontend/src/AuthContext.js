import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        const token = localStorage.getItem("token"); // Assuming you have a token stored
        if (storedUser && token) {
            setUser(JSON.parse(storedUser));
            console.log("🔹 User loaded from Local Storage:", JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();
            console.log("Login API Response:", data);

            if (data.success && data.user_id) {
                const userData = {
                    id: data.user_id,
                    email: data.email,
                    firstName: data.first_name,
                    lastName: data.last_name,
                    role: data.role,
                };
                setUser(userData);
                localStorage.setItem("user", JSON.stringify(userData));
                console.log("User saved:", userData);

                await fetch("http://127.0.0.1:5000/add_log", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        action: "User logged in",
                        user_id: data.user_id,
                    }),
                });

                return { success: true };
            } else {
                return { success: false, message: data.message };
            }
        } catch (error) {
            console.error("Login error:", error);
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
                localStorage.removeItem("token"); // Remove token
                console.log("User logged out successfully.");

                await fetch("http://127.0.0.1:5000/add_log", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        action: "User logged out",
                        user_id: user?.id,
                    }),
                });
            } else {
                console.error("Logout error:", data.message);
            }
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};