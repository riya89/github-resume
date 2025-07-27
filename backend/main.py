# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# import base64
# import google.generativeai as genai
# import os
# import logging
# import traceback
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

# # Configure Gemini API
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     print("Warning: GEMINI_API_KEY not found in environment variables")
#     GEMINI_API_KEY = "your-gemini-api-key-here"

# genai.configure(api_key=GEMINI_API_KEY)

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GitHubClient:
#     def __init__(self):
#         self.base_url = "https://api.github.com"
        
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
#         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}")
#         if response.status_code != 200:
#             raise Exception("Repository not found")
#         return response.json()
    
#     def get_repository_contents(self, owner: str, repo: str, path: str = ""):
#         """Get repository contents"""
#         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/contents/{path}")
#         if response.status_code != 200:
#             return []
#         return response.json()
    
#     def get_file_content(self, owner: str, repo: str, file_path: str):
#         """Get content of a specific file"""
#         response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}")
#         if response.status_code != 200:
#             return None
        
#         file_data = response.json()
#         if file_data.get('encoding') == 'base64':
#             try:
#                 content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
#                 return content
#             except:
#                 return None
#         return file_data.get('content', '')

# class CodeAnalyzer:
#     def __init__(self):
#         self.github_client = GitHubClient()
#         self.important_files = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb']
    
#     def analyze_repository(self, github_url: str):
#         """Analyze repository and extract relevant code and structure"""
#         owner, repo = self.github_client.extract_repo_info(github_url)
        
#         # Get basic repo info
#         repo_info = self.github_client.get_repository_info(owner, repo)
        
#         # Get repository structure and important files
#         files_content = self._get_important_files(owner, repo)
        
#         return {
#             'repo_info': repo_info,
#             'files_content': files_content,
#             'owner': owner,
#             'repo_name': repo
#         }
    
#     def _get_important_files(self, owner: str, repo: str, max_files: int = 10):
#         """Get content of important files from the repository"""
#         files_content = {}
        
#         try:
#             contents = self.github_client.get_repository_contents(owner, repo)
#             if not contents:
#                 return files_content
            
#             priority_files = []
#             code_files = []
            
#             for item in contents:
#                 if item['type'] == 'file':
#                     filename = item['name']
#                     if filename.lower() in ['readme.md', 'package.json', 'requirements.txt', 'dockerfile']:
#                         priority_files.append(item)
#                     elif any(filename.endswith(ext) for ext in self.important_files):
#                         code_files.append(item)
            
#             # Process priority files first
#             for item in priority_files[:3]:
#                 content = self.github_client.get_file_content(owner, repo, item['path'])
#                 if content:
#                     files_content[item['path']] = content[:3000]  # Limit content
            
#             # Then process code files
#             remaining_slots = max_files - len(files_content)
#             for item in code_files[:remaining_slots]:
#                 content = self.github_client.get_file_content(owner, repo, item['path'])
#                 if content:
#                     files_content[item['path']] = content[:3000]  # Limit content
            
#         except Exception as e:
#             logger.error(f"Error getting repository files: {e}")
        
#         return files_content

# class ResumePointsGenerator:
#     def __init__(self):
#         try:
#             self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
#             logger.info("Gemini 2.0 Flash model initialized successfully")
#         except Exception as e:
#             logger.error(f"Failed to initialize Gemini 2.0 Flash: {e}")
#             try:
#                 self.model = genai.GenerativeModel('gemini-pro')
#                 logger.info("Using gemini-pro as fallback")
#             except Exception as e2:
#                 logger.error(f"Failed to initialize fallback model: {e2}")
#                 raise Exception("Could not initialize any Gemini model")
    
#     def create_prompt(self, repo_data: dict, request_data: dict):
#         """Create a detailed prompt for Gemini"""
#         repo_info = repo_data['repo_info']
#         files_content = repo_data['files_content']
        
#         context = f"""
# Repository: {repo_info.get('name', 'Unknown')}
# Description: {repo_info.get('description', 'No description')}
# Language: {repo_info.get('language', 'Multiple')}
# Stars: {repo_info.get('stargazers_count', 0)}
# Forks: {repo_info.get('forks_count', 0)}

