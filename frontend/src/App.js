import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import BatteryPostings from "./BatteryPostings";
import Login from "./Login";
import Register from "./Register";

const App = () => {
    const [token, setToken] = useState(localStorage.getItem("token"));

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        if (storedToken) {
            setToken(storedToken);
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("token");
        setToken(null);
    };

    return (
        <Router>
            <div style={{ padding: "10px", textAlign: "right" }}>
                {token ? (
                    <>
                        <span>✅ Logged in</span>
                        <button onClick={handleLogout} style={{ marginLeft: "10px" }}>Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/login"><button>Login</button></Link>
                        <Link to="/register" style={{ marginLeft: "10px" }}><button>Register</button></Link>
                    </>
                )}
            </div>

            <Routes>
                <Route path="/" element={<BatteryPostings />} />
                <Route path="/login" element={<Login setToken={setToken} />} />
                <Route path="/register" element={<Register />} />
            </Routes>
        </Router>
    );
};

export default App;
