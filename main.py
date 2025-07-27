# # # from flask import Flask, request, jsonify
# # # from flask_cors import CORS
# # # import requests
# # # import base64
# # # import google.generativeai as genai
# # # import os
# # # import logging
# # # import traceback
# # # import time
# # # from dotenv import load_dotenv

# # # # Load environment variables
# # # load_dotenv()

# # # app = Flask(__name__)
# # # CORS(app, origins=["http://localhost:3000"])

# # # # Configure Gemini API
# # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # # if not GEMINI_API_KEY:
# # #     print("Warning: GEMINI_API_KEY not found in environment variables")
# # #     GEMINI_API_KEY = "your-gemini-api-key-here"

# # # genai.configure(api_key=GEMINI_API_KEY)

# # # # Set up logging
# # # logging.basicConfig(level=logging.INFO)
# # # logger = logging.getLogger(__name__)

# # # class GitHubClient:
# # #     def __init__(self):
# # #         self.base_url = "https://api.github.com"
        
# # #     def extract_repo_info(self, github_url: str):
# # #         """Extract owner and repo name from GitHub URL"""
# # #         url_parts = str(github_url).rstrip('/').split('/')
# # #         if len(url_parts) < 2:
# # #             raise ValueError("Invalid GitHub URL format")
        
# # #         owner = url_parts[-2]
# # #         repo = url_parts[-1]
# # #         return owner, repo
    
# # #     def get_repository_info(self, owner: str, repo: str):
# # #         """Get basic repository information"""
# # #         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}")
# # #         if response.status_code != 200:
# # #             raise Exception("Repository not found")
# # #         return response.json()
    
# # #     def get_repository_contents(self, owner: str, repo: str, path: str = ""):
# # #         """Get repository contents"""
# # #         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/contents/{path}")
# # #         if response.status_code != 200:
# # #             return []
# # #         return response.json()
    
# # #     def get_file_content(self, owner: str, repo: str, file_path: str):
# # #         """Get content of a specific file"""
# # #         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}")
# # #         if response.status_code != 200:
# # #             return None
        
# # #         file_data = response.json()
# # #         if file_data.get('encoding') == 'base64':
# # #             try:
# # #                 content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
# # #                 return content
# # #             except:
# # #                 return None
# # #         return file_data.get('content', '')

# # # class CodeAnalyzer:
# # #     def __init__(self):
# # #         self.github_client = GitHubClient()
# # #         self.important_files = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb']
    
# # #     def analyze_repository(self, github_url: str):
# # #         """Analyze repository and extract relevant code and structure"""
# # #         owner, repo = self.github_client.extract_repo_info(github_url)
        
# # #         # Get basic repo info
# # #         repo_info = self.github_client.get_repository_info(owner, repo)
        
# # #         # Get repository structure and important files
# # #         files_content = self._get_important_files(owner, repo)
        
# # #         return {
# # #             'repo_info': repo_info,
# # #             'files_content': files_content,
# # #             'owner': owner,
# # #             'repo_name': repo
# # #         }
    
# # #     def _get_important_files(self, owner: str, repo: str, max_files: int = 10):
# # #         """Get content of important files from the repository"""
# # #         files_content = {}
        
# # #         try:
# # #             contents = self.github_client.get_repository_contents(owner, repo)
# # #             if not contents:
# # #                 return files_content
            
# # #             priority_files = []
# # #             code_files = []
            
# # #             for item in contents:
# # #                 if item['type'] == 'file':
# # #                     filename = item['name']
# # #                     if filename.lower() in ['readme.md', 'package.json', 'requirements.txt', 'dockerfile']:
# # #                         priority_files.append(item)
# # #                     elif any(filename.endswith(ext) for ext in self.important_files):
# # #                         code_files.append(item)
            
# # #             # Process priority files first
# # #             for item in priority_files[:3]:
# # #                 content = self.github_client.get_file_content(owner, repo, item['path'])
# # #                 if content:
# # #                     files_content[item['path']] = content[:3000]  # Limit content
            
# # #             # Then process code files
# # #             remaining_slots = max_files - len(files_content)
# # #             for item in code_files[:remaining_slots]:
# # #                 content = self.github_client.get_file_content(owner, repo, item['path'])
# # #                 if content:
# # #                     files_content[item['path']] = content[:3000]  # Limit content
            
# # #         except Exception as e:
# # #             logger.error(f"Error getting repository files: {e}")
        
# # #         return files_content

# # # class ResumePointsGenerator:
# # #     def __init__(self):
# # #         try:
# # #             self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
# # #             logger.info("Gemini 2.0 Flash model initialized successfully")
# # #         except Exception as e:
# # #             logger.error(f"Failed to initialize Gemini 2.0 Flash: {e}")
# # #             try:
# # #                 self.model = genai.GenerativeModel('gemini-pro')
# # #                 logger.info("Using gemini-pro as fallback")
# # #             except Exception as e2:
# # #                 logger.error(f"Failed to initialize fallback model: {e2}")
# # #                 raise Exception("Could not initialize any Gemini model")
    
# # #     def create_prompt(self, repo_data: dict, request_data: dict):
# # #         """Create a detailed prompt for Gemini"""
# # #         repo_info = repo_data['repo_info']
# # #         files_content = repo_data['files_content']
        
# # #         context = f"""
# # # Repository: {repo_info.get('name', 'Unknown')}
# # # Description: {repo_info.get('description', 'No description')}
# # # Language: {repo_info.get('language', 'Multiple')}
# # # Stars: {repo_info.get('stargazers_count', 0)}
# # # Forks: {repo_info.get('forks_count', 0)}

# # # Files analyzed:
# # # """
        
# # #         for file_path, content in files_content.items():
# # #             context += f"\n--- {file_path} ---\n{content[:800]}...\n"
        
# # #         technical_depth = {
# # #             "basic": "Focus on high-level technologies and basic functionalities",
# # #             "medium": "Include specific frameworks, libraries, and implementation details", 
# # #             "advanced": "Emphasize complex algorithms, architectures, performance optimizations"
# # #         }
        
# # #         tone_style = {
# # #             "concise": "Use brief, impactful statements",
# # #             "detailed": "Provide comprehensive explanations with context",
# # #             "action-oriented": "Start with strong action verbs and focus on achievements"
# # #         }
        
# # #         num_points = request_data.get('num_points', 5)
# # #         technical_level = request_data.get('technical_level', 'medium')
# # #         output_tone = request_data.get('output_tone', 'action-oriented')
        
# # #         prompt = f"""
# # # Based on the GitHub repository analysis above, generate {num_points} professional resume bullet points.

# # # Requirements:
# # # - Technical Level: {technical_level} - {technical_depth.get(technical_level, '')}
# # # - Tone: {output_tone} - {tone_style.get(output_tone, '')}
# # # - Focus on technical achievements and implementation details
# # # - Use quantifiable metrics where possible
# # # - Highlight technologies, frameworks, and methodologies used
# # # - Each point should be a complete, professional resume bullet point

# # # Format each point as a separate line starting with "•"

# # # Context: {context}
# # # """
        
# # #         return prompt
    
# # #     def generate_points(self, repo_data: dict, request_data: dict):
# # #         """Generate resume points using Gemini"""
# # #         prompt = self.create_prompt(repo_data, request_data)
        
# # #         try:
# # #             logger.info("Generating content with Gemini...")
# # #             response = self.model.generate_content(prompt)
            
# # #             logger.info("Content generated successfully")
            
# # #             points = []
# # #             if response.text:
# # #                 lines = response.text.strip().split('\n')
# # #                 for line in lines:
# # #                     line = line.strip()
# # #                     if line.startswith('•') or line.startswith('-') or line.startswith('*'):
# # #                         points.append(line[1:].strip())
# # #                     elif line and not line.startswith('#') and len(line) > 15:
# # #                         points.append(line)
            
# # #             # Filter out empty or very short points
# # #             points = [point for point in points if len(point.strip()) > 25]
            
# # #             num_points = request_data.get('num_points', 5)
# # #             if len(points) < num_points:
# # #                 # Generate additional generic points if needed
# # #                 repo_language = repo_data['repo_info'].get('language', 'multiple programming languages')
# # #                 additional_points = [
# # #                     f"Developed and maintained software applications using {repo_language}",
# # #                     "Implemented version control best practices using Git for collaborative development",
# # #                     "Designed and built scalable software solutions following industry best practices",
# # #                     "Collaborated with team members to deliver high-quality code and documentation",
# # #                     "Utilized modern development tools and methodologies to improve code quality"
# # #                 ]
# # #                 points.extend(additional_points[:num_points - len(points)])
            
# # #             return points[:num_points]
            
# # #         except Exception as e:
# # #             logger.error(f"Error in generate_points: {str(e)}")
# # #             logger.error(f"Traceback: {traceback.format_exc()}")
            
# # #             # Return fallback points if AI generation fails
# # #             repo_language = repo_data['repo_info'].get('language', 'multiple programming languages')
# # #             fallback_points = [
# # #                 f"Developed software project using {repo_language} with focus on clean code practices",
# # #                 "Implemented version control and collaborative development practices using Git",
# # #                 "Built and maintained application codebase following software engineering best practices",
# # #                 "Designed software architecture and implemented key features for enhanced functionality",
# # #                 "Utilized modern development tools and frameworks for efficient software development"
# # #             ]
            
