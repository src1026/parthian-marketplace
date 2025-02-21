import React, { useState } from "react";
import { register } from "./api";
import { useNavigate } from "react-router-dom";

const Register = () => {
    const [email, setEmail] = useState("");
    const [fullName, setFullName] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await register(email, fullName, password);
        if (response.message) {
            setMessage("✅ Registration successful! Please check your email to verify.");
            setTimeout(() => navigate("/login"), 2000);
        } else {
            setMessage(response.detail || "❌ Registration failed.");
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <h2>📝 Register</h2>
            <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} required style={{ marginBottom: "10px", padding: "8px", width: "250px" }} />
                <input type="text" placeholder="Full Name" onChange={(e) => setFullName(e.target.value)} required style={{ marginBottom: "10px", padding: "8px", width: "250px" }} />
                <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} required style={{ marginBottom: "10px", padding: "8px", width: "250px" }} />
                <button type="submit" style={{ padding: "10px", width: "150px" }}>Register</button>
            </form>
            {message && <p style={{ marginTop: "15px", color: message.startsWith("✅") ? "green" : "red" }}>{message}</p>}
        </div>
    );
};

export default Register;
