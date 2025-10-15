import { useState } from "react";
import { login } from "../api/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    try {
      const data = await login(email, username, password);
      localStorage.setItem("token", data.access_token);
      setMessage("Login successful!");
      window.location.href = "/dashboard";
    } catch (err: any) {
      setMessage("Invalid credentials");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <form
        onSubmit={handleLogin}
        className="bg-gray-800 p-8 rounded-2xl shadow-lg w-96 space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">Welcome Back</h2>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-3 rounded bg-gray-700"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Username"
          className="w-full p-3 rounded bg-gray-700"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-3 rounded bg-gray-700"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-green-500 hover:bg-green-400 py-2 rounded font-semibold"
        >
          Log In
        </button>
        <p className="text-center text-sm mt-2">
          Don’t have an account?{" "}
          <a href="/signup" className="text-green-400 underline">
            Sign up
          </a>
        </p>
        <p className="text-center text-xs mt-2 text-gray-400">{message}</p>
      </form>
    </div>
  );
}