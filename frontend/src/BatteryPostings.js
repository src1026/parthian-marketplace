import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const BatteryPostings = () => {
    const [batteries, setBatteries] = useState([]);
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://localhost:8001/batteries")
            .then((res) => res.json())
            .then((data) => {
                setBatteries(Array.isArray(data) ? data : []);
            })
            .catch((error) => {
                console.error("Error fetching batteries:", error);
                setBatteries([]);
            });
    }, []);

    const handleAddToCart = (batteryId) => {
        const token = localStorage.getItem("token");

        if (!token) {
            setMessage("❌ You must log in before adding to cart.");
            setTimeout(() => navigate("/login"), 1500);
            return;
        }

        fetch(`http://localhost:8001/cart`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ battery_id: batteryId }),
        })
            .then((res) => res.json())
            .then((data) => {
                setMessage(data.success ? "✅ Battery added to cart!" : "❌ Failed to add to cart.");
            })
            .catch(() => setMessage("❌ Error adding to cart."));
    };

    return (
        <div>
            <h2>🔋 Battery Postings</h2>
            {message && <p style={{ color: message.startsWith("✅") ? "green" : "red" }}>{message}</p>}
            <ul>
                {batteries.length > 0 ? batteries.map((battery) => (
                    <li key={battery.id}>
                        {battery.name} - ${battery.price}
                        <button onClick={() => handleAddToCart(battery.id)}>🛒 Add to Cart</button>
                    </li>
                )) : <p>No batteries available.</p>}
            </ul>
        </div>
    );
};

export default BatteryPostings;
