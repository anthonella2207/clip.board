import { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "./AuthContext";

// This component protects routes that require authentication
export default function ProtectedRoute() {
    const { user } = useContext(AuthContext);

    // If the user is authenticated, render the requested route
    // Otherwise, redirect to the login page
    return user ? <Outlet /> : <Navigate to="/login" replace />;
}