# # #             return fallback_points[:request_data.get('num_points', 5)]

# # # # Initialize services
# # # code_analyzer = CodeAnalyzer()
# # # resume_generator = ResumePointsGenerator()

# # # @app.route('/')
# # # def root():
# # #     return jsonify({"message": "GitHub Resume Points Generator API"})

# # # @app.route('/health')
# # # def health_check():
# # #     return jsonify({"status": "healthy"})

# # # @app.route('/generate-resume-points', methods=['POST'])
# # # def generate_resume_points():
# # #     """Generate resume points from GitHub repository"""
# # #     start_time = time.time()
    
# # #     try:
# # #         request_data = request.get_json()
        
# # #         if not request_data or 'github_url' not in request_data:
# # #             return jsonify({"error": "github_url is required"}), 400
        
# # #         logger.info(f"Processing request for: {request_data.get('github_url')}")
        
# # #         # Set defaults
# # #         request_data.setdefault('num_points', 5)
# # #         request_data.setdefault('technical_level', 'medium')
# # #         request_data.setdefault('output_tone', 'action-oriented')
        
# # #         # Analyze the repository
# # #         repo_data = code_analyzer.analyze_repository(request_data['github_url'])
# # #         logger.info("Repository analysis completed")
        
# # #         # Generate resume points
# # #         points = resume_generator.generate_points(repo_data, request_data)
# # #         logger.info("Resume points generated successfully")
        
# # #         processing_time = f"{time.time() - start_time:.2f}s"
        
# # #         return jsonify({
# # #             "points": points,
# # #             "repository_info": {
# # #                 "name": repo_data['repo_info'].get('name'),
# # #                 "description": repo_data['repo_info'].get('description'),
# # #                 "language": repo_data['repo_info'].get('language'),
# # #                 "stars": repo_data['repo_info'].get('stargazers_count', 0),
# # #                 "forks": repo_data['repo_info'].get('forks_count', 0)
# # #             },
# # #             "processing_time": processing_time
# # #         })
        
# # #     except Exception as e:
# # #         logger.error(f"Error in generate_resume_points: {str(e)}")
# # #         logger.error(f"Traceback: {traceback.format_exc()}")
# # #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# # # if __name__ == "__main__":
# # #     print("🚀 Starting GitHub Resume Points Generator API")
# # #     print("📍 Running on http://localhost:8000")
# # #     print("🔧 Make sure GEMINI_API_KEY is set in your .env file")
# # #     app.run(host="0.0.0.0", port=8000, debug=True)
# # import os
# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import firebase_admin
# # from firebase_admin import credentials, auth as firebase_auth
# # import requests
# # import base64
# # import google.generativeai as genai
# # import logging
# # import traceback
# # import time
# # from dotenv import load_dotenv

# # # Load environment variables
# # load_dotenv()

# # app = Flask(__name__)
# # CORS(app, origins=["http://localhost:3000"])

# # # Configure Gemini API KEY
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # if not GEMINI_API_KEY:
# #     print("Warning: GEMINI_API_KEY not found in environment variables")
# #     GEMINI_API_KEY = "your-gemini-api-key-here"

# # genai.configure(api_key=GEMINI_API_KEY)

# # # Setup logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # Initialize Firebase Admin SDK
# # FIREBASE_CERT_PATH = os.getenv("FIREBASE_CERT_PATH", "firebase-adminsdk.json")
# # cred = credentials.Certificate(FIREBASE_CERT_PATH)
# # firebase_admin.initialize_app(cred)

# # # Authentication decorator to verify Firebase ID token
# # from functools import wraps

# # def firebase_auth_required(f):
# #     @wraps(f)
# #     def decorated_function(*args, **kwargs):
# #         auth_header = request.headers.get('Authorization', None)
# #         if not auth_header:
# #             return jsonify({"error": "Authorization header missing"}), 401
        
# #         parts = auth_header.split()
# #         if parts[0].lower() != "bearer" or len(parts) != 2:
# #             return jsonify({"error": "Invalid Authorization header"}), 401

# #         id_token = parts[1]

# #         try:
# #             decoded_token = firebase_auth.verify_id_token(id_token)
# #             request.user = decoded_token  # Attach user info to request object
# #         except Exception as e:
# #             logger.error(f"Firebase token verification failed: {str(e)}")
# #             return jsonify({"error": "Invalid or expired token"}), 401

# #         return f(*args, **kwargs)
# #     return decorated_function


# # # Set up logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # class GitHubClient:
# #     def __init__(self):
# #         self.base_url = "https://api.github.com"
        
# #     def extract_repo_info(self, github_url: str):
# #         """Extract owner and repo name from GitHub URL"""
# #         url_parts = str(github_url).rstrip('/').split('/')
# #         if len(url_parts) < 2:
# #             raise ValueError("Invalid GitHub URL format")
        
# #         owner = url_parts[-2]
# #         repo = url_parts[-1]
# #         return owner, repo
    
# #     def get_repository_info(self, owner: str, repo: str):
# #         """Get basic repository information"""
# #         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}")
# #         if response.status_code != 200:
# #             raise Exception("Repository not found")
# #         return response.json()
    
# #     def get_branches(self, owner: str, repo: str):
# #         """Get all branches of the repository"""
# #         try:
# #             response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/branches")
# #             if response.status_code == 200:
# #                 branches = response.json()
# #                 return [branch['name'] for branch in branches]
# #             return []
# #         except Exception as e:
# #             logger.error(f"Error fetching branches: {e}")
# #             return []
    
# #     def get_repository_contents(self, owner: str, repo: str, path: str = "", branch: str = None):
# #         """Get repository contents from specific branch"""
# #         url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
# #         if branch:
# #             url += f"?ref={branch}"
        
# #         response = requests.get(url)
# #         if response.status_code != 200:
# #             return []
# #         return response.json()
    
# #     def get_file_content(self, owner: str, repo: str, file_path: str, branch: str = None):
# #         """Get content of a specific file from specific branch"""
# #         url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
# #         if branch:
# #             url += f"?ref={branch}"
            
# #         response = requests.get(url)
# #         if response.status_code != 200:
# #             return None
        
# #         file_data = response.json()
# #         if file_data.get('encoding') == 'base64':
# #             try:
# #                 content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
# #                 return content
# #             except:
# #                 return None
# #         return file_data.get('content', '')
    
# #     def find_best_branch(self, owner: str, repo: str):
# #         """Find the most active/content-rich branch"""
# #         branches = self.get_branches(owner, repo)
# #         if not branches:
# #             return None
        
# #         # Score branches based on content
# #         branch_scores = {}
        
# #         for branch in branches[:5]:  # Check max 5 branches to avoid rate limits
# #             try:
# #                 contents = self.get_repository_contents(owner, repo, "", branch)
# #                 if contents:
# #                     # Score based on number of files and presence of code files
# #                     score = len(contents)
                    
# #                     for item in contents:
# #                         if item['type'] == 'file':
# #                             filename = item['name'].lower()
# #                             # Boost score for important files
# #                             if any(filename.endswith(ext) for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.go']):
# #                                 score += 5
# #                             elif filename in ['package.json', 'requirements.txt', 'dockerfile', 'makefile']:
# #                                 score += 3
# #                             elif filename.endswith('.md'):
# #                                 score += 1
                    
# #                     branch_scores[branch] = score
                    
# #             except Exception as e:
# #                 logger.error(f"Error analyzing branch {branch}: {e}")
# #                 continue
        
# #         if branch_scores:
# #             best_branch = max(branch_scores.items(), key=lambda x: x[1])
# #             logger.info(f"Best branch found: {best_branch[0]} (score: {best_branch[1]})")
# #             return best_branch[0]
        
# #         # Fallback to common branch names
# #         priority_branches = ['main', 'master', 'develop', 'dev']
# #         for branch in priority_branches:
# #             if branch in branches:
# #                 return branch
                
# #         return branches[0] if branches else None

# # class CodeAnalyzer:
# #     def __init__(self):
# #         self.github_client = GitHubClient()
# #         self.important_files = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb', '.swift', '.kt']
    
# #     def analyze_repository(self, github_url: str, branch: str = None):
# #         """Analyze repository and extract relevant code and structure"""
# #         owner, repo = self.github_client.extract_repo_info(github_url)
        
# #         # Get basic repo info
# #         repo_info = self.github_client.get_repository_info(owner, repo)
        
# #         # Find best branch if not specified
# #         if not branch:
# #             branch = self.github_client.find_best_branch(owner, repo)
# #             logger.info(f"Using branch: {branch}")
        
# #         # Get repository structure and important files
# #         files_content = self._get_important_files(owner, repo, branch)
        
# #         # Get branch information
# #         branches = self.github_client.get_branches(owner, repo)
        
# #         return {
# #             'repo_info': repo_info,
# #             'files_content': files_content,
# #             'owner': owner,
# #             'repo_name': repo,
# #             'branch_used': branch,
# #             'available_branches': branches
# #         }
    