# Files analyzed:
# """
        
#         for file_path, content in files_content.items():
#             context += f"\n--- {file_path} ---\n{content[:800]}...\n"
        
#         technical_depth = {
#             "basic": "Focus on high-level technologies and basic functionalities",
#             "medium": "Include specific frameworks, libraries, and implementation details", 
#             "advanced": "Emphasize complex algorithms, architectures, performance optimizations"
#         }
        
#         tone_style = {
#             "concise": "Use brief, impactful statements",
#             "detailed": "Provide comprehensive explanations with context",
#             "action-oriented": "Start with strong action verbs and focus on achievements"
#         }
        
#         num_points = request_data.get('num_points', 5)
#         technical_level = request_data.get('technical_level', 'medium')
#         output_tone = request_data.get('output_tone', 'action-oriented')
        
#         prompt = f"""
# Based on the GitHub repository analysis above, generate {num_points} professional resume bullet points.

# Requirements:
# - Technical Level: {technical_level} - {technical_depth.get(technical_level, '')}
# - Tone: {output_tone} - {tone_style.get(output_tone, '')}
# - Focus on technical achievements and implementation details
# - Use quantifiable metrics where possible
# - Highlight technologies, frameworks, and methodologies used
# - Each point should be a complete, professional resume bullet point

# Format each point as a separate line starting with "•"

# Context: {context}
# """
        
#         return prompt
    
#     def generate_points(self, repo_data: dict, request_data: dict):
#         """Generate resume points using Gemini"""
#         prompt = self.create_prompt(repo_data, request_data)
        
#         try:
#             logger.info("Generating content with Gemini...")
#             response = self.model.generate_content(prompt)
            
#             logger.info("Content generated successfully")
            
#             points = []
#             if response.text:
#                 lines = response.text.strip().split('\n')
#                 for line in lines:
#                     line = line.strip()
#                     if line.startswith('•') or line.startswith('-') or line.startswith('*'):
#                         points.append(line[1:].strip())
#                     elif line and not line.startswith('#') and len(line) > 15:
#                         points.append(line)
            
#             # Filter out empty or very short points
#             points = [point for point in points if len(point.strip()) > 25]
            
#             num_points = request_data.get('num_points', 5)
#             if len(points) < num_points:
#                 # Generate additional generic points if needed
#                 repo_language = repo_data['repo_info'].get('language', 'multiple programming languages')
#                 additional_points = [
#                     f"Developed and maintained software applications using {repo_language}",
#                     "Implemented version control best practices using Git for collaborative development",
#                     "Designed and built scalable software solutions following industry best practices",
#                     "Collaborated with team members to deliver high-quality code and documentation",
#                     "Utilized modern development tools and methodologies to improve code quality"
#                 ]
#                 points.extend(additional_points[:num_points - len(points)])
            
#             return points[:num_points]
            
#         except Exception as e:
#             logger.error(f"Error in generate_points: {str(e)}")
#             logger.error(f"Traceback: {traceback.format_exc()}")
            
#             # Return fallback points if AI generation fails
#             repo_language = repo_data['repo_info'].get('language', 'multiple programming languages')
#             fallback_points = [
#                 f"Developed software project using {repo_language} with focus on clean code practices",
#                 "Implemented version control and collaborative development practices using Git",
#                 "Built and maintained application codebase following software engineering best practices",
#                 "Designed software architecture and implemented key features for enhanced functionality",
#                 "Utilized modern development tools and frameworks for efficient software development"
#             ]
            
#             return fallback_points[:request_data.get('num_points', 5)]

# # Initialize services
# code_analyzer = CodeAnalyzer()
# resume_generator = ResumePointsGenerator()

# @app.route('/')
# def root():
#     return jsonify({"message": "GitHub Resume Points Generator API"})

# @app.route('/health')
# def health_check():
#     return jsonify({"status": "healthy"})

