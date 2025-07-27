// src/pages/Login.js
import React, { useState } from "react";
import { auth, provider, signInWithPopup } from "../firebase";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, provider);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="bg-white/10 p-10 rounded-xl shadow-lg text-white max-w-md w-full text-center">
        <h1 className="text-3xl font-bold mb-6">Sign in to GitHub Resume Generator</h1>

        {error && <p className="mb-4 text-red-400">{error}</p>}

        <button
          onClick={handleGoogleLogin}
          className="bg-blue-600 hover:bg-blue-700 py-3 px-6 rounded-lg transition"
        >
          Sign in with Google
        </button>
      </div>
    </div>
  );
};

export default Login;