# #     def _get_important_files(self, owner: str, repo: str, branch: str, max_files: int = 12):
# #         """Get content of important files from the repository"""
# #         files_content = {}
        
# #         try:
# #             contents = self.github_client.get_repository_contents(owner, repo, "", branch)
# #             if not contents:
# #                 return files_content
            
# #             # Categorize files
# #             priority_files = []  # README, config files
# #             code_files = []      # Source code files
# #             config_files = []    # Package managers, build files
            
# #             for item in contents:
# #                 if item['type'] == 'file':
# #                     filename = item['name'].lower()
                    
# #                     if filename.startswith('readme'):
# #                         priority_files.insert(0, item)  # README gets highest priority
# #                     elif filename in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 'composer.json', 'gemfile', 'cargo.toml']:
# #                         config_files.append(item)
# #                     elif filename in ['dockerfile', 'docker-compose.yml', 'makefile', '.gitignore']:
# #                         config_files.append(item)
# #                     elif any(filename.endswith(ext) for ext in self.important_files):
# #                         code_files.append(item)
            
# #             # Process files in order of importance
# #             files_to_process = priority_files[:2] + config_files[:3] + code_files[:7]
            
# #             for item in files_to_process:
# #                 if len(files_content) >= max_files:
# #                     break
                    
# #                 content = self.github_client.get_file_content(owner, repo, item['path'], branch)
# #                 if content and len(content.strip()) > 0:
# #                     # Limit content size but preserve structure
# #                     if len(content) > 4000:
# #                         content = content[:4000] + "\n... [truncated]"
# #                     files_content[item['path']] = content
            
# #             logger.info(f"Analyzed {len(files_content)} files from branch '{branch}'")
            
# #         except Exception as e:
# #             logger.error(f"Error getting repository files: {e}")
        
# #         return files_content

# # class ResumePointsGenerator:
# #     def __init__(self):
# #         try:
# #             self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
# #             logger.info("Gemini 2.0 Flash model initialized successfully")
# #         except Exception as e:
# #             logger.error(f"Failed to initialize Gemini 2.0 Flash: {e}")
# #             try:
# #                 self.model = genai.GenerativeModel('gemini-pro')
# #                 logger.info("Using gemini-pro as fallback")
# #             except Exception as e2:
# #                 logger.error(f"Failed to initialize fallback model: {e2}")
# #                 raise Exception("Could not initialize any Gemini model")
    
# #     def create_enhanced_prompt(self, repo_data: dict, request_data: dict):
# #         """Create an enhanced, detailed prompt for better resume points"""
# #         repo_info = repo_data['repo_info']
# #         files_content = repo_data['files_content']
# #         branch_used = repo_data.get('branch_used', 'main')
        
# #         # Analyze tech stack from files
# #         tech_stack = self._analyze_tech_stack(files_content)
# #         project_complexity = self._assess_project_complexity(repo_info, files_content)
        
# #         context = f"""
# # REPOSITORY ANALYSIS:
# # ==================
# # Repository: {repo_info.get('name', 'Unknown')}
# # Description: {repo_info.get('description', 'No description available')}
# # Primary Language: {repo_info.get('language', 'Not specified')}
# # Repository Stats: {repo_info.get('stargazers_count', 0)} stars, {repo_info.get('forks_count', 0)} forks
# # Branch Analyzed: {branch_used}
# # Project Size: {repo_info.get('size', 0)} KB
# # Last Updated: {repo_info.get('updated_at', 'Unknown')}

# # TECHNOLOGY STACK IDENTIFIED:
# # {tech_stack}

# # PROJECT COMPLEXITY ASSESSMENT:
# # {project_complexity}

# # CODE ANALYSIS:
# # =============
# # """
        
# #         for file_path, content in files_content.items():
# #             context += f"\n--- {file_path} ---\n{content[:1200]}\n"
        
# #         technical_levels = {
# #             "basic": "Focus on technologies used and basic functionalities implemented. Use simple, clear language that any recruiter can understand.",
# #             "medium": "Include specific frameworks, libraries, design patterns, and implementation approaches. Balance technical depth with accessibility.",
# #             "advanced": "Emphasize architectural decisions, performance optimizations, complex algorithms, scalability considerations, and advanced technical concepts. Use industry-specific terminology."
# #         }
        
# #         tone_styles = {
# #             "concise": "Create brief, impactful statements (10-15 words each). Focus on key achievements and technologies.",
# #             "detailed": "Provide comprehensive explanations with context, methodologies, and outcomes (20-30 words each).",
# #             "action-oriented": "Start with strong action verbs (Developed, Implemented, Designed, Built, Optimized). Focus on accomplishments and measurable impact."
# #         }
        
# #         num_points = request_data.get('num_points', 5)
# #         technical_level = request_data.get('technical_level', 'medium')
# #         output_tone = request_data.get('output_tone', 'action-oriented')
        
# #         prompt = f"""
# # As a senior technical recruiter and software engineering expert, analyze this GitHub repository and generate {num_points} exceptional resume bullet points that will impress hiring managers at top tech companies.

# # REQUIREMENTS:
# # ============
# # - Technical Level: {technical_level} - {technical_levels.get(technical_level)}
# # - Writing Style: {output_tone} - {tone_styles.get(output_tone)}
# # - Each bullet point should be a complete, professional resume entry
# # - Include specific technologies, frameworks, and methodologies identified in the code
# # - Quantify impact where possible (performance improvements, scale, complexity)
# # - Highlight problem-solving abilities and technical decision-making
# # - Make each point unique and valuable to potential employers

# # BULLET POINT CRITERIA:
# # =====================
# # 1. Start with a strong action verb (Developed, Implemented, Architected, Optimized, etc.)
# # 2. Specify the technology stack and tools used
# # 3. Describe the functionality or problem solved
# # 4. Include scale, complexity, or impact metrics when available
# # 5. Use industry-standard terminology
# # 6. Ensure each point adds unique value

# # CONTEXT TO ANALYZE:
# # {context}

# # Generate exactly {num_points} bullet points, each on a separate line starting with "•"

# # Focus on making these bullet points stand out to recruiters and demonstrate real software engineering expertise.
# # """
        
# #         return prompt
    
# #     def _analyze_tech_stack(self, files_content: dict) -> str:
# #         """Analyze and categorize the technology stack"""
# #         tech_stack = {
# #             "Frontend": set(),
# #             "Backend": set(),
# #             "Database": set(),
# #             "DevOps/Tools": set(),
# #             "Languages": set()
# #         }
        
# #         # File extension to technology mapping
# #         tech_mapping = {
# #             '.js': 'JavaScript', '.jsx': 'React/JSX', '.ts': 'TypeScript', '.tsx': 'React/TypeScript',
# #             '.py': 'Python', '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.go': 'Go',
# #             '.rs': 'Rust', '.php': 'PHP', '.rb': 'Ruby', '.swift': 'Swift', '.kt': 'Kotlin'
# #         }
        
# #         for file_path, content in files_content.items():
# #             filename = file_path.lower()
# #             content_lower = content.lower()
            
# #             # Detect by file extension
# #             for ext, lang in tech_mapping.items():
# #                 if filename.endswith(ext):
# #                     tech_stack["Languages"].add(lang)
            
# #             # Detect frameworks and libraries from content
# #             if 'package.json' in filename:
# #                 if 'react' in content_lower: tech_stack["Frontend"].add('React')
# #                 if 'vue' in content_lower: tech_stack["Frontend"].add('Vue.js')
# #                 if 'angular' in content_lower: tech_stack["Frontend"].add('Angular')
# #                 if 'express' in content_lower: tech_stack["Backend"].add('Express.js')
# #                 if 'next' in content_lower: tech_stack["Frontend"].add('Next.js')
                
# #             if 'requirements.txt' in filename or filename.endswith('.py'):
# #                 if 'django' in content_lower: tech_stack["Backend"].add('Django')
# #                 if 'flask' in content_lower: tech_stack["Backend"].add('Flask')
# #                 if 'fastapi' in content_lower: tech_stack["Backend"].add('FastAPI')
# #                 if 'tensorflow' in content_lower: tech_stack["Backend"].add('TensorFlow')
# #                 if 'pytorch' in content_lower: tech_stack["Backend"].add('PyTorch')
                
# #             if 'dockerfile' in filename:
# #                 tech_stack["DevOps/Tools"].add('Docker')
                
# #             # Database detection
# #             if any(db in content_lower for db in ['postgresql', 'postgres']):
# #                 tech_stack["Database"].add('PostgreSQL')
# #             if 'mongodb' in content_lower or 'mongo' in content_lower:
# #                 tech_stack["Database"].add('MongoDB')
# #             if 'mysql' in content_lower:
# #                 tech_stack["Database"].add('MySQL')
# #             if 'redis' in content_lower:
# #                 tech_stack["Database"].add('Redis')
        
# #         # Format tech stack summary
# #         summary = []
# #         for category, techs in tech_stack.items():
# #             if techs:
# #                 summary.append(f"{category}: {', '.join(sorted(techs))}")
        
# #         return '\n'.join(summary) if summary else "Technology stack could not be fully determined from available files."
    
# #     def _assess_project_complexity(self, repo_info: dict, files_content: dict) -> str:
# #         """Assess project complexity and scale"""
# #         complexity_indicators = []
        
