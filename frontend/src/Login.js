import React, { useState } from "react";
import { login } from "./api";
import { useNavigate } from "react-router-dom";

const Login = ({ setToken }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");

        try {
            const response = await login(email, password);
            if (response.access_token) {
                localStorage.setItem("token", response.access_token);
                setToken(response.access_token);
                setMessage("✅ Login successful! Redirecting...");
                setTimeout(() => navigate("/"), 1000); // 登录后跳转
            } else {
                setMessage(response.detail || "❌ Login failed.");
            }
        } catch (error) {
            setMessage("❌ Error connecting to server.");
            console.error("Login error:", error);
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <h2>🔑 Login</h2>
            <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{ marginBottom: "10px", padding: "8px", width: "250px" }}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ marginBottom: "10px", padding: "8px", width: "250px" }}
                />
                <button type="submit" style={{ padding: "10px", width: "150px" }}>Login</button>
            </form>
            {message && <p style={{ marginTop: "15px", color: message.startsWith("✅") ? "green" : "red" }}>{message}</p>}
        </div>
    );
};

export default Login;

