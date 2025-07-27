// import React, { useState } from 'react';
// import { Github, Sparkles, Copy, Download, Settings, Star, GitFork, Clock } from 'lucide-react';

// const App = () => {
//   const [formData, setFormData] = useState({
//     github_url: '',
//     num_points: 5,
//     technical_level: 'medium',
//     output_tone: 'action-oriented',
//     generate_technical: true
//   });
  
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState('');

//   const handleInputChange = (e) => {
//     const { name, value, type, checked } = e.target;
//     setFormData(prev => ({
//       ...prev,
//       [name]: type === 'checkbox' ? checked : value
//     }));
//   };

//   const handleSubmit = async () => {
//     setLoading(true);
//     setError('');
//     setResult(null);

//     try {
//       const response = await fetch('http://localhost:8000/generate-resume-points', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           ...formData,
//           num_points: parseInt(formData.num_points)
//         }),
//       });

//       if (!response.ok) {
//         const errorData = await response.json();
//         throw new Error(errorData.detail || 'Failed to generate resume points');
//       }

//       const data = await response.json();
//       setResult(data);
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const copyToClipboard = (text) => {
//     navigator.clipboard.writeText(text);
//   };

//   const downloadAsText = () => {
//     if (!result) return;
    
//     const content = result.points.join('\n');
//     const blob = new Blob([content], { type: 'text/plain' });
//     const url = URL.createObjectURL(blob);
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = `resume-points-${result.repository_info.name}.txt`;
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     URL.revokeObjectURL(url);
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
//       <div className="container mx-auto px-4 py-8 max-w-4xl">
//         {/* Header */}
//         <div className="text-center mb-8">
//           <div className="flex items-center justify-center mb-4">
//             <Github className="text-white mr-3" size={40} />
//             <Sparkles className="text-yellow-400 ml-2" size={32} />
//           </div>
//           <h1 className="text-4xl font-bold text-white mb-2">
//             GitHub Resume Points Generator
//           </h1>
//           <p className="text-gray-300 text-lg">
//             Transform your GitHub repositories into professional resume bullet points
//           </p>
//         </div>

//         {/* Main Form */}
//         <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
//           <div className="space-y-6">
//             {/* GitHub URL Input */}
//             <div>
//               <label className="block text-white text-sm font-semibold mb-2">
//                 GitHub Repository URL
//               </label>
//               <div className="relative">
//                 <Github className="absolute left-3 top-3 text-gray-400" size={20} />
//                 <input
//                   type="url"
//                   name="github_url"
//                   value={formData.github_url}
//                   onChange={handleInputChange}
//                   placeholder="https://github.com/username/repository"
//                   className="w-full pl-12 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
//                   required
//                 />
//               </div>
//             </div>

//             {/* Settings Grid */}
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//               {/* Number of Points */}
//               <div>
//                 <label className="block text-white text-sm font-semibold mb-2">
//                   Number of Points
//                 </label>
//                 <input
//                   type="number"
//                   name="num_points"
//                   value={formData.num_points}
//                   onChange={handleInputChange}
//                   min="1"
//                   max="10"
//                   className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
//                 />
//               </div>

//               {/* Technical Level */}
//               <div>
//                 <label className="block text-white text-sm font-semibold mb-2">
//                   Technical Level
//                 </label>
//                 <select
//                   name="technical_level"
//                   value={formData.technical_level}
//                   onChange={handleInputChange}
//                   className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
//                 >
//                   <option value="basic" className="bg-gray-800">Basic</option>
//                   <option value="medium" className="bg-gray-800">Medium</option>
//                   <option value="advanced" className="bg-gray-800">Advanced</option>
//                 </select>
//               </div>

//               {/* Output Tone */}
//               <div>
//                 <label className="block text-white text-sm font-semibold mb-2">
//                   Output Tone
//                 </label>
//                 <select
//                   name="output_tone"
//                   value={formData.output_tone}
//                   onChange={handleInputChange}
//                   className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
//                 >
//                   <option value="concise" className="bg-gray-800">Concise</option>
//                   <option value="detailed" className="bg-gray-800">Detailed</option>
//                   <option value="action-oriented" className="bg-gray-800">Action-Oriented</option>
//                 </select>
//               </div>

//               {/* Generate Technical */}
//               <div className="flex items-center">
//                 <input
//                   type="checkbox"
//                   name="generate_technical"
//                   checked={formData.generate_technical}
//                   onChange={handleInputChange}
//                   className="w-5 h-5 text-purple-600 bg-white/10 border-white/20 rounded focus:ring-purple-500"
//                 />
//                 <label className="ml-3 text-white text-sm font-semibold">
//                   Focus on Technical Details
//                 </label>
//               </div>
//             </div>

//             {/* Submit Button */}
//             <button
//               type="button"
//               onClick={handleSubmit}
//               disabled={loading}
//               className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-lg transition duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-transparent"
//             >
//               {loading ? (
//                 <div className="flex items-center justify-center">
//                   <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
//                   Generating Resume Points...
//                 </div>
//               ) : (
//                 <div className="flex items-center justify-center">
//                   <Sparkles className="mr-2" size={20} />
//                   Generate Resume Points
//                 </div>
//               )}
//             </button>
//           </div>

//           {/* Error Display */}
//           {error && (
//             <div className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg">
//               <p className="text-red-200 text-sm">{error}</p>
//             </div>
//           )}

//           {/* Results */}
//           {result && (
//             <div className="mt-8 space-y-6">
//               {/* Repository Info */}
//               <div className="bg-white/5 rounded-lg p-6 border border-white/10">
//                 <h3 className="text-xl font-bold text-white mb-4 flex items-center">
//                   <Github className="mr-2" size={24} />
//                   {result.repository_info.name}
//                 </h3>
//                 <p className="text-gray-300 mb-4">{result.repository_info.description}</p>
//                 <div className="flex items-center space-x-6 text-sm text-gray-400">
//                   <div className="flex items-center">
//                     <Star className="mr-1" size={16} />
//                     {result.repository_info.stars} stars
//                   </div>
//                   <div className="flex items-center">
//                     <GitFork className="mr-1" size={16} />
//                     {result.repository_info.forks} forks
//                   </div>
//                   <div className="flex items-center">
//                     <Clock className="mr-1" size={16} />
//                     {result.processing_time}
//                   </div>
//                   <div className="bg-purple-600 px-2 py-1 rounded text-white text-xs">
//                     {result.repository_info.language}
//                   </div>
//                 </div>
//               </div>

//               {/* Resume Points */}
//               <div className="bg-white/5 rounded-lg p-6 border border-white/10">
//                 <div className="flex items-center justify-between mb-4">
//                   <h3 className="text-xl font-bold text-white">Resume Points</h3>
//                   <div className="flex space-x-2">
//                     <button
//                       onClick={() => copyToClipboard(result.points.join('\n'))}
//                       className="flex items-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition duration-200"
//                     >
//                       <Copy className="mr-1" size={16} />
//                       Copy All
//                     </button>
//                     <button
//                       onClick={downloadAsText}
//                       className="flex items-center px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition duration-200"
//                     >
//                       <Download className="mr-1" size={16} />
//                       Download
//                     </button>
//                   </div>
//                 </div>
                
//                 <div className="space-y-3">
//                   {result.points.map((point, index) => (
//                     <div
//                       key={index}
//                       className="flex items-start space-x-3 p-3 bg-white/5 rounded-lg border border-white/10 group hover:bg-white/10 transition duration-200"
//                     >
//                       <div className="flex-shrink-0 w-6 h-6 bg-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
//                         {index + 1}
//                       </div>
//                       <p className="text-gray-200 flex-1 leading-relaxed">{point}</p>
//                       <button
//                         onClick={() => copyToClipboard(point)}
//                         className="opacity-0 group-hover:opacity-100 transition duration-200 p-1 hover:bg-white/10 rounded"
//                       >
//                         <Copy className="text-gray-400 hover:text-white" size={16} />
//                       </button>
//                     </div>
//                   ))}
//                 </div>
//               </div>
//             </div>
//           )}
//         </div>

//         {/* Footer */}
//         <div className="text-center mt-8 text-gray-400">
//           <p>Powered by Gemini 2.0 Flash • Built with FastAPI & React</p>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default App;
import React, { useState } from 'react';
import {
  Github,
  Sparkles,
  Copy,
  Download,
  Star,
  GitFork,
  Clock,
  GitBranch,
} from 'lucide-react';

const App = () => {
  const [formData, setFormData] = useState({
    github_url: '',
    num_points: 5,
    technical_level: 'medium',
    output_tone: 'action-oriented',
    generate_technical: true,
    branch: '',
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [branches, setBranches] = useState([]);
  const [loadingBranches, setLoadingBranches] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const fetchBranches = async (githubUrl) => {
    if (!githubUrl) return;

    try {
      // Extract owner/repo from URL
      const urlParts = githubUrl.split('/').filter(Boolean);
      if (urlParts.length < 2) return;

      const owner = urlParts[urlParts.length - 2];
      const repo = urlParts[urlParts.length - 1];

      setLoadingBranches(true);
      const response = await fetch(
        `http://localhost:8000/get-branches/${owner}/${repo}`
      );

      if (response.ok) {
        const data = await response.json();
        setBranches(data.branches || []);
        // Optionally reset the selected branch when branches change
        setFormData((prev) => ({ ...prev, branch: '' }));
      } else {
        setBranches([]);
      }
    } catch (err) {
      console.error('Failed to fetch branches:', err);
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
    setError('');
    setResult(null);

    try {
      const requestData = {
        ...formData,
        num_points: parseInt(formData.num_points, 10),
      };

      // Remove empty branch field to let backend auto-detect
      if (!requestData.branch) {
        delete requestData.branch;
      }

      const response = await fetch(
        'http://localhost:8000/generate-resume-points',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error || errorData.detail || 'Failed to generate resume points'
        );
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const downloadAsText = () => {
    if (!result) return;

    const content = result.points.join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resume-points-${result.repository_info.name}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
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
            Transform your GitHub repositories into professional resume bullet points with smart branch detection
          </p>
        </div>

        {/* Main Form */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
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
                <p className="text-sm text-gray-400 mt-1">Loading branches...</p>
              )}
            </div>

            {/* Branch Selection */}
            {branches.length > 0 && (
              <div>
                <label className="block text-white text-sm font-semibold mb-2 flex items-center">
                  <GitBranch className="mr-2" size={16} />
                  Branch (Optional - auto-detects best branch if empty)
                </label>
                <select
                  name="branch"
                  value={formData.branch}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">Auto-detect best branch</option>
                  {branches.map((branch) => (
                    <option key={branch} value={branch} className="bg-gray-800">
                      {branch}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Settings Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Number of Points */}
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

              {/* Technical Level */}
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
                  <option value="basic" className="bg-gray-800">Basic</option>
                  <option value="medium" className="bg-gray-800">Medium</option>
                  <option value="advanced" className="bg-gray-800">Advanced</option>
                </select>
              </div>

              {/* Output Tone */}
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
                  <option value="concise" className="bg-gray-800">Concise</option>
                  <option value="detailed" className="bg-gray-800">Detailed</option>
                  <option value="action-oriented" className="bg-gray-800">Action-Oriented</option>
                </select>
              </div>

              {/* Generate Technical */}
              <div className="flex items-center">
                <input
                  type="checkbox"
                  name="generate_technical"
                  checked={formData.generate_technical}
                  onChange={handleInputChange}
                  className="w-5 h-5 text-purple-600 bg-white/10 border-white/20 rounded focus:ring-purple-500"
                />
                <label className="ml-3 text-white text-sm font-semibold">
                  Focus on Technical Details
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
                  Analyzing Repository & Generating Points...
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
            <div className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg">
              <p className="text-red-200 text-sm">{error}</p>
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="mt-8 space-y-6">
              {/* Repository Info */}
              <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                  <Github className="mr-2" size={24} />
                  {result.repository_info.name}
                </h3>
                <p className="text-gray-300 mb-4">{result.repository_info.description}</p>
                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400">
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
                    {result.processing_time}
                  </div>
                  <div className="flex items-center">
                    <GitBranch className="mr-1" size={16} />
                    {result.repository_info.branch_used || 'main'}
                  </div>
                  <div className="bg-purple-600 px-2 py-1 rounded text-white text-xs">
                    {result.repository_info.language}
                  </div>
                </div>

                {result.repository_info.available_branches && result.repository_info.available_branches.length > 1 && (
                  <div className="mt-3 p-3 bg-blue-500/20 rounded-lg border border-blue-500/30">
                    <p className="text-blue-200 text-sm">
                      <GitBranch className="inline mr-1" size={14} />
                      Repository has {result.repository_info.available_branches.length} branches: {result.repository_info.available_branches.join(', ')}
                    </p>
                  </div>
                )}
              </div>

              {/* Resume Points */}
              <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white">Enhanced Resume Points</h3>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => copyToClipboard(result.points.join('\n'))}
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
                  {result.points.map((point, index) => (
                    <div
                      key={index}
                      className="flex items-start space-x-4 p-4 bg-white/5 rounded-lg border border-white/10 group hover:bg-white/10 transition duration-200"
                    >
                      <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <p className="text-gray-200 leading-relaxed text-base">{point}</p>
                      </div>
                      <button
                        onClick={() => copyToClipboard(point)}
                        className="opacity-0 group-hover:opacity-100 transition duration-200 p-2 hover:bg-white/10 rounded-lg"
                      >
                        <Copy className="text-gray-400 hover:text-white" size={16} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Tips Section */}
              <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg p-6 border border-blue-500/30">
                <h4 className="text-lg font-semibold text-white mb-3">💡 Pro Tips for Using These Points:</h4>
                <ul className="text-gray-300 text-sm space-y-2">
                  <li>• Customize each point to match the specific job requirements</li>
                  <li>• Add quantifiable metrics where possible (e.g., "improved performance by 30%")</li>
                  <li>• Use these as starting points and expand with your specific contributions</li>
                  <li>• Adjust technical terminology based on your target audience</li>
                </ul>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-400">
          <p className="mb-2">Powered by Gemini 2.0 Flash • Built with FastAPI & React</p>
          <p className="text-sm">✨ Features: Smart branch detection, enhanced prompts, tech stack analysis</p>
        </div>
      </div>
    </div>
  );
};

export default App;