# #         # Repository metrics
# #         stars = repo_info.get('stargazers_count', 0)
# #         forks = repo_info.get('forks_count', 0)
# #         size = repo_info.get('size', 0)
        
# #         if stars > 100:
# #             complexity_indicators.append(f"Popular open-source project ({stars} stars)")
# #         if forks > 20:
# #             complexity_indicators.append(f"Community-driven development ({forks} forks)")
# #         if size > 10000:  # > 10MB
# #             complexity_indicators.append("Large-scale codebase")
        
# #         # Code complexity analysis
# #         file_count = len(files_content)
# #         total_lines = sum(len(content.split('\n')) for content in files_content.values())
        
# #         if file_count > 10:
# #             complexity_indicators.append("Multi-file architecture")
# #         if total_lines > 1000:
# #             complexity_indicators.append(f"Substantial codebase (~{total_lines} lines analyzed)")
        
# #         # Technical complexity
# #         has_config_files = any('package.json' in f or 'requirements.txt' in f or 'dockerfile' in f.lower() 
# #                               for f in files_content.keys())
# #         if has_config_files:
# #             complexity_indicators.append("Production-ready configuration")
        
# #         return '; '.join(complexity_indicators) if complexity_indicators else "Standard project complexity"
    
# #     def generate_points(self, repo_data: dict, request_data: dict):
# #         """Generate enhanced resume points using Gemini"""
# #         prompt = self.create_enhanced_prompt(repo_data, request_data)
        
# #         try:
# #             logger.info("Generating enhanced resume points with Gemini...")
# #             response = self.model.generate_content(prompt)
            
# #             logger.info("Content generated successfully")
            
# #             points = []
# #             if response.text:
# #                 lines = response.text.strip().split('\n')
# #                 for line in lines:
# #                     line = line.strip()
# #                     if line.startswith('•') or line.startswith('-') or line.startswith('*'):
# #                         clean_point = line[1:].strip()
# #                         if len(clean_point) > 30:  # Ensure substantial content
# #                             points.append(clean_point)
# #                     elif line and not line.startswith('#') and len(line) > 30:
# #                         points.append(line)
            
# #             # Filter and enhance points
# #             points = [point for point in points if len(point.strip()) > 30 and not point.lower().startswith(('generate', 'create', 'here are'))]
            
# #             num_points = request_data.get('num_points', 5)
# #             if len(points) < num_points:
# #                 # Generate enhanced fallback points
# #                 repo_name = repo_data['repo_info'].get('name', 'software project')
# #                 repo_language = repo_data['repo_info'].get('language', 'modern programming languages')
                
# #                 enhanced_fallbacks = [
# #                     f"Developed {repo_name} using {repo_language} with emphasis on clean code architecture and best practices",
# #                     f"Implemented comprehensive version control workflow using Git for collaborative development of {repo_name}",
# #                     f"Designed and built scalable software architecture for {repo_name} following industry-standard design patterns",
# #                     f"Collaborated on {repo_name} development using modern software engineering methodologies and code review processes",
# #                     f"Optimized {repo_name} performance and maintainability through refactoring and technical debt reduction"
# #                 ]
                
# #                 points.extend(enhanced_fallbacks[:num_points - len(points)])
            
# #             return points[:num_points]
            
# #         except Exception as e:
# #             logger.error(f"Error in generate_points: {str(e)}")
# #             logger.error(f"Traceback: {traceback.format_exc()}")
            
# #             # Enhanced fallback points
# #             repo_name = repo_data['repo_info'].get('name', 'software application')
# #             repo_language = repo_data['repo_info'].get('language', 'modern programming technologies')
            
# #             fallback_points = [
# #                 f"Developed {repo_name} using {repo_language} with focus on scalable architecture and code quality",
# #                 f"Implemented robust version control and collaborative development practices using Git for {repo_name}",
# #                 f"Built comprehensive software solution {repo_name} following software engineering best practices and design patterns",
# #                 f"Designed technical architecture and implemented core features for {repo_name} with emphasis on maintainability",
# #                 f"Utilized modern development tools and methodologies to deliver high-quality {repo_name} solution"
# #             ]
            
# #             return fallback_points[:request_data.get('num_points', 5)]

# # # Initialize services after classes
# # code_analyzer = CodeAnalyzer()
# # resume_generator = ResumePointsGenerator()


# # @app.route('/')
# # def root():
# #     return jsonify({"message": "GitHub Resume Points Generator API"})


# # @app.route('/health')
# # def health_check():
# #     return jsonify({"status": "healthy"})


# # @app.route('/get-branches/<owner>/<repo>')
# # @firebase_auth_required
# # def get_branches(owner, repo):
# #     """Get available branches for a repository"""
# #     try:
# #         branches = code_analyzer.github_client.get_branches(owner, repo)
# #         return jsonify({"branches": branches})
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500


# # @app.route('/generate-resume-points', methods=['POST'])
# # @firebase_auth_required
# # def generate_resume_points():
# #     """Generate resume points from GitHub repository"""
# #     start_time = time.time()

# #     try:
# #         request_data = request.get_json()

# #         if not request_data or 'github_url' not in request_data:
# #             return jsonify({"error": "github_url is required"}), 400

# #         # You can also get user info if needed:
# #         user_uid = request.user.get('uid')
# #         logger.info(f"Processing request for user: {user_uid}, repo: {request_data.get('github_url')}")

# #         # Set defaults
# #         request_data.setdefault('num_points', 5)
# #         request_data.setdefault('technical_level', 'medium')
# #         request_data.setdefault('output_tone', 'action-oriented')

# #         # Extract branch from request (optional)
# #         branch = request_data.get('branch', None)

# #         # Analyze the repository
# #         repo_data = code_analyzer.analyze_repository(request_data['github_url'], branch)
# #         logger.info(f"Repository analysis completed using branch: {repo_data.get('branch_used')}")

# #         # Generate resume points
# #         points = resume_generator.generate_points(repo_data, request_data)
# #         logger.info("Enhanced resume points generated successfully")

# #         processing_time = f"{time.time() - start_time:.2f}s"

# #         return jsonify({
# #             "points": points,
# #             "repository_info": {
# #                 "name": repo_data['repo_info'].get('name'),
# #                 "description": repo_data['repo_info'].get('description'),
# #                 "language": repo_data['repo_info'].get('language'),
# #                 "stars": repo_data['repo_info'].get('stargazers_count', 0),
# #                 "forks": repo_data['repo_info'].get('forks_count', 0),
# #                 "branch_used": repo_data.get('branch_used'),
# #                 "available_branches": repo_data.get('available_branches', [])
# #             },
# #             "processing_time": processing_time
# #         })

# #     except Exception as e:
# #         logger.error(f"Error in generate_resume_points: {str(e)}")
# #         logger.error(f"Traceback: {traceback.format_exc()}")
# #         return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# # if __name__ == "__main__":
# #     print("🚀 Starting Enhanced GitHub Resume Points Generator API with Firebase Auth")
# #     print("📍 Running on http://localhost:8000")
# #     print("🔧 Features: Smart branch detection, enhanced prompts, tech stack analysis")
# #     print("🌟 Make sure GEMINI_API_KEY and FIREBASE_CERT_PATH are set in your .env file")
# #     app.run(host="0.0.0.0", port=8000, debug=True)
# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import firebase_admin
# from firebase_admin import credentials, auth as firebase_auth
# import requests
# import base64
# import google.generativeai as genai
# import logging
# import traceback
# import time
# from dotenv import load_dotenv


# # Load environment variables
# load_dotenv()


# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])


# # Configure Gemini API
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_KEY:
#     print("Warning: GEMINI_API_KEY not found in environment variables")
#     GEMINI_KEY = "your_gemini_api_key_here"

# genai.configure(api_key=GEMINI_KEY)


# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# # Initialize Firebase Admin SDK
# FIREBASE_CERT_PATH = os.getenv("FIREBASE_CERT_PATH", "firebase-adminsdk.json")
# cred = credentials.Certificate(FIREBASE_CERT_PATH)
# firebase_admin.initialize_app(cred)


# # Authentication decorator to verify Firebase ID token
# from functools import wraps


# def firebase_auth_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         auth_header = request.headers.get('Authorization', None)
#         if not auth_header:
#             return jsonify({"error": "Authorization header missing"}), 401

#         parts = auth_header.split()
#         if parts[0].lower() != "bearer" or len(parts) != 2:
#             return jsonify({"error": "Invalid Authorization header"}), 401

#         id_token = parts[1]

#         try:
#             decoded_token = firebase_auth.verify_id_token(id_token)
#             request.user = decoded_token  # Attach user info to request object
#         except Exception as e:
#             logger.error(f"Firebase token verification failed: {str(e)}")
#             return jsonify({"error": "Invalid or expired token"}), 401

#         return f(*args, **kwargs)
#     return decorated_function


# class GitHubClient:
#     def __init__(self):
#         self.base_url = "https://api.github.com"
#         self.github_token = os.getenv("GITHUB_TOKEN")

#     def _headers(self):
#         headers = {
#             "Accept": "application/vnd.github.v3+json"
#         }
#         if self.github_token:
#             headers["Authorization"] = f"token {self.github_token}"
#         return headers