# @app.route('/generate-resume-points', methods=['POST'])
# def generate_resume_points():
#     """Generate resume points from GitHub repository"""
#     start_time = time.time()
    
#     try:
#         request_data = request.get_json()
        
#         if not request_data or 'github_url' not in request_data:
#             return jsonify({"error": "github_url is required"}), 400
        
#         logger.info(f"Processing request for: {request_data.get('github_url')}")
        
#         # Set defaults
#         request_data.setdefault('num_points', 5)
#         request_data.setdefault('technical_level', 'medium')
#         request_data.setdefault('output_tone', 'action-oriented')
        
#         # Analyze the repository
#         repo_data = code_analyzer.analyze_repository(request_data['github_url'])
#         logger.info("Repository analysis completed")
        
#         # Generate resume points
#         points = resume_generator.generate_points(repo_data, request_data)
#         logger.info("Resume points generated successfully")
        
#         processing_time = f"{time.time() - start_time:.2f}s"
        
#         return jsonify({
#             "points": points,
#             "repository_info": {
#                 "name": repo_data['repo_info'].get('name'),
#                 "description": repo_data['repo_info'].get('description'),
#                 "language": repo_data['repo_info'].get('language'),
#                 "stars": repo_data['repo_info'].get('stargazers_count', 0),
#                 "forks": repo_data['repo_info'].get('forks_count', 0)
#             },
#             "processing_time": processing_time
#         })
        
#     except Exception as e:
#         logger.error(f"Error in generate_resume_points: {str(e)}")
#         logger.error(f"Traceback: {traceback.format_exc()}")
#         return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# if __name__ == "__main__":
#     print("🚀 Starting GitHub Resume Points Generator API")
#     print("📍 Running on http://localhost:8000")
#     print("🔧 Make sure GEMINI_API_KEY is set in your .env file")
#     app.run(host="0.0.0.0", port=8000, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import google.generativeai as genai
import os
import logging
import traceback
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    GEMINI_API_KEY = "your-gemini-api-key-here"

