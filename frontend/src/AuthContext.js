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
            console.log("Login API Response:", data);

            if(data.success && data.user_id){
                const userData = { id: data.user_id, email, firstName: data.first_name, lastName: data.last_name };
                setUser(userData);
                localStorage.setItem("user", JSON.stringify(userData));
                console.log("User gespeichert:", userData);

                await fetch("http://127.0.0.1:5000/add_log", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        action: "User logged in",
                        user_id: data.user_id
                    }),
                });
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

                await fetch("http://127.0.0.1:5000/add_log", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        action: "User logged out",
                        user_id: user.id
                    }),
                });
            }
            else {
                console.error("Logout failed:", data.message);
            }
        }
        catch (error) {
            console.error("Error during logout:", error);
        }
    };

    const updateEmail = async (newEmail, password) => {
        if(!user) {
            return {success: false, message: "User not logged in"};
        }

        try{
            const response = await fetch("http://127.0.0.1:5000/update_email", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({user_id: user.id, new_email: newEmail, password}),
            });

            const data = await response.json();
            if(data.success){
                setUser({...user, email: newEmail});
                localStorage.setItem("user", JSON.stringify({...user, email: newEmail}));
            }
            return data;
        }
        catch (error){
            console.error("Error updating email: ", error);
            return {success: false, message: "Server error"};
        }
    };

    const updatePassword = async (oldPassword, newPassword) => {
        if(!user){
            return {success: false, message: "User not logged in"};
        }
        try{
            const response = await fetch("http://127.0.0.1:5000/update_password", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({user_id: user.id, old_password: oldPassword, new_password: newPassword}),
            });

            return await response.json();
        }
        catch (error){
            console.error("Error updating password: ", error);
            return {success: false, message: "Server error"};
        }
    };

    return(
        <AuthContext.Provider value={{ user, login, logout, updateEmail, updatePassword }}>
            {children}
        </AuthContext.Provider>
    );
};