#     def extract_repo_info(self, github_url: str):
#         """Extract owner and repo name from GitHub URL"""
#         url_parts = str(github_url).rstrip('/').split('/')
#         if len(url_parts) < 2:
#             raise ValueError("Invalid GitHub URL format")

#         owner = url_parts[-2]
#         repo = url_parts[-1]
#         return owner, repo

#     def get_repository_info(self, owner: str, repo: str):
#         """Get basic repository information"""
#         url = f"{self.base_url}/repos/{owner}/{repo}"
#         response = requests.get(url, headers=self._headers())
#         if response.status_code != 200:
#             logger.error(f"GitHub repo info fetch failed: {response.status_code}, {response.text}")
#             raise Exception("Repository not found")
#         return response.json()

#     def get_branches(self, owner: str, repo: str):
#         """Get all branches of a repository"""
#         try:
#             url = f"{self.base_url}/repos/{owner}/{repo}/branches"
#             response = requests.get(url, headers=self._headers())
#             if response.status_code == 200:
#                 branches = response.json()
#                 return [branch['name'] for branch in branches]
#             else:
#                 logger.error(f"GitHub branches fetch failed: {response.status_code}, {response.text}")
#                 return []
#         except Exception as e:
#             logger.error(f"Error fetching branches: {e}")
#             return []

#     def get_repository_contents(self, owner: str, repo: str, path: str = "", branch: str = None):
#         """Get repository contents from a specific branch"""
#         url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
#         if branch:
#             url += f"?ref={branch}"
#         response = requests.get(url, headers=self._headers())
#         if response.status_code != 200:
#             logger.error(f"GitHub repo contents fetch failed: {response.status_code}, {response.text}")
#             return []
#         return response.json()

#     def get_file_content(self, owner: str, repo: str, file_path: str, branch: str = None):
#         """Get content of a specific file from a specific branch"""
#         url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
#         if branch:
#             url += f"?ref={branch}"
#         response = requests.get(url, headers=self._headers())
#         if response.status_code != 200:
#             logger.error(f"GitHub file content fetch failed: {response.status_code}, {response.text}")
#             return None
#         file_data = response.json()
#         if file_data.get('encoding') == 'base64':
#             try:
#                 return base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
#             except Exception as e:
#                 logger.error(f"Failed decoding base64 content of {file_path}: {e}")
#                 return None
#         return file_data.get('content', '')

#     def find_best_branch(self, owner: str, repo: str):
#         """Find the branch with most relevant code/content"""
#         branches = self.get_branches(owner, repo)
#         if not branches:
#             return None

#         branch_scores = {}
#         for branch in branches[:5]:  # Limit to first five for rate control
#             try:
#                 contents = self.get_repository_contents(owner, repo, "", branch)
#                 if not contents:
#                     continue

#                 score = len(contents)
#                 for item in contents:
#                     if item['type'] == 'file':
#                         filename = item['name'].lower()
#                         if any(filename.endswith(ext) for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.go']):
#                             score += 5
#                         elif filename in ['package.json', 'requirements.txt', 'dockerfile', 'makefile']:
#                             score += 3
#                         elif filename.endswith('.md'):
#                             score += 1
#                 branch_scores[branch] = score
#             except Exception as e:
#                 logger.error(f"Error analyzing branch {branch}: {e}")
#                 continue

#         if branch_scores:
#             best_branch = max(branch_scores.items(), key=lambda x: x[1])
#             logger.info(f"Best branch found: {best_branch[0]} (score: {best_branch[1]})")
#             return best_branch[0]

#         for preferred in ['main', 'master', 'develop', 'dev']:
#             if preferred in branches:
#                 return preferred

#         return branches[0]


# class CodeAnalyzer:
#     def __init__(self):
#         self.github_client = GitHubClient()
#         self.important_exts = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb', '.swift', '.kt']

#     def analyze_repository(self, github_url: str, branch: str = None):
#         owner, repo = self.github_client.extract_repo_info(github_url)

#         repo_info = self.github_client.get_repository_info(owner, repo)

#         if branch is None:
#             branch = self.github_client.find_best_branch(owner, repo)

#         files_content = self._get_important_files(owner, repo, branch)
#         branches = self.github_client.get_branches(owner, repo)

#         return {
#             "repo_info": repo_info,
#             "files_content": files_content,
#             "owner": owner,
#             "repo_name": repo,
#             "branch_used": branch,
#             "available_branches": branches
#         }

#     def _get_important_files(self, owner, repo, branch, max_files=12):
#         file_contents = {}
#         try:
#             contents = self.github_client.get_repository_contents(owner, repo, "", branch)
#             if not contents:
#                 return file_contents

#             priority_files = []
#             code_files = []
#             config_files = []

#             for item in contents:
#                 if item['type'] != 'file':
#                     continue
#                 filename = item['name'].lower()
#                 if filename.startswith('readme'):
#                     priority_files.insert(0, item)
#                 elif filename in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 'composer.json', 'gemfile', 'cargo.toml']:
#                     config_files.append(item)
#                 elif filename in ['dockerfile', 'docker-compose.yml', 'makefile', '.gitignore']:
#                     config_files.append(item)
#                 elif any(filename.endswith(ext) for ext in self.important_exts):
#                     code_files.append(item)

#             selected = priority_files[:2] + config_files[:3] + code_files[:7]

#             for item in selected:
#                 if len(file_contents) >= max_files:
#                     break
#                 content = self.github_client.get_file_content(owner, repo, item['path'], branch)
#                 if content and content.strip():
#                     if len(content) > 4000:
#                         content = content[:4000] + "\n... [truncated]"
#                     file_contents[item['path']] = content

#             logger.info(f"Analyzed {len(file_contents)} files from branch '{branch}'")
#         except Exception as e:
#             logger.error(f"Error fetching files for repo: {e}")

#         return file_contents


# class ResumeGenerator:
#     def __init__(self):
#         try:
#             self.model = genai.GenerativeModel("gemini-2.0-flash")
#             logger.info("Gemini 2.0 Flash initialized")
#         except Exception as e:
#             logger.error(f"Failed to initialize Gemini 2.0 Flash: {e}")
#             try:
#                 self.model = genai.GenerativeModel("gemini-pro")
#                 logger.info("Fallback to Gemini Pro model")
#             except Exception as ee:
#                 logger.error(f"Failed fallback model initialization: {ee}")
#                 raise e

#     def generate_points(self, repo_data, request_data):
#         # Compose prompt with repo context and user parameters per previous logic...
#         # Here, simplified for brevity; implement full prompt logic as needed
#         prompt = self._build_prompt(repo_data, request_data)

#         try:
#             response = self.model.generate_content(prompt)
#             text = response.text if response and hasattr(response, 'text') else ''
#             points = self._parse_points(text)
#             if len(points) < request_data.get('num_points', 5):
#                 points += self._fallback_points(repo_data, request_data)
#             return points[:request_data.get('num_points', 5)]
#         except Exception as e:
#             logger.error(f"Error generating points: {e}")
#             logger.error(traceback.format_exc())
#             return self._fallback_points(repo_data, request_data)

#     def _build_prompt(self, repo_data, request_data):
#         # Build the comprehensive prompt here based on repo_data and request_data
#         # This skeleton only for illustration
#         return f"Analyze this repository: {repo_data['repo_info']['name']} and generate {request_data.get('num_points', 5)} resume points."

#     def _parse_points(self, text):
#         # Parse the model's output into list of bullet points
#         points = []
#         for line in text.splitlines():
#             line = line.strip()
#             if line.startswith('•') or line.startswith('-') or line.startswith('*'):
#                 points.append(line[1:].strip())
#             elif line:
#                 points.append(line)
#         return [p for p in points if p and len(p) > 20]

#     def _fallback_points(self, repo_data, request_data):
#         base = repo_data['repo_info'].get('name', 'software project')
#         return [
#             f"Developed {base} using modern technologies",
#             f"Improved performance and maintainability of {base}",
#             f"Collaborated in agile team to deliver {base}"
#         ]


# code_analyzer = CodeAnalyzer()
# resume_generator = ResumeGenerator()


# @app.route('/')
# def index():
#     return jsonify({"message": "Welcome to GitHub Resume Generator API"})


# @app.route('/health', methods=['GET'])
# def health():
#     return jsonify({"status": "healthy"})


# @app.route('/get-branches/<owner>/<repo>', methods=['GET'])
# @firebase_auth_required
# def get_branches(owner, repo):
#     try:
#         branches = code_analyzer.github_client.get_branches(owner, repo)
#         return jsonify({"branches": branches})
#     except Exception as e:
#         logger.error(f"Error getting branches: {e}")
#         return jsonify({"error": str(e)}), 500


# @app.route('/generate-resume-points', methods=['POST'])
# @firebase_auth_required
# def generate_resume_points():
#     start_time = time.time()
#     try:
#         data = request.json
#         if not data or "github_url" not in data:
#             return jsonify({"error": "Missing required parameter: github_url"}), 400

#         user_uid = request.user.get("uid")
#         logger.info(f"User {user_uid} requested analysis on {data.get('github_url')}")