genai.configure(api_key=GEMINI_API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        
    def extract_repo_info(self, github_url: str):
        """Extract owner and repo name from GitHub URL"""
        url_parts = str(github_url).rstrip('/').split('/')
        if len(url_parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        
        owner = url_parts[-2]
        repo = url_parts[-1]
        return owner, repo
    
    def get_repository_info(self, owner: str, repo: str):
        """Get basic repository information"""
        response = requests.get(f"{self.base_url}/repos/{owner}/{repo}")
        if response.status_code != 200:
            raise Exception("Repository not found")
        return response.json()
    
    def get_branches(self, owner: str, repo: str):
        """Get all branches of the repository"""
        try:
            response = requests.get(f"{self.base_url}/repos/{owner}/{repo}/branches")
            if response.status_code == 200:
                branches = response.json()
                return [branch['name'] for branch in branches]
            return []
        except Exception as e:
            logger.error(f"Error fetching branches: {e}")
            return []
    
    def get_repository_contents(self, owner: str, repo: str, path: str = "", branch: str = None):
        """Get repository contents from specific branch"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        if branch:
            url += f"?ref={branch}"
        
        response = requests.get(url)
        if response.status_code != 200:
            return []
        return response.json()
    
    def get_file_content(self, owner: str, repo: str, file_path: str, branch: str = None):
        """Get content of a specific file from specific branch"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{file_path}"
        if branch:
            url += f"?ref={branch}"
            
        response = requests.get(url)
        if response.status_code != 200:
            return None
        
        file_data = response.json()
        if file_data.get('encoding') == 'base64':
            try:
                content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
                return content
            except:
                return None
        return file_data.get('content', '')
    
    def find_best_branch(self, owner: str, repo: str):
        """Find the most active/content-rich branch"""
        branches = self.get_branches(owner, repo)
        if not branches:
            return None
        
        # Score branches based on content
        branch_scores = {}
        
        for branch in branches[:5]:  # Check max 5 branches to avoid rate limits
            try:
                contents = self.get_repository_contents(owner, repo, "", branch)
                if contents:
                    # Score based on number of files and presence of code files
                    score = len(contents)
                    
                    for item in contents:
                        if item['type'] == 'file':
                            filename = item['name'].lower()
                            # Boost score for important files
                            if any(filename.endswith(ext) for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.go']):
                                score += 5
                            elif filename in ['package.json', 'requirements.txt', 'dockerfile', 'makefile']:
                                score += 3
                            elif filename.endswith('.md'):
                                score += 1
                    
                    branch_scores[branch] = score
                    
            except Exception as e:
                logger.error(f"Error analyzing branch {branch}: {e}")
                continue
        
        if branch_scores:
            best_branch = max(branch_scores.items(), key=lambda x: x[1])
            logger.info(f"Best branch found: {best_branch[0]} (score: {best_branch[1]})")
            return best_branch[0]
        
        # Fallback to common branch names
        priority_branches = ['main', 'master', 'develop', 'dev']
        for branch in priority_branches:
            if branch in branches:
                return branch
                
        return branches[0] if branches else None

class CodeAnalyzer:
    def __init__(self):
        self.github_client = GitHubClient()
        self.important_files = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb', '.swift', '.kt']
    
    def analyze_repository(self, github_url: str, branch: str = None):
        """Analyze repository and extract relevant code and structure"""
        owner, repo = self.github_client.extract_repo_info(github_url)
        
        # Get basic repo info
        repo_info = self.github_client.get_repository_info(owner, repo)
        
        # Find best branch if not specified
        if not branch:
            branch = self.github_client.find_best_branch(owner, repo)
            logger.info(f"Using branch: {branch}")
        
        # Get repository structure and important files
        files_content = self._get_important_files(owner, repo, branch)
        
        # Get branch information
        branches = self.github_client.get_branches(owner, repo)
        
        return {
            'repo_info': repo_info,
            'files_content': files_content,
            'owner': owner,
            'repo_name': repo,
            'branch_used': branch,
            'available_branches': branches
        }
    
    def _get_important_files(self, owner: str, repo: str, branch: str, max_files: int = 12):
        """Get content of important files from the repository"""
        files_content = {}
        
        try:
            contents = self.github_client.get_repository_contents(owner, repo, "", branch)
            if not contents:
                return files_content
            
            # Categorize files
            priority_files = []  # README, config files
            code_files = []      # Source code files
            config_files = []    # Package managers, build files
            
            for item in contents:
                if item['type'] == 'file':
                    filename = item['name'].lower()
                    
                    if filename.startswith('readme'):
                        priority_files.insert(0, item)  # README gets highest priority
                    elif filename in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 'composer.json', 'gemfile', 'cargo.toml']:
                        config_files.append(item)
                    elif filename in ['dockerfile', 'docker-compose.yml', 'makefile', '.gitignore']:
                        config_files.append(item)
                    elif any(filename.endswith(ext) for ext in self.important_files):
                        code_files.append(item)
            
            # Process files in order of importance
            files_to_process = priority_files[:2] + config_files[:3] + code_files[:7]
            
            for item in files_to_process:
                if len(files_content) >= max_files:
                    break
                    
                content = self.github_client.get_file_content(owner, repo, item['path'], branch)
                if content and len(content.strip()) > 0:
                    # Limit content size but preserve structure
                    if len(content) > 4000:
                        content = content[:4000] + "\n... [truncated]"
                    files_content[item['path']] = content
            
            logger.info(f"Analyzed {len(files_content)} files from branch '{branch}'")
            
        except Exception as e:
            logger.error(f"Error getting repository files: {e}")
        
        return files_content

class ResumePointsGenerator:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Gemini 2.0 Flash model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini 2.0 Flash: {e}")
            try:
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Using gemini-pro as fallback")
            except Exception as e2:
                logger.error(f"Failed to initialize fallback model: {e2}")
                raise Exception("Could not initialize any Gemini model")
    
    def create_enhanced_prompt(self, repo_data: dict, request_data: dict):
        """Create an enhanced, detailed prompt for better resume points"""
        repo_info = repo_data['repo_info']
        files_content = repo_data['files_content']
        branch_used = repo_data.get('branch_used', 'main')
        
        # Analyze tech stack from files
        tech_stack = self._analyze_tech_stack(files_content)
        project_complexity = self._assess_project_complexity(repo_info, files_content)
        
        context = f"""
REPOSITORY ANALYSIS:
==================
Repository: {repo_info.get('name', 'Unknown')}
Description: {repo_info.get('description', 'No description available')}
Primary Language: {repo_info.get('language', 'Not specified')}
Repository Stats: {repo_info.get('stargazers_count', 0)} stars, {repo_info.get('forks_count', 0)} forks
Branch Analyzed: {branch_used}
Project Size: {repo_info.get('size', 0)} KB
Last Updated: {repo_info.get('updated_at', 'Unknown')}

TECHNOLOGY STACK IDENTIFIED:
{tech_stack}

PROJECT COMPLEXITY ASSESSMENT:
{project_complexity}

CODE ANALYSIS:
=============
"""
        
        for file_path, content in files_content.items():
            context += f"\n--- {file_path} ---\n{content[:1200]}\n"
        
        technical_levels = {
            "basic": "Focus on technologies used and basic functionalities implemented. Use simple, clear language that any recruiter can understand.",
            "medium": "Include specific frameworks, libraries, design patterns, and implementation approaches. Balance technical depth with accessibility.",
            "advanced": "Emphasize architectural decisions, performance optimizations, complex algorithms, scalability considerations, and advanced technical concepts. Use industry-specific terminology."
        }
        
        tone_styles = {
            "concise": "Create brief, impactful statements (10-15 words each). Focus on key achievements and technologies.",
            "detailed": "Provide comprehensive explanations with context, methodologies, and outcomes (20-30 words each).",
            "action-oriented": "Start with strong action verbs (Developed, Implemented, Designed, Built, Optimized). Focus on accomplishments and measurable impact."
        }
        
        num_points = request_data.get('num_points', 5)
        technical_level = request_data.get('technical_level', 'medium')
        output_tone = request_data.get('output_tone', 'action-oriented')
        
        prompt = f"""
As a senior technical recruiter and software engineering expert, analyze this GitHub repository and generate {num_points} exceptional resume bullet points that will impress hiring managers at top tech companies.

REQUIREMENTS:
============
- Technical Level: {technical_level} - {technical_levels.get(technical_level)}
- Writing Style: {output_tone} - {tone_styles.get(output_tone)}
- Each bullet point should be a complete, professional resume entry
- Include specific technologies, frameworks, and methodologies identified in the code
- Quantify impact where possible (performance improvements, scale, complexity)
- Highlight problem-solving abilities and technical decision-making
- Make each point unique and valuable to potential employers

BULLET POINT CRITERIA:
=====================
1. Start with a strong action verb (Developed, Implemented, Architected, Optimized, etc.)
2. Specify the technology stack and tools used
3. Describe the functionality or problem solved
4. Include scale, complexity, or impact metrics when available
5. Use industry-standard terminology
6. Ensure each point adds unique value

CONTEXT TO ANALYZE:
{context}

Generate exactly {num_points} bullet points, each on a separate line starting with "•"

Focus on making these bullet points stand out to recruiters and demonstrate real software engineering expertise.
"""
        
        return prompt
    
    def _analyze_tech_stack(self, files_content: dict) -> str:
        """Analyze and categorize the technology stack"""
        tech_stack = {
            "Frontend": set(),
            "Backend": set(),
            "Database": set(),
            "DevOps/Tools": set(),
            "Languages": set()
        }
        
        # File extension to technology mapping
        tech_mapping = {
            '.js': 'JavaScript', '.jsx': 'React/JSX', '.ts': 'TypeScript', '.tsx': 'React/TypeScript',
            '.py': 'Python', '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.go': 'Go',
            '.rs': 'Rust', '.php': 'PHP', '.rb': 'Ruby', '.swift': 'Swift', '.kt': 'Kotlin'
        }
        
        for file_path, content in files_content.items():
            filename = file_path.lower()
            content_lower = content.lower()
            
            # Detect by file extension
            for ext, lang in tech_mapping.items():
                if filename.endswith(ext):
                    tech_stack["Languages"].add(lang)
            
            # Detect frameworks and libraries from content
            if 'package.json' in filename:
                if 'react' in content_lower: tech_stack["Frontend"].add('React')
                if 'vue' in content_lower: tech_stack["Frontend"].add('Vue.js')
                if 'angular' in content_lower: tech_stack["Frontend"].add('Angular')
                if 'express' in content_lower: tech_stack["Backend"].add('Express.js')
                if 'next' in content_lower: tech_stack["Frontend"].add('Next.js')
                
            if 'requirements.txt' in filename or filename.endswith('.py'):
                if 'django' in content_lower: tech_stack["Backend"].add('Django')
                if 'flask' in content_lower: tech_stack["Backend"].add('Flask')
                if 'fastapi' in content_lower: tech_stack["Backend"].add('FastAPI')
                if 'tensorflow' in content_lower: tech_stack["Backend"].add('TensorFlow')
                if 'pytorch' in content_lower: tech_stack["Backend"].add('PyTorch')
                
            if 'dockerfile' in filename:
                tech_stack["DevOps/Tools"].add('Docker')
                
            # Database detection
            if any(db in content_lower for db in ['postgresql', 'postgres']):
                tech_stack["Database"].add('PostgreSQL')
            if 'mongodb' in content_lower or 'mongo' in content_lower:
                tech_stack["Database"].add('MongoDB')
            if 'mysql' in content_lower:
                tech_stack["Database"].add('MySQL')
            if 'redis' in content_lower:
                tech_stack["Database"].add('Redis')
        
        # Format tech stack summary
        summary = []
        for category, techs in tech_stack.items():
            if techs:
                summary.append(f"{category}: {', '.join(sorted(techs))}")
        
        return '\n'.join(summary) if summary else "Technology stack could not be fully determined from available files."
    
    def _assess_project_complexity(self, repo_info: dict, files_content: dict) -> str:
        """Assess project complexity and scale"""
        complexity_indicators = []
        
        # Repository metrics
        stars = repo_info.get('stargazers_count', 0)
        forks = repo_info.get('forks_count', 0)
        size = repo_info.get('size', 0)
        
        if stars > 100:
            complexity_indicators.append(f"Popular open-source project ({stars} stars)")
        if forks > 20:
            complexity_indicators.append(f"Community-driven development ({forks} forks)")
        if size > 10000:  # > 10MB
            complexity_indicators.append("Large-scale codebase")
        
        # Code complexity analysis
        file_count = len(files_content)
        total_lines = sum(len(content.split('\n')) for content in files_content.values())
        
        if file_count > 10:
            complexity_indicators.append("Multi-file architecture")
        if total_lines > 1000:
            complexity_indicators.append(f"Substantial codebase (~{total_lines} lines analyzed)")
        
        # Technical complexity
        has_config_files = any('package.json' in f or 'requirements.txt' in f or 'dockerfile' in f.lower() 
                              for f in files_content.keys())
        if has_config_files:
            complexity_indicators.append("Production-ready configuration")
        
        return '; '.join(complexity_indicators) if complexity_indicators else "Standard project complexity"
    
    def generate_points(self, repo_data: dict, request_data: dict):
        """Generate enhanced resume points using Gemini"""
        prompt = self.create_enhanced_prompt(repo_data, request_data)
        
        try:
            logger.info("Generating enhanced resume points with Gemini...")
            response = self.model.generate_content(prompt)
            
            logger.info("Content generated successfully")
            
            points = []
            if response.text:
                lines = response.text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                        clean_point = line[1:].strip()
                        if len(clean_point) > 30:  # Ensure substantial content
                            points.append(clean_point)
                    elif line and not line.startswith('#') and len(line) > 30:
                        points.append(line)
            
            # Filter and enhance points
            points = [point for point in points if len(point.strip()) > 30 and not point.lower().startswith(('generate', 'create', 'here are'))]
            
            num_points = request_data.get('num_points', 5)
            if len(points) < num_points:
                # Generate enhanced fallback points
                repo_name = repo_data['repo_info'].get('name', 'software project')
                repo_language = repo_data['repo_info'].get('language', 'modern programming languages')
                
                enhanced_fallbacks = [
                    f"Developed {repo_name} using {repo_language} with emphasis on clean code architecture and best practices",
                    f"Implemented comprehensive version control workflow using Git for collaborative development of {repo_name}",
                    f"Designed and built scalable software architecture for {repo_name} following industry-standard design patterns",
                    f"Collaborated on {repo_name} development using modern software engineering methodologies and code review processes",
                    f"Optimized {repo_name} performance and maintainability through refactoring and technical debt reduction"
                ]
                
                points.extend(enhanced_fallbacks[:num_points - len(points)])
            
            return points[:num_points]
            
        except Exception as e:
            logger.error(f"Error in generate_points: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Enhanced fallback points
            repo_name = repo_data['repo_info'].get('name', 'software application')
            repo_language = repo_data['repo_info'].get('language', 'modern programming technologies')
            
            fallback_points = [
                f"Developed {repo_name} using {repo_language} with focus on scalable architecture and code quality",
                f"Implemented robust version control and collaborative development practices using Git for {repo_name}",
                f"Built comprehensive software solution {repo_name} following software engineering best practices and design patterns",
                f"Designed technical architecture and implemented core features for {repo_name} with emphasis on maintainability",
                f"Utilized modern development tools and methodologies to deliver high-quality {repo_name} solution"
            ]
            
            return fallback_points[:request_data.get('num_points', 5)]

# Initialize services
code_analyzer = CodeAnalyzer()
resume_generator = ResumePointsGenerator()

@app.route('/')
def root():
    return jsonify({"message": "GitHub Resume Points Generator API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/get-branches/<owner>/<repo>')
def get_branches(owner, repo):
    """Get available branches for a repository"""
    try:
        branches = code_analyzer.github_client.get_branches(owner, repo)
        return jsonify({"branches": branches})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-resume-points', methods=['POST'])
def generate_resume_points():
    """Generate resume points from GitHub repository"""
    start_time = time.time()
    
    try:
        request_data = request.get_json()
        
        if not request_data or 'github_url' not in request_data:
            return jsonify({"error": "github_url is required"}), 400
        
        logger.info(f"Processing request for: {request_data.get('github_url')}")
        
        # Set defaults
        request_data.setdefault('num_points', 5)
        request_data.setdefault('technical_level', 'medium')
        request_data.setdefault('output_tone', 'action-oriented')
        
        # Extract branch from request (optional)
        branch = request_data.get('branch', None)
        
        # Analyze the repository
        repo_data = code_analyzer.analyze_repository(request_data['github_url'], branch)
        logger.info(f"Repository analysis completed using branch: {repo_data.get('branch_used')}")
        
        # Generate resume points
        points = resume_generator.generate_points(repo_data, request_data)
        logger.info("Enhanced resume points generated successfully")
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        return jsonify({
            "points": points,
            "repository_info": {
                "name": repo_data['repo_info'].get('name'),
                "description": repo_data['repo_info'].get('description'),
                "language": repo_data['repo_info'].get('language'),
                "stars": repo_data['repo_info'].get('stargazers_count', 0),
                "forks": repo_data['repo_info'].get('forks_count', 0),
                "branch_used": repo_data.get('branch_used'),
                "available_branches": repo_data.get('available_branches', [])
            },
            "processing_time": processing_time
        })
        
    except Exception as e:
        logger.error(f"Error in generate_resume_points: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    print("🚀 Starting Enhanced GitHub Resume Points Generator API")
    print("📍 Running on http://localhost:8000")
    print("🔧 Features: Smart branch detection, enhanced prompts, tech stack analysis")
    print("🌟 Make sure GEMINI_API_KEY is set in your .env file")
    app.run(host="0.0.0.0", port=8000, debug=True)
    