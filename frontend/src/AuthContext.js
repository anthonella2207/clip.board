import React, { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// Create an authentication context
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // Holds the logged-in user data
    const [loading, setLoading] = useState(true); // Tracks loading state

    useEffect(() => {
        // Load user details from localStorage on initial render
        const storedUser = localStorage.getItem("user");
        const token = localStorage.getItem("token");
        if (storedUser && token) {
            setUser(JSON.parse(storedUser));
            console.log("🔹 User loaded from Local Storage:", JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    // Handles user login
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
                // Store user details
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

                // Log user login action
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

    const navigate = useNavigate();
    let logoutTimer;

    // Resets logout timer on user activity
    const resetLogoutTimer = () => {
        if (logoutTimer) clearTimeout(logoutTimer);
        logoutTimer = setTimeout(() => {
            logout();
        }, 10 * 60 * 1000);  // 10 minutes
    };

    // Handles user logout
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

                 // Log logout action
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
    // Auto logout after inactivity
     useEffect(() => {
        if (user) {
            resetLogoutTimer(); // start timer when user logs in

            // options for user activity
            window.addEventListener("mousemove", resetLogoutTimer);
            window.addEventListener("keydown", resetLogoutTimer);
            window.addEventListener("click", resetLogoutTimer);
        }

        return () => {
            clearTimeout(logoutTimer);
            window.removeEventListener("mousemove", resetLogoutTimer);
            window.removeEventListener("keydown", resetLogoutTimer);
            window.removeEventListener("click", resetLogoutTimer);
        };
    }, [user]);

     // Update user email
     const updateEmail = async (newEmail, currentPassword) => {
        if (!user) {
            return { success: false, message: "User not logged in" };
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/update_email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: user.id,
                    new_email: newEmail,
                    password: currentPassword,
                }),
            });

            const data = await response.json();
            if (data.success) {
            // Update local user data
                const updatedUser = { ...user, email: newEmail };
                setUser(updatedUser);
                localStorage.setItem("user", JSON.stringify(updatedUser));
            }

            return data;
        } catch (error) {
            console.error("Error updating email:", error);
            return { success: false, message: "Server error" };
        }
    };

     //update password
     const updatePassword = async (currentPassword, newPassword) => {
        if (!user) {
            return { success: false, message: "User not logged in" };
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/update_password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: user.id,
                    old_password: currentPassword,
                    new_password: newPassword,
                }),
            });

            const data = await response.json();
            return data; // Erfolgs- oder Fehlermeldung vom Backend zurückgeben
        } catch (error) {
            console.error("Error updating password:", error);
            return { success: false, message: "Server error" };
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading, updateEmail, updatePassword }}>
            {children}
        </AuthContext.Provider>
    );
};