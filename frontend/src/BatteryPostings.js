import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const BatteryPostings = () => {
  const [batteries, setBatteries] = useState([]);
  const [message, setMessage] = useState("");
  const [newBattery, setNewBattery] = useState({
    batteryId: "",
    capacity: "",
    voltage: "",
    state_of_health: "",
    cycle_count: "",
    chemistry_type: "",
    weight: "",
    price: "",
    location: ""
  });
  const navigate = useNavigate();

  // 当无过滤条件时，调用 GET /batteries 显示所有电池数据
  useEffect(() => {
    fetch("http://localhost:8002/batteries")
      .then((res) => res.json())
      .then((data) => {
        setBatteries(Array.isArray(data) ? data : []);
      })
      .catch((error) => {
        console.error("Error fetching batteries:", error);
        setBatteries([]);
      });
  }, []);

  // 处理表单输入变化
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewBattery((prev) => ({ ...prev, [name]: value }));
  };

  // 提交新电池数据到后端 battery_service（8002 端口）
  const handleCreateBattery = (e) => {
    e.preventDefault();
    fetch("http://localhost:8002/batteries", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newBattery)
    })
      .then((res) => res.json())
      .then((data) => {
        setMessage("✅ Battery created successfully!");
        // 可选：创建成功后更新电池列表
        setBatteries((prev) => [...prev, newBattery]);
        setNewBattery({
          batteryId: "",
          capacity: "",
          voltage: "",
          state_of_health: "",
          cycle_count: "",
          chemistry_type: "",
          weight: "",
          price: "",
          location: ""
        });
      })
      .catch(() => setMessage("❌ Error creating battery."));
  };

  // 添加电池到购物车（调用 user_service 的 /cart 接口，假设其在 8001 端口）
  const handleAddToCart = (batteryId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      setMessage("❌ You must log in before adding to cart.");
      setTimeout(() => navigate("/login"), 1500);
      return;
    }

    fetch("http://localhost:8001/cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ battery_id: batteryId })
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
      {message && (
        <p style={{ color: message.startsWith("✅") ? "green" : "red" }}>{message}</p>
      )}

      {/* 创建新电池表单 */}
      <form onSubmit={handleCreateBattery}>
        <h3>Create New Battery</h3>
        <input
          type="text"
          name="batteryId"
          placeholder="Battery ID"
          value={newBattery.batteryId}
          onChange={handleInputChange}
          required
        />
        <input
          type="number"
          name="capacity"
          placeholder="Capacity (kWh)"
          value={newBattery.capacity}
          onChange={handleInputChange}
          required
        />
        <input
          type="number"
          name="voltage"
          placeholder="Voltage (V)"
          value={newBattery.voltage}
          onChange={handleInputChange}
          required
        />
        <input
          type="number"
          name="state_of_health"
          placeholder="State of Health (%)"
          value={newBattery.state_of_health}
          onChange={handleInputChange}
          required
        />
        <input
          type="number"
          name="cycle_count"
          placeholder="Cycle Count"
          value={newBattery.cycle_count}
          onChange={handleInputChange}
          required
        />
        <input
          type="text"
          name="chemistry_type"
          placeholder="Chemistry Type"
          value={newBattery.chemistry_type}
          onChange={handleInputChange}
          required
        />
        <input
          type="number"
          name="weight"
          placeholder="Weight (kg)"
          value={newBattery.weight}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="price"
          placeholder="Price (USD)"
          value={newBattery.price}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="location"
          placeholder="Location"
          value={newBattery.location}
          onChange={handleInputChange}
        />
        <button type="submit">Post Battery</button>
      </form>

      {/* 电池列表 */}
      <h3>Available Batteries</h3>
      {batteries.length > 0 ? (
        <ul>
          {batteries.map((battery) => (
            <li key={battery.batteryId}>
              <strong>ID:</strong> {battery.batteryId} | <strong>Capacity:</strong> {battery.capacity} kWh |{" "}
              <strong>Voltage:</strong> {battery.voltage} V | <strong>Price:</strong> ${battery.price}
              <button onClick={() => handleAddToCart(battery.batteryId)}>
                🛒 Add to Cart
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No batteries available.</p>
      )}
    </div>
  );
};

export default BatteryPostings;
