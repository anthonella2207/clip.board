import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "./AuthContext";
import "./AdminLogs.css";

export default function AdminLogs() {
    //gets current user from AuthContext
    const { user } = useContext(AuthContext);
    //check if user is admin
    const isAdmin = user?.role === "Admin";

    //states for logs and filters
    const [logs, setLogs] = useState([]);
    const [filterUser, setFilterUser] = useState("");
    const [filterAction, setFilterAction] = useState("");

    //called if filterUser or filterAction changes
    useEffect(() => {
        fetchLogs();
    }, [filterUser, filterAction]);

    //function to request the logs data from the backend
    const fetchLogs = async () => {
        let url = "http://127.0.0.1:5000/api/user_logs";
        const params = [];

        //adds filter parametres if called
        if (filterUser) params.push(`user_id=${encodeURIComponent(filterUser)}`);
        if (filterAction) params.push(`action=${encodeURIComponent(filterAction)}`);

        //if filter params, append to URL
        if (params.length > 0) {
            url += `?${params.join("&")}`;
        }

        try {
            //send request to backend
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            //convert answer to json
            const data = await response.json();
            setLogs(data);
        }
        catch (error) {
            console.error("Error fetching logs:", error);
        }
    };



    return (
        <div className="admin-logs">
            <h2>User Logs</h2>

            <div className="log-filters">
                <input
                    type="text"
                    placeholder="Filter by User ID"
                    value={filterUser}
                    onChange={(e) => setFilterUser(e.target.value)}
                />
                <select value={filterAction} onChange={(e) => setFilterAction(e.target.value)}>
                    <option value="">All Actions</option>
                    <option value="User registered">User registered</option>
                    <option value="User logged in">User logged in</option>
                    <option value="User logged out">User logged out</option>
                    <option value="User made a reservation">User made a reservation</option>
                </select>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Action</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.length > 0 ? (
                        logs.map((log) => (
                            <tr key={log.id}>
                                <td>{log.id}</td>
                                <td>{log.user}</td>
                                <td>{log.action}</td>
                                <td>{new Date(log.timestamp).toLocaleString()}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="4">No logs found</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}