#         data.setdefault("num_points", 5)
#         data.setdefault("technical_level", "medium")
#         data.setdefault("output_tone", "action-oriented")

#         branch = data.get("branch")
#         repo_data = code_analyzer.analyze_repository(data["github_url"], branch)
#         points = resume_generator.generate_points(repo_data, data)

#         elapsed = f"{time.time() - start_time:.2f}s"

#         return jsonify(
#             {
#                 "points": points,
#                 "repository_info": {
#                     "name": repo_data["repo_info"]["name"],
#                     "description": repo_data["repo_info"].get("description"),
#                     "language": repo_data["repo_info"].get("language"),
#                     "stars": repo_data["repo_info"].get("stargazers_count", 0),
#                     "forks": repo_data["repo_info"].get("forks_count", 0),
#                     "branch_used": repo_data.get("branch_used"),
#                     "available_branches": repo_data.get("available_branches", []),
#                 },
#                 "processing_time": elapsed,
#             }
#         )
#     except Exception as e:
#         logger.error(f"Error during resume points generation: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     logger.info("Starting Flask app...")
#     app.run(host="0.0.0.0", port=8000, debug=True)


import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
import requests
import base64
import google.generativeai as genai
import logging
import traceback
import time
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Configure Gemini API
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    GEMINI_KEY = "your_gemini_api_key_here"

genai.configure(api_key=GEMINI_KEY)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_firebase():
    """Initialize Firebase using environment variables only"""
    try:
        # Check if Firebase is already initialized
        if firebase_admin._apps:
            logger.info("Firebase already initialized")
            return True
        
        # Load Firebase credentials from environment variables
        firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
        firebase_private_key = os.getenv("FIREBASE_PRIVATE_KEY")
        firebase_client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
        
        if not (firebase_project_id and firebase_private_key and firebase_client_email):
            raise Exception("Missing required Firebase environment variables. Please check FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, and FIREBASE_CLIENT_EMAIL in your .env file.")
        
        logger.info("Loading Firebase credentials from environment variables")
        
        # Handle the private key formatting
        private_key = firebase_private_key.replace('\\n', '\n')
        
        creds_dict = {
            "type": os.getenv("FIREBASE_TYPE", "service_account"),
            "project_id": firebase_project_id,
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": private_key,
            "client_email": firebase_client_email,
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
        }
        
        cred = credentials.Certificate(creds_dict)
        
        # Initialize Firebase
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Firebase initialization failed: {e}")
        logger.error(traceback.format_exc())
        return False

# Initialize Firebase
firebase_initialized = initialize_firebase()

if firebase_initialized:
    db = firestore.client()
    logger.info("Firestore client initialized")
else:
    db = None
    logger.error("Firestore client not available")

