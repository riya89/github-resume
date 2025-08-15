import React, { useState, useEffect } from "react";
import {
  auth,
  signOut,
  getIdToken,
  db,
  collection,
  addDoc,
  query,
  where,
  getDocs,
  orderBy,
  serverTimestamp,
} from "../firebase";

import {
  Github,
  Sparkles,
  Copy,
  Download,
  Star,
  GitFork,
  Clock,
  GitBranch,
  Trash2,
  RefreshCw,
  TrendingUp,
  Code,
  Database,
  AlertCircle,
} from "lucide-react";

const Dashboard = ({ user }) => {
  const [formData, setFormData] = useState({
    github_url: "",
    num_points: 5,
    technical_level: "medium",
    output_tone: "action-oriented",
    generate_technical: true,
    branch: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [branches, setBranches] = useState([]);
  const [loadingBranches, setLoadingBranches] = useState(false);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [deletingItems, setDeletingItems] = useState(new Set());

  // Load history from Firestore on mount
  useEffect(() => {
    if (!user) return;
    fetchHistory();
  }, [user]);

  const fetchHistory = async () => {
    if (!user) return;
    
    setHistoryLoading(true);
    try {
      const token = await getIdToken(user);
      const response = await fetch('https://github-resume.onrender.com/history', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setHistory(data.history || []);
        console.log("History loaded:", data.history?.length || 0, "items");
      } else {
        console.error("Failed to fetch history:", response.status);
        // Fallback to Firestore direct query
        await fetchHistoryFromFirestore();
      }
    } catch (err) {
      console.error("Failed to fetch history from API:", err);
      // Fallback to Firestore direct query
      await fetchHistoryFromFirestore();
    } finally {
      setHistoryLoading(false);
    }
  };

  const fetchHistoryFromFirestore = async () => {
    try {
      const historyQuery = query(
        collection(db, "repo_histories"),
        where("uid", "==", user.uid),
        orderBy("timestamp", "desc")
      );
      const snapshot = await getDocs(historyQuery);
      const histories = [];
      snapshot.forEach((doc) => {
        histories.push({ id: doc.id, ...doc.data() });
      });
      setHistory(histories);
    } catch (err) {
      console.error("Failed to fetch history from Firestore:", err);
      setError("Failed to load history. Please try refreshing the page.");
    }
  };

  const deleteHistoryItem = async (itemId, itemName) => {
    if (!window.confirm(`Are you sure you want to delete "${itemName}"?`)) {
      return;
    }

    setDeletingItems(prev => new Set([...prev, itemId]));
    
    try {
      const token = await getIdToken(user);
      const response = await fetch(`https://github-resume.onrender.com/history/${itemId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setHistory(prev => prev.filter(item => item.id !== itemId));
        console.log("Successfully deleted history item:", itemId);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete item');
      }
    } catch (err) {
      console.error("Error deleting history item:", err);
      setError(`Failed to delete item: ${err.message}`);
    } finally {
      setDeletingItems(prev => {
        const newSet = new Set(prev);
        newSet.delete(itemId);
        return newSet;
      });
    }
  };

  const clearAllHistory = async () => {
    if (!window.confirm("Are you sure you want to delete ALL your history? This action cannot be undone.")) {
      return;
    }

    setHistoryLoading(true);
    try {
      const token = await getIdToken(user);
      const response = await fetch('https://github-resume.onrender.com/history/clear', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setHistory([]);
        console.log("Successfully cleared all history:", data.deleted_count);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to clear history');
      }
    } catch (err) {
      console.error("Error clearing history:", err);
      setError(`Failed to clear history: ${err.message}`);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleLogout = async () => {
    await signOut(auth);
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const fetchBranches = async (githubUrl) => {
    if (!githubUrl) return;
    
    try {
      const urlParts = githubUrl.split("/").filter(Boolean);
      if (urlParts.length < 2) return;

      const owner = urlParts[urlParts.length - 2];
      const repo = urlParts[urlParts.length - 1];

      setLoadingBranches(true);
      const token = await getIdToken(user);
      const response = await fetch(
        `https://github-resume.onrender.com/get-branches/${owner}/${repo}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setBranches(data.branches || []);
        setFormData((prev) => ({ ...prev, branch: "" }));
        console.log("Branches loaded:", data.branches?.length || 0);
      } else {
        setBranches([]);
        console.error("Failed to fetch branches:", response.status);
      }
    } catch (err) {
      console.error("Error fetching branches:", err);
      setBranches([]);
    } finally {
      setLoadingBranches(false);
    }
  };

  const handleUrlBlur = () => {
    if (formData.github_url) {
      fetchBranches(formData.github_url);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const token = await getIdToken(user);

      let requestData = {
        ...formData,
        num_points: parseInt(formData.num_points, 10),
      };

      if (!requestData.branch) {
        delete requestData.branch;
      }

      console.log("Submitting request:", requestData);

      const response = await fetch("https://github-resume.onrender.com/generate-resume-points", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error || errorData.detail || "Failed to generate resume points"
        );
      }

      const data = await response.json();
      console.log("Resume points generated:", data);
      setResult(data);

      // Save this request to history (Firestore)
      try {
        await addDoc(collection(db, "repo_histories"), {
          uid: user.uid,
          userEmail: user.email,
          github_url: formData.github_url,
          branch: formData.branch || null,
          points: data.points,
          repository_info: data.repository_info,
          analysis_details: data.analysis_details || {},
          user_settings: data.user_settings || {},
          timestamp: serverTimestamp(),
        });

        // Refresh history
        fetchHistory();
      } catch (saveError) {
        console.error("Failed to save to history:", saveError);
        setError("Resume generated successfully, but failed to save to history.");
      }

    } catch (err) {
      console.error("Submit error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      console.log("Copied to clipboard");
    }).catch(err => {
      console.error("Failed to copy:", err);
    });
  };

  const downloadAsText = () => {
    if (!result) return;
    
    try {
      const content = result.points.join("\n");
      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume-points-${result.repository_info.name || 'export'}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download failed:", err);
      setError("Failed to download file");
    }
  };

  const loadHistoryEntry = (entry) => {
    console.log("Loading history entry:", entry);
    
    setResult({
      points: entry.points,
      repository_info: entry.repository_info,
      analysis_details: entry.analysis_details || {},
      processing_time: entry.timestamp
        ? entry.timestamp instanceof Date 
          ? entry.timestamp.toLocaleString()
          : new Date(entry.timestamp.seconds * 1000).toLocaleString()
        : "N/A",
    });
    
    // Populate form with historical data
    if (entry.github_url) {
      setFormData(prev => ({
        ...prev,
        github_url: entry.github_url,
        branch: entry.branch || "",
        num_points: entry.user_settings?.num_points || prev.num_points,
        technical_level: entry.user_settings?.technical_level || prev.technical_level,
        output_tone: entry.user_settings?.output_tone || prev.output_tone,
      }));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8 max-w-7xl grid grid-cols-1 lg:grid-cols-4 gap-6">

        {/* Enhanced Sidebar with Delete Functionality */}
        <aside className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-lg border border-white/20 max-h-[85vh] overflow-y-auto text-white">
          {/* User Info */}
          <div className="flex flex-col items-center mb-6">
            <div className="bg-purple-600 rounded-full h-16 w-16 flex items-center justify-center text-xl font-bold text-white mb-3">
              {user.displayName ? user.displayName[0] : "U"}
            </div>
            <h2 className="text-xl font-semibold text-center">
              {user.displayName || "User"}
            </h2>
            <p className="text-sm text-gray-300 text-center mt-1">
              {user.email}
            </p>
            <button
              onClick={handleLogout}
              className="mt-4 bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-white w-full transition duration-200"
            >
              Logout
            </button>
          </div>

          {/* History Header with Actions */}
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-bold text-lg">Previous Repos</h3>
            <div className="flex space-x-2">
              <button
                onClick={fetchHistory}
                disabled={historyLoading}
                className="p-1 hover:bg-white/20 rounded transition duration-200"
                title="Refresh history"
              >
                <RefreshCw className={`w-4 h-4 ${historyLoading ? 'animate-spin' : ''}`} />
              </button>
              {history.length > 0 && (
                <button
                  onClick={clearAllHistory}
                  className="p-1 hover:bg-red-500/30 rounded transition duration-200"
                  title="Clear all history"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>
          
          {/* History Loading State */}
          {historyLoading && (
            <div className="flex items-center justify-center py-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
              <span className="ml-2 text-sm">Loading history...</span>
            </div>
          )}
          
          {/* Empty History State */}
          {!historyLoading && history.length === 0 && (
            <div className="text-center py-8">
              <Github className="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-300 text-sm">No history yet</p>
              <p className="text-gray-400 text-xs mt-1">Generate your first resume points!</p>
            </div>
          )}
          
          {/* History List */}
          <ul className="space-y-3 max-h-[50vh] overflow-y-auto">
            {history.map((entry, idx) => (
              <li
                key={entry.id || idx}
                className="relative group bg-white/5 rounded-lg p-3 border border-white/10 hover:bg-white/10 transition duration-200"
              >
                <div 
                  onClick={() => loadHistoryEntry(entry)}
                  className="cursor-pointer"
                  title={entry.github_url}
                >
                  <div className="font-semibold truncate text-sm mb-2">
                    {entry.repository_info?.name || entry.github_url?.split('/').pop() || 'Unknown Repo'}
                  </div>
                  
                  <div className="text-xs text-gray-400 space-y-1">
                    <div className="flex items-center">
                      <GitBranch className="w-3 h-3 mr-1" />
                      {entry.branch || "Auto-detected"}
                    </div>
                    
                    <div className="flex items-center">
                      <Code className="w-3 h-3 mr-1" />
                      {entry.repository_info?.language || "Multiple"}
                    </div>
                    
                    <div className="flex items-center">
                      <Clock className="w-3 h-3 mr-1" />
                      {entry.timestamp
                        ? entry.timestamp instanceof Date 
                          ? entry.timestamp.toLocaleDateString()
                          : new Date(entry.timestamp.seconds * 1000).toLocaleDateString()
                        : "N/A"}
                    </div>
                    
                    {entry.analysis_details?.technologies_detected?.length > 0 && (
                      <div className="flex items-center">
                        <Database className="w-3 h-3 mr-1" />
                        {entry.analysis_details.technologies_detected.slice(0, 2).join(', ')}
                        {entry.analysis_details.technologies_detected.length > 2 && '...'}
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Delete Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteHistoryItem(entry.id, entry.repository_info?.name || 'this item');
                  }}
                  disabled={deletingItems.has(entry.id)}
                  className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/30 rounded transition duration-200"
                  title="Delete this item"
                >
                  {deletingItems.has(entry.id) ? (
                    <RefreshCw className="w-3 h-3 animate-spin" />
                  ) : (
                    <Trash2 className="w-3 h-3" />
                  )}
                </button>
              </li>
            ))}
          </ul>
        </aside>

        {/* Main Content - Enhanced */}
        <main className="lg:col-span-3 bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20 max-h-[85vh] overflow-y-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Github className="text-white mr-3" size={40} />
              <Sparkles className="text-yellow-400 ml-2" size={32} />
            </div>
            <h1 className="text-4xl font-bold text-white mb-2">
              GitHub Resume Points Generator
            </h1>
            <p className="text-gray-300 text-lg">
              Transform your GitHub repositories into professional resume bullet points with smart branch detection and comprehensive code analysis
            </p>
          </div>

          {/* Form - Same as before but with enhanced styling */}
          <div className="space-y-6">
            {/* GitHub URL Input */}
            <div>
              <label className="block text-white text-sm font-semibold mb-2">
                GitHub Repository URL
              </label>
              <div className="relative">
                <Github className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type="url"
                  name="github_url"
                  value={formData.github_url}
                  onChange={handleInputChange}
                  onBlur={handleUrlBlur}
                  placeholder="https://github.com/username/repository"
                  className="w-full pl-12 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>
              {loadingBranches && (
                <p className="text-sm text-gray-400 mt-1 flex items-center">
                  <RefreshCw className="w-4 h-4 animate-spin mr-1" />
                  Loading branches...
                </p>
              )}
            </div>

            {/* Branch Selection */}
            {branches.length > 0 && (
              <div>
                <label className="block text-white text-sm font-semibold mb-2 flex items-center">
                  <GitBranch className="mr-2" size={16} />
                  Branch Selection ({branches.length} available)
                </label>
                <select
                  name="branch"
                  value={formData.branch}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">🤖 Auto-detect best branch</option>
                  {branches.map((branch) => (
                    <option key={branch} value={branch} className="bg-gray-800">
                      📁 {branch}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-gray-400 mt-1">
                  Auto-detection analyzes code complexity and selects the most suitable branch
                </p>
              </div>
            )}

            {/* Settings Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  Number of Points
                </label>
                <input
                  type="number"
                  name="num_points"
                  value={formData.num_points}
                  onChange={handleInputChange}
                  min="1"
                  max="10"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  Technical Level
                </label>
                <select
                  name="technical_level"
                  value={formData.technical_level}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="basic" className="bg-gray-800">📝 Basic - Simple, clear language</option>
                  <option value="medium" className="bg-gray-800">⚖️ Medium - Balanced technical depth</option>
                  <option value="advanced" className="bg-gray-800">🚀 Advanced - Industry terminology</option>
                </select>
              </div>

              <div>
                <label className="block text-white text-sm font-semibold mb-2">
                  Output Tone
                </label>
                <select
                  name="output_tone"
                  value={formData.output_tone}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="concise" className="bg-gray-800">✂️ Concise - Brief, impactful</option>
                  <option value="detailed" className="bg-gray-800">📖 Detailed - Comprehensive explanations</option>
                  <option value="action-oriented" className="bg-gray-800">💪 Action-Oriented - Strong verbs, achievements</option>
                </select>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  name="generate_technical"
                  checked={formData.generate_technical}
                  onChange={handleInputChange}
                  className="w-5 h-5 text-purple-600 bg-white/10 border-white/20 rounded focus:ring-purple-500"
                />
                <label className="ml-3 text-white text-sm font-semibold">
                  🔬 Enhanced Technical Analysis
                </label>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading || !formData.github_url}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-lg transition duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-transparent"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Analyzing Repository & Generating Enhanced Points...
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <Sparkles className="mr-2" size={20} />
                  Generate Enhanced Resume Points
                </div>
              )}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg flex items-start">
              <AlertCircle className="w-5 h-5 text-red-400 mr-3 mt-0.5 flex-shrink-0" />
              <div className="flex-1">
                <p className="text-red-200 text-sm">{error}</p>
                <button 
                  onClick={() => setError("")}
                  className="mt-2 text-xs text-red-300 hover:text-red-100 underline"
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}

          {/* Enhanced Results Display */}
          {result && (
            <div className="mt-8 space-y-6">
              {/* Repository Info with Tech Stack */}
              <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                  <Github className="mr-2" size={24} />
                  {result.repository_info.name}
                </h3>
                <p className="text-gray-300 mb-4">{result.repository_info.description}</p>
                
                {/* Enhanced Stats */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm text-gray-400 mb-4">
                  <div className="flex items-center">
                    <Star className="mr-1" size={16} />
                    {result.repository_info.stars} stars
                  </div>
                  <div className="flex items-center">
                    <GitFork className="mr-1" size={16} />
                    {result.repository_info.forks} forks
                  </div>
                  <div className="flex items-center">
                    <Clock className="mr-1" size={16} />
                    {result.processing_time || "N/A"}
                  </div>
                  <div className="flex items-center">
                    <GitBranch className="mr-1" size={16} />
                    {result.repository_info.branch_used || "main"}
                  </div>
                  <div className="flex items-center">
                    <Database className="mr-1" size={16} />
                    {result.repository_info.size ? `${Math.round(result.repository_info.size / 1024)}MB` : "N/A"}
                  </div>
                </div>

                {/* Language and Tech Stack */}
                <div className="flex flex-wrap gap-2 mb-4">
                  <div className="bg-purple-600 px-3 py-1 rounded-full text-white text-xs font-semibold">
                    📝 {result.repository_info.language || "Multiple"}
                  </div>
                  {result.analysis_details?.technologies_detected?.slice(0, 5).map((tech, idx) => (
                    <div key={idx} className="bg-blue-500/30 px-2 py-1 rounded text-blue-200 text-xs">
                      {tech}
                    </div>
                  ))}
                  {result.analysis_details?.technologies_detected?.length > 5 && (
                    <div className="bg-gray-500/30 px-2 py-1 rounded text-gray-300 text-xs">
                      +{result.analysis_details.technologies_detected.length - 5} more
                    </div>
                  )}
                </div>

                {/* Analysis Summary */}
                {result.analysis_details && (
                  <div className="bg-blue-500/20 rounded-lg p-3 border border-blue-500/30">
                    <h4 className="text-blue-200 text-sm font-semibold mb-2 flex items-center">
                      <TrendingUp className="mr-1" size={14} />
                      Analysis Summary
                    </h4>
                    <div className="text-blue-200 text-xs space-y-1">
                      <div>🔍 Files Analyzed: {result.analysis_details.total_files_analyzed || 0}</div>
                      <div>🛠️ Technologies: {result.analysis_details.technologies_detected?.length || 0}</div>
                      <div>💻 Primary Language: {result.analysis_details.primary_language || "Not detected"}</div>
                      {result.repository_info.available_branches?.length > 1 && (
                        <div>🌿 Branches Available: {result.repository_info.available_branches.length}</div>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Enhanced Resume Points */}
              <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white flex items-center">
                    <Sparkles className="mr-2" size={20} />
                    Enhanced Resume Points
                  </h3>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => copyToClipboard(result.points.join("\n"))}
                      className="flex items-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition duration-200"
                    >
                      <Copy className="mr-1" size={16} />
                      Copy All
                    </button>
                    <button
                      onClick={downloadAsText}
                      className="flex items-center px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition duration-200"
                    >
                      <Download className="mr-1" size={16} />
                      Download
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  {result.points.map((point, idx) => (
                    <div
                      key={idx}
                      className="flex items-start space-x-4 p-4 bg-white/5 rounded-lg border border-white/10 group hover:bg-white/10 transition duration-200"
                    >
                      <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        {idx + 1}
                      </div>
                      <div className="flex-1">
                        <p className="text-gray-200 leading-relaxed text-base">{point}</p>
                      </div>
                      <button
                        onClick={() => copyToClipboard(point)}
                        className="opacity-0 group-hover:opacity-100 transition duration-200 p-2 hover:bg-white/10 rounded-lg"
                        title="Copy this point"
                      >
                        <Copy className="text-gray-400 hover:text-white" size={16} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pro Tips */}
              <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg p-6 border border-blue-500/30">
                <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
                  <Sparkles className="mr-2" size={18} />
                  💡 Pro Tips for Using These Points
                </h4>
                <div className="grid md:grid-cols-2 gap-4 text-gray-300 text-sm">
                  <ul className="space-y-2">
                    <li>• <strong>Customize:</strong> Tailor each point to match specific job requirements</li>
                    <li>• <strong>Quantify:</strong> Add metrics where possible (e.g., "improved performance by 30%")</li>
                    <li>• <strong>Context:</strong> Expand with your specific contributions and outcomes</li>
                  </ul>
                  <ul className="space-y-2">
                    <li>• <strong>Keywords:</strong> Match technical terminology to job descriptions</li>
                    <li>• <strong>Impact:</strong> Focus on business value and technical achievements</li>
                    <li>• <strong>Audience:</strong> Adjust complexity based on who's reading (HR vs. Tech)</li>
                  </ul>
                </div>
              </div>

              {/* Generation Settings Summary */}
              {result.user_settings && (
                <div className="bg-gray-500/20 rounded-lg p-4 border border-gray-500/30">
                  <h4 className="text-gray-200 text-sm font-semibold mb-2">⚙️ Generation Settings Used</h4>
                  <div className="flex flex-wrap gap-3 text-xs text-gray-300">
                    <span className="bg-gray-600/30 px-2 py-1 rounded">
                      📊 Points: {result.user_settings.num_points}
                    </span>
                    <span className="bg-gray-600/30 px-2 py-1 rounded">
                      🎯 Level: {result.user_settings.technical_level}
                    </span>
                    <span className="bg-gray-600/30 px-2 py-1 rounded">
                      ✍️ Tone: {result.user_settings.output_tone}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;