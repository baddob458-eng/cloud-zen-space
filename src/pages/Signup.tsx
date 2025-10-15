import { useState } from "react";
import { signup } from "../api/auth";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    try {
      const data = await signup(email, username, password);
      localStorage.setItem("token", data.access_token);
      setMessage("Signup successful! You’re in.");
      window.location.href = "/dashboard";
    } catch (err: any) {
      setMessage(err.message || "Signup failed");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <form
        onSubmit={handleSignup}
        className="bg-gray-800 p-8 rounded-2xl shadow-lg w-96 space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">Create Account</h2>
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
          Sign Up
        </button>
        <p className="text-center text-sm mt-2">
          Already have an account?{" "}
          <a href="/login" className="text-green-400 underline">
            Log in
          </a>
        </p>
        <p className="text-center text-xs mt-2 text-gray-400">{message}</p>
      </form>
    </div>
  );
}