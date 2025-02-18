import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "./AuthContext";
import { Pie, Bar } from "react-chartjs-2";
import { Chart, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";
import "./Statistics.css";

// Register chart components
Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function StatisticsPage() {
    // Get user details from AuthContext
    const {user} =useContext(AuthContext);
    const isAdmin = user ?.role === "Admin";

    // State variables for statistics selection and data
    const[selectedStat, setSelectedStat] = useState("occupancy");
    const[statsData, setStatsData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Fetch statistics when the selectedStat changes
    useEffect(() => {
        if(!isAdmin){
            return;
        }
        fetchStatistics(selectedStat);
    }, [selectedStat]);

    // Function to fetch statistics based on selected type
    const fetchStatistics = async (type) => {
        setLoading(true);
        setError(null);
        setStatsData(null);

        let apiUrl = "";
        if (type === "occupancy") apiUrl = "http://127.0.0.1:5000/api/hall_occupancy";
        else if (type === "revenue") apiUrl = "http://127.0.0.1:5000/api/monthly_revenue";
        else if (type === "bestsellers") apiUrl = "http://127.0.0.1:5000/api/bestseller_movies";

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setStatsData(data);
        } catch (error) {
            console.error("Error fetching statistics:", error);
            setError("Failed to load statistics.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="statistics-page">
            <h2>Admin Statistics</h2>
            <div className="stats-selection">
                <button onClick={() => setSelectedStat("occupancy")}>Hall Occupancy</button>
                <button onClick={() => setSelectedStat("revenue")}>Monthly Revenue</button>
                <button onClick={() => setSelectedStat("bestsellers")}>Bestseller Movies</button>
            </div>

            {loading && <p>Loading...</p>}
            {error && <p className="error-message">{error}</p>}

            {statsData && selectedStat === "occupancy" && (
                <div className="chart-container">
                    <h3>Hall Occupancy</h3>
                    <Bar
                        data={{
                            labels: statsData.map((row) => `${row.hall} (${row.showtime})`),
                            datasets: [
                                {
                                    label: "Occupancy Rate (%)",
                                    data: statsData.map((row) => row.occupancy_rate),
                                    backgroundColor: "#4CAF50",
                                },
                            ],
                        }}
                    />
                </div>
            )}

            {statsData && selectedStat === "revenue" && (
                <div className="chart-container">
                    <h3>Monthly Revenue</h3>
                    <Bar
                        data={{
                            labels: statsData.map((row) => row.month),
                            datasets: [
                                {
                                    label: "Revenue (€)",
                                    data: statsData.map((row) => row.revenue),
                                    backgroundColor: "#2196F3",
                                },
                            ],
                        }}
                    />
                </div>
            )}

            {statsData && selectedStat === "bestsellers" && (
                <div className="chart-container">
                    <h3>Bestseller Movies</h3>
                    <ul className="bestseller-list">
                        {statsData.map((movie, index) => (
                            <li key={index}>{movie.title} - {movie.count} Tickets sold</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}