def firebase_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not firebase_initialized:
            return jsonify({"error": "Firebase not properly configured"}), 503
            
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"error": "Invalid Authorization header"}), 401

        id_token = parts[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            request.user = decoded_token
        except Exception as e:
            logger.error(f"Firebase token verification failed: {str(e)}")
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    return decorated_function

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.github_token = os.getenv("GITHUB_TOKEN")

    def _headers(self):
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Resume-Generator/1.0"
        }
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    def extract_repo_info(self, github_url: str):
        """Extract owner and repo name from GitHub URL"""
        url_parts = str(github_url).rstrip('/').split('/')
        if len(url_parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        owner = url_parts[-2]
        repo = url_parts[-1]
        return owner, repo

    def get_repository_info(self, owner: str, repo: str):
        """Get comprehensive repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            logger.error(f"GitHub repo info fetch failed: {response.status_code}, {response.text}")
            raise Exception(f"Repository not found: {response.status_code}")
        return response.json()

    def get_branches(self, owner: str, repo: str):
        """Get all branches of a repository"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/branches"
            response = requests.get(url, headers=self._headers())
            if response.status_code == 200:
                branches = response.json()
                return [branch['name'] for branch in branches]
            else:
                logger.error(f"GitHub branches fetch failed: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error fetching branches: {e}")
            return []

    def get_repository_contents(self, owner: str, repo: str, path: str = "", branch: str = None):
        """Get repository contents from a specific branch"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        if branch:
            url += f"?ref={branch}"
        
        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            logger.error(f"GitHub repo contents fetch failed: {response.status_code}")
            return []
        return response.json()

    def get_file_content(self, owner: str, repo: str, file_path: str, branch: str = None):
        """Get content of a specific file from a specific branch"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
        if branch:
            url += f"?ref={branch}"
            
        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            return None
            
        file_data = response.json()
        if file_data.get('encoding') == 'base64':
            try:
                content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
                return content
            except Exception as e:
                logger.error(f"Failed decoding base64 content: {e}")
                return None
        return file_data.get('content', '')

    def find_best_branch(self, owner: str, repo: str):
        """Find the branch with most relevant code/content"""
        branches = self.get_branches(owner, repo)
        if not branches:
            return None

        branch_scores = {}
        
        # Analyze up to 5 branches to find the best one
        for branch in branches[:5]:
            try:
                contents = self.get_repository_contents(owner, repo, "", branch)
                if not contents:
                    continue

                score = len(contents)
                code_files = 0
                config_files = 0
                
                for item in contents:
                    if item['type'] == 'file':
                        filename = item['name'].lower()
                        # Score code files highly
                        if any(filename.endswith(ext) for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.go', '.rs']):
                            score += 10
                            code_files += 1
                        # Score config files moderately
                        elif filename in ['package.json', 'requirements.txt', 'dockerfile', 'makefile', 'pom.xml']:
                            score += 5
                            config_files += 1
                        # Score documentation files slightly
                        elif filename.endswith('.md'):
                            score += 2

                # Bonus for having a good mix of files
                if code_files > 0 and config_files > 0:
                    score += 15
                    
                branch_scores[branch] = score
                logger.info(f"Branch '{branch}' scored {score} points ({code_files} code files, {config_files} config files)")
                
            except Exception as e:
                logger.error(f"Error analyzing branch {branch}: {e}")
                continue

        if branch_scores:
            best_branch = max(branch_scores.items(), key=lambda x: x[1])
            logger.info(f"Best branch selected: {best_branch[0]} (score: {best_branch[1]})")
            return best_branch[0]

        # Fallback to common branch names
        for preferred in ['main', 'master', 'develop', 'dev', 'development']:
            if preferred in branches:
                logger.info(f"Using fallback branch: {preferred}")
                return preferred

        return branches[0] if branches else None

class TechStackAnalyzer:
    """Analyzes technology stack from repository files"""
    
    def __init__(self):
        self.tech_patterns = {
            # Frontend Technologies
            'React': ['react', 'jsx', '.jsx', 'react-dom'],
            'Vue.js': ['vue', '.vue', 'vue-cli'],
            'Angular': ['angular', '@angular', '.component.ts'],
            'Next.js': ['next', 'next.config', '_app.js'],
            'Svelte': ['svelte', '.svelte'],
            
            # Backend Technologies
            'Express.js': ['express', 'app.use', 'app.get'],
            'FastAPI': ['fastapi', 'from fastapi'],
            'Django': ['django', 'from django', 'manage.py'],
            'Flask': ['flask', 'from flask', 'app.route'],
            'Spring Boot': ['spring-boot', '@SpringBootApplication', '@RestController'],
            'Node.js': ['node', 'npm', 'package.json'],
            
            # Databases
            'MongoDB': ['mongodb', 'mongoose', 'mongo'],
            'PostgreSQL': ['postgresql', 'postgres', 'psycopg2'],
            'MySQL': ['mysql', 'mysql2'],
            'Redis': ['redis', 'redis-py'],
            'SQLite': ['sqlite', 'sqlite3'],
            
            # Languages
            'Python': ['.py', 'python', 'requirements.txt'],
            'JavaScript': ['.js', 'javascript', 'package.json'],
            'TypeScript': ['.ts', 'typescript', 'tsconfig.json'],
            'Java': ['.java', 'pom.xml', 'build.gradle'],
            'Go': ['.go', 'go.mod', 'go.sum'],
            'Rust': ['.rs', 'cargo.toml'],
            'C++': ['.cpp', '.hpp', 'cmake'],
            
            # DevOps & Tools
            'Docker': ['dockerfile', 'docker-compose', '.dockerignore'],
            'Kubernetes': ['k8s', 'kubernetes', '.yaml'],
            'AWS': ['aws', 's3', 'lambda', 'ec2'],
            'CI/CD': ['.github/workflows', 'jenkins', '.travis.yml'],
            'Testing': ['jest', 'pytest', 'junit', 'mocha']
        }
    
    def analyze(self, files_content, repo_info):
        """Analyze tech stack from repository files"""
        detected_techs = set()
        evidence = {}
        
        # Analyze file extensions and names
        for file_path in files_content.keys():
            filename = file_path.lower()
            for tech, patterns in self.tech_patterns.items():
                for pattern in patterns:
                    if pattern in filename:
                        detected_techs.add(tech)
                        evidence[tech] = evidence.get(tech, []) + [f"File: {file_path}"]
        
        # Analyze file contents
        for file_path, content in files_content.items():
            content_lower = content.lower()
            for tech, patterns in self.tech_patterns.items():
                for pattern in patterns:
                    if pattern in content_lower:
                        detected_techs.add(tech)
                        evidence[tech] = evidence.get(tech, []) + [f"Content in: {file_path}"]
        
        # Add primary language from GitHub
        if repo_info.get('language'):
            detected_techs.add(repo_info['language'])
            evidence[repo_info['language']] = ['Primary language (GitHub)']
        
        return {
            'technologies': list(detected_techs),
            'evidence': evidence,
            'primary_language': repo_info.get('language', 'Unknown')
        }

class CodeAnalyzer:
    def __init__(self):
        self.github_client = GitHubClient()
        self.tech_analyzer = TechStackAnalyzer()
        self.important_exts = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb', '.swift', '.kt']

    def analyze_repository(self, github_url: str, branch: str = None):
        """Comprehensive repository analysis"""
        owner, repo = self.github_client.extract_repo_info(github_url)
        logger.info(f"Analyzing repository: {owner}/{repo}")

        # Get repository metadata
        repo_info = self.github_client.get_repository_info(owner, repo)
        logger.info(f"Repository info retrieved: {repo_info['name']}, Language: {repo_info.get('language')}")

        # Determine best branch if not specified
        if branch is None:
            branch = self.github_client.find_best_branch(owner, repo)
            logger.info(f"Auto-selected branch: {branch}")

        # Get file contents
        files_content = self._get_important_files(owner, repo, branch)
        logger.info(f"Analyzed {len(files_content)} files")

        # Analyze technology stack
        tech_analysis = self.tech_analyzer.analyze(files_content, repo_info)
        logger.info(f"Detected technologies: {tech_analysis['technologies']}")

        # Get all branches
        branches = self.github_client.get_branches(owner, repo)

        return {
            "repo_info": repo_info,
            "files_content": files_content,
            "tech_analysis": tech_analysis,
            "owner": owner,
            "repo_name": repo,
            "branch_used": branch,
            "available_branches": branches,
            "analysis_summary": {
                "total_files_analyzed": len(files_content),
                "technologies_detected": len(tech_analysis['technologies']),
                "primary_language": tech_analysis['primary_language']
            }
        }

    def _get_important_files(self, owner, repo, branch, max_files=15):
        """Get content of most important files for analysis"""
        file_contents = {}
        
        try:
            contents = self.github_client.get_repository_contents(owner, repo, "", branch)
            if not contents:
                logger.warning("No contents found in repository")
                return file_contents

            # Categorize files by importance
            priority_files = []    # README, main config files
            code_files = []        # Source code files
            config_files = []      # Package configs, build files
            doc_files = []         # Documentation files

            for item in contents:
                if item['type'] != 'file':
                    continue
                    
                filename = item['name'].lower()
                
                # Highest priority: README files
                if filename.startswith('readme'):
                    priority_files.insert(0, item)
                # High priority: Package and build configuration
                elif filename in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 
                                'composer.json', 'gemfile', 'cargo.toml', 'go.mod']:
                    priority_files.append(item)
                # Medium priority: Infrastructure and deployment
                elif filename in ['dockerfile', 'docker-compose.yml', 'makefile', '.gitignore', 
                                'tsconfig.json', 'webpack.config.js']:
                    config_files.append(item)
                # Code files
                elif any(filename.endswith(ext) for ext in self.important_exts):
                    code_files.append(item)
                # Documentation
                elif filename.endswith('.md'):
                    doc_files.append(item)

            # Select files in order of importance
            selected_files = (
                priority_files[:3] +      # Top 3 priority files
                config_files[:4] +        # Top 4 config files  
                code_files[:6] +          # Top 6 code files
                doc_files[:2]             # Top 2 doc files
            )

            logger.info(f"Selected {len(selected_files)} files for analysis")

            # Fetch content for selected files
            for item in selected_files:
                if len(file_contents) >= max_files:
                    break
                    
                content = self.github_client.get_file_content(owner, repo, item['path'], branch)
                if content and content.strip():
                    # Limit content size but preserve structure
                    if len(content) > 5000:
                        # Try to keep complete functions/classes when truncating
                        content = content[:5000] + "\n... [truncated for analysis]"
                    file_contents[item['path']] = content
                    logger.debug(f"Added file: {item['path']} ({len(content)} chars)")

            logger.info(f"Successfully analyzed {len(file_contents)} files from branch '{branch}'")
            
        except Exception as e:
            logger.error(f"Error fetching repository files: {e}")
            logger.error(traceback.format_exc())

        return file_contents

class ResumeGenerator:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
            logger.info("Gemini 2.0 Flash Experimental initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini 2.0 Flash Exp: {e}")
            try:
                self.model = genai.GenerativeModel("gemini-pro")
                logger.info("Fallback to Gemini Pro model")
            except Exception as ee:
                logger.error(f"Failed fallback model initialization: {ee}")
                raise Exception("Could not initialize any Gemini model")

    def generate_points(self, repo_data, request_data):
        """Generate high-quality resume points based on actual repository analysis"""
        prompt = self._build_comprehensive_prompt(repo_data, request_data)
        
        try:
            logger.info("Generating resume points with Gemini...")
            response = self.model.generate_content(prompt)
            
            if not response or not hasattr(response, 'text') or not response.text:
                logger.error("Empty response from Gemini")
                return self._fallback_points(repo_data, request_data)
            
            text = response.text
            logger.info(f"Generated response length: {len(text)} characters")
            
            points = self._parse_points(text)
            logger.info(f"Parsed {len(points)} points from response")
            
            # Ensure we have enough points
            num_requested = request_data.get('num_points', 5)
            if len(points) < num_requested:
                logger.info(f"Need {num_requested - len(points)} more points, adding fallbacks")
                fallback_points = self._fallback_points(repo_data, request_data)
                points.extend(fallback_points[:num_requested - len(points)])
            
            return points[:num_requested]
            
        except Exception as e:
            logger.error(f"Error generating points: {e}")
            logger.error(traceback.format_exc())
            return self._fallback_points(repo_data, request_data)

    def _build_comprehensive_prompt(self, repo_data, request_data):
        """Build a comprehensive prompt for high-quality resume point generation"""
        
        repo_info = repo_data['repo_info']
        files_content = repo_data['files_content']
        tech_analysis = repo_data['tech_analysis']
        
        # Technical level descriptions
        technical_levels = {
            "basic": "Use simple, clear language that any recruiter can understand. Focus on high-level technologies and basic functionalities.",
            "medium": "Include specific frameworks, libraries, and implementation details. Balance technical depth with accessibility.",
            "advanced": "Use industry-specific terminology. Emphasize architectural decisions, performance optimizations, and complex technical concepts."
        }
        
        # Output tone descriptions
        tone_styles = {
            "concise": "Create brief, impactful statements (15-20 words each). Focus on key achievements and technologies.",
            "detailed": "Provide comprehensive explanations with context and methodologies (25-35 words each).",
            "action-oriented": "Start with strong action verbs (Developed, Implemented, Architected, Optimized). Focus on accomplishments and measurable impact."
        }
        
        # Build the comprehensive prompt
        prompt = f"""
You are a senior technical recruiter and software engineering expert. Analyze this GitHub repository in detail and generate {request_data.get('num_points', 5)} exceptional resume bullet points that will impress hiring managers at top tech companies.

REPOSITORY DETAILS:
==================
Repository Name: {repo_info.get('name', 'Unknown')}
Description: {repo_info.get('description', 'No description available')}
Primary Language: {repo_info.get('language', 'Multiple languages')}
Repository Stats: {repo_info.get('stargazers_count', 0)} stars, {repo_info.get('forks_count', 0)} forks
Repository Size: {repo_info.get('size', 0)} KB
Branch Analyzed: {repo_data.get('branch_used', 'main')}
Created: {repo_info.get('created_at', 'Unknown')}
Last Updated: {repo_info.get('updated_at', 'Unknown')}

TECHNOLOGY STACK DETECTED:
=========================
Technologies: {', '.join(tech_analysis['technologies']) if tech_analysis['technologies'] else 'Not determined'}
Primary Language: {tech_analysis['primary_language']}

DETAILED CODE ANALYSIS:
======================
"""
        
        # Add file analysis
        for file_path, content in files_content.items():
            prompt += f"\n--- FILE: {file_path} ---\n"
            # Include first 1500 characters of each file for context
            file_preview = content[:1500]
            if len(content) > 1500:
                file_preview += "... [content continues]"
            prompt += file_preview + "\n"
        
        prompt += f"""

RESUME POINT REQUIREMENTS:
=========================
Technical Level: {request_data.get('technical_level', 'medium')} - {technical_levels.get(request_data.get('technical_level', 'medium'), '')}
Writing Style: {request_data.get('output_tone', 'action-oriented')} - {tone_styles.get(request_data.get('output_tone', 'action-oriented'), '')}
Number of Points: {request_data.get('num_points', 5)}

SPECIFIC INSTRUCTIONS:
=====================
1. Analyze the ACTUAL CODE FILES provided above - do not make generic assumptions
2. Identify specific technologies, frameworks, and implementation patterns from the code
3. Look for evidence of:
   - Architecture patterns (MVC, microservices, etc.)
   - Database usage and data modeling
   - API design and implementation
   - Frontend/backend integration
   - Testing strategies
   - Performance optimizations
   - Security implementations
   - DevOps practices (Docker, CI/CD, etc.)

4. Each bullet point MUST:
   - Start with a strong action verb (Developed, Implemented, Architected, Built, Designed, Optimized)
   - Reference specific technologies found in the code analysis
   - Describe the actual functionality implemented
   - Include scale/complexity indicators when evident from the code
   - Be unique and add distinct value

5. Base your points ONLY on evidence from the provided code files
6. If you see database schemas, mention data modeling
7. If you see API endpoints, mention API development
8. If you see frontend components, mention UI/UX development
9. If you see test files, mention testing implementation
10. If you see Docker/deployment files, mention DevOps practices

CRITICAL: Generate points based on ACTUAL ANALYSIS of the provided code, not generic software development activities.

Generate exactly {request_data.get('num_points', 5)} bullet points, each on a separate line starting with "•"
"""
        
        return prompt

    def _parse_points(self, text):
        """Parse AI response into clean bullet points"""
        points = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and headers
            if not line or line.startswith('#') or line.lower().startswith(('here are', 'based on', 'analysis')):
                continue
                
            # Extract bullet points
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                clean_point = line[1:].strip()
                if len(clean_point) > 30:  # Ensure substantial content
                    points.append(clean_point)
            elif len(line) > 30 and not line.endswith(':'):
                # Treat substantial lines as bullet points even without markers
                points.append(line)
        
        # Filter out low-quality points
        quality_points = []
        for point in points:
            # Skip overly generic points
            if any(generic in point.lower() for generic in [
                'software development', 'programming languages', 'worked on', 'participated in'
            ]):
                continue
            quality_points.append(point)
        
        return quality_points

    def _fallback_points(self, repo_data, request_data):
        """Generate fallback points based on repository analysis"""
        repo_info = repo_data['repo_info']
        tech_analysis = repo_data['tech_analysis']
        
        repo_name = repo_info.get('name', 'software application')
        primary_lang = tech_analysis['primary_language']
        technologies = tech_analysis['technologies']
        
        fallback_points = [
            f"Developed {repo_name} using {primary_lang} with focus on scalable architecture and maintainable code structure",
            f"Implemented comprehensive software solution leveraging {', '.join(technologies[:3]) if len(technologies) >= 3 else primary_lang} for enhanced functionality",
            f"Built robust {repo_name} application following software engineering best practices and design patterns",
            f"Designed and developed {repo_name} with emphasis on code quality, testing, and documentation standards",
            f"Created {repo_name} utilizing modern {primary_lang} development practices and industry-standard tools"
        ]
        
        return fallback_points[:request_data.get('num_points', 5)]

# Initialize services
code_analyzer = CodeAnalyzer()
resume_generator = ResumeGenerator()

@app.route('/')
def index():
    return jsonify({
        "message": "GitHub Resume Generator API v2.0",
        "features": ["Smart branch detection", "Comprehensive code analysis", "Tech stack detection", "Delete functionality"],
        "status": "operational"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/get-branches/<owner>/<repo>', methods=['GET'])
@firebase_auth_required
def get_branches(owner, repo):
    """Get available branches for a repository"""
    try:
        logger.info(f"User {request.user.get('uid')} requesting branches for {owner}/{repo}")
        branches = code_analyzer.github_client.get_branches(owner, repo)
        return jsonify({"branches": branches, "count": len(branches)})
    except Exception as e:
        logger.error(f"Error getting branches: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate-resume-points', methods=['POST'])
@firebase_auth_required
def generate_resume_points():
    """Generate resume points with comprehensive repository analysis"""
    start_time = time.time()
    user_uid = request.user.get('uid')
    
    try:
        data = request.json
        if not data or "github_url" not in data:
            return jsonify({"error": "Missing required parameter: github_url"}), 400

        logger.info(f"User {user_uid} requesting analysis for: {data.get('github_url')}")

        # Set defaults
        data.setdefault("num_points", 5)
        data.setdefault("technical_level", "medium")
        data.setdefault("output_tone", "action-oriented")

        # Perform comprehensive analysis
        branch = data.get("branch")
        logger.info(f"Analyzing repository with branch: {branch or 'auto-detect'}")
        
        repo_data = code_analyzer.analyze_repository(data["github_url"], branch)
        logger.info(f"Repository analysis complete: {repo_data['analysis_summary']}")
        
        # Generate resume points
        points = resume_generator.generate_points(repo_data, data)
        logger.info(f"Generated {len(points)} resume points")

        elapsed = f"{time.time() - start_time:.2f}s"

        response_data = {
            "points": points,
            "repository_info": {
                "name": repo_data["repo_info"]["name"],
                "description": repo_data["repo_info"].get("description"),
                "language": repo_data["repo_info"].get("language"),
                "stars": repo_data["repo_info"].get("stargazers_count", 0),
                "forks": repo_data["repo_info"].get("forks_count", 0),
                "size": repo_data["repo_info"].get("size", 0),
                "branch_used": repo_data.get("branch_used"),
                "available_branches": repo_data.get("available_branches", []),
                "created_at": repo_data["repo_info"].get("created_at"),
                "updated_at": repo_data["repo_info"].get("updated_at")
            },
            "analysis_details": {
                "technologies_detected": repo_data["tech_analysis"]["technologies"],
                "total_files_analyzed": repo_data["analysis_summary"]["total_files_analyzed"],
                "primary_language": repo_data["tech_analysis"]["primary_language"]
            },
            "processing_time": elapsed,
            "user_settings": {
                "num_points": data["num_points"],
                "technical_level": data["technical_level"],
                "output_tone": data["output_tone"]
            }
        }

        logger.info(f"Successfully generated resume points for {user_uid} in {elapsed}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error during resume points generation for user {user_uid}: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": str(e),
            "processing_time": f"{time.time() - start_time:.2f}s"
        }), 500

@app.route('/history', methods=['GET'])
@firebase_auth_required
def get_history():
    """Get user's resume generation history"""
    try:
        user_uid = request.user.get('uid')
        logger.info(f"Fetching history for user: {user_uid}")
        
        # Query Firestore for user's history
        docs = db.collection('repo_histories').where('uid', '==', user_uid).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(50).stream()
        
        history = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            history.append(data)
        
        logger.info(f"Retrieved {len(history)} history items for user {user_uid}")
        return jsonify({"history": history, "count": len(history)})
        
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/history/<history_id>', methods=['DELETE'])
@firebase_auth_required
def delete_history_item(history_id):
    """Delete a specific history item"""
    try:
        user_uid = request.user.get('uid')
        logger.info(f"User {user_uid} deleting history item: {history_id}")
        
        # Get the document first to verify ownership
        doc_ref = db.collection('repo_histories').document(history_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({"error": "History item not found"}), 404
        
        doc_data = doc.to_dict()
        if doc_data.get('uid') != user_uid:
            return jsonify({"error": "Unauthorized: Cannot delete another user's history"}), 403
        
        # Delete the document
        doc_ref.delete()
        logger.info(f"Successfully deleted history item {history_id} for user {user_uid}")
        
        return jsonify({
            "message": "History item deleted successfully",
            "deleted_id": history_id
        })
        
    except Exception as e:
        logger.error(f"Error deleting history item: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/history/clear', methods=['DELETE'])
@firebase_auth_required
def clear_all_history():
    """Clear all history for the authenticated user"""
    try:
        user_uid = request.user.get('uid')
        logger.info(f"User {user_uid} clearing all history")
        
        # Get all documents for this user
        docs = db.collection('repo_histories').where('uid', '==', user_uid).stream()
        
        deleted_count = 0
        batch = db.batch()
        
        for doc in docs:
            batch.delete(doc.reference)
            deleted_count += 1
        
        # Commit the batch delete
        batch.commit()
        
        logger.info(f"Successfully deleted {deleted_count} history items for user {user_uid}")
        
        return jsonify({
            "message": f"Successfully cleared {deleted_count} history items",
            "deleted_count": deleted_count
        })
        
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
@firebase_auth_required
def get_user_stats():
    """Get usage statistics for the authenticated user"""
    try:
        user_uid = request.user.get('uid')
        
        # Get user's history count
        docs = db.collection('repo_histories').where('uid', '==', user_uid).stream()
        
        total_generations = 0
        languages_used = set()
        repositories = set()
        
        for doc in docs:
            data = doc.to_dict()
            total_generations += 1
            
            if data.get('repository_info', {}).get('language'):
                languages_used.add(data['repository_info']['language'])
            
            if data.get('github_url'):
                repositories.add(data['github_url'])
        
        stats = {
            "total_generations": total_generations,
            "unique_repositories": len(repositories),
            "languages_used": list(languages_used),
            "languages_count": len(languages_used)
        }
        
        return jsonify({"stats": stats})
        
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("🚀 Starting GitHub Resume Generator API v2.0")
    logger.info("📋 Features: Enhanced analysis, tech stack detection, delete functionality")
    logger.info("🔧 Make sure Firebase Admin SDK key is properly configured")
    app.run(host="0.0.0.0", port=8000, debug=True)