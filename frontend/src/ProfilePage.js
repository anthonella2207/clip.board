import React, { useState, useContext, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import defaultProfilePic from "./images/defaultProfilePic.jpg";
import "./ProfilePage.css";
import { useNavigate } from "react-router-dom";
import { FaSignOutAlt } from "react-icons/fa";

function ProfilePage() {
    const { user, updateEmail, updatePassword, logout } = useContext(AuthContext); // Agregar logout
    const [newEmail, setNewEmail] = useState("");
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        if (!user) {
            navigate("/login");
        }
    }, [user, navigate]);

    const handleEmailChange = async (e) => {
        e.preventDefault();
        const result = await updateEmail(newEmail, currentPassword);
        setMessage(result.message);
    };

    const handlePasswordChange = async (e) => {
        e.preventDefault();
        const result = await updatePassword(currentPassword, newPassword);
        setMessage(result.message);
    };

    return (
        <div className="profile-container">
            {/* Sección izquierda: Cambio de email y contraseña */}
            <div className="profile-left">
                <h2>Change Email</h2>
                <form onSubmit={handleEmailChange}>
                    <input type="email" placeholder="New Email" value={newEmail}
                           onChange={(e) => setNewEmail(e.target.value)} required />
                    <input type="password" placeholder="Current Password" value={currentPassword}
                           onChange={(e) => setCurrentPassword(e.target.value)} required />
                    <button type="submit">Update Email</button>
                </form>

                <h2>Change Password</h2>
                <form onSubmit={handlePasswordChange}>
                    <input type="password" placeholder="Current Password" value={currentPassword}
                           onChange={(e) => setCurrentPassword(e.target.value)} required />
                    <input type="password" placeholder="New Password" value={newPassword}
                           onChange={(e) => setNewPassword(e.target.value)} required />
                    <button type="submit">Update Password</button>
                </form>

                {message && <p className="message">{message}</p>}
            </div>

            {/* Sección derecha: Información del usuario y Logout */}
            <div className="profile-right">
                <img src={defaultProfilePic} alt="Profile" className="profile-picture" />
                <h2>User Information</h2>
                <p><strong>Email:</strong> {user?.email}</p>
                <p><strong>First Name:</strong> {user?.firstName || "N/A"}</p>
                <p><strong>Last Name:</strong> {user?.lastName || "N/A"}</p>

                {/* Botón de Logout */}
                <button onClick={logout} className="logout-button">
                    <FaSignOutAlt /> Logout
                </button>
            </div>
        </div>
    );
}

export default ProfilePage;
