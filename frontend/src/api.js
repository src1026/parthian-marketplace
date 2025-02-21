const API_URL = "http://localhost:8001";

export const register = async (email, fullName, password) => {
    const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, full_name: fullName, password })
    });

    if (!response.ok) {
        throw new Error("Registration failed");
    }

    return response.json();
};
export const login = async (email, password) => {
    const response = await fetch("http://localhost:8001/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username: email, password: password }).toString(),
    });

    const data = await response.json();
    return data;
};
