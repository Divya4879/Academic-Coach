import requests
import json
from typing import Dict, List, Optional
import re

class ContentGenerator:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.groq_api_key = None
        
        if api_keys.get('GROQ_API_KEY'):
            try:
                self.groq_api_key = api_keys['GROQ_API_KEY']
                self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
                self.groq_model = "llama3-8b-8192"
                print("✅ Groq API configured successfully")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
                self.groq_api_key = None
        else:
            print("⚠️ No Groq API key provided")
        
        if not self.groq_api_key:
            print("⚠️ No AI APIs available - using mock responses")

    def generate_comprehensive_content(self, academic_level: str, subject: str, topic: str) -> Dict:
        """
        Generate comprehensive educational content with structure and references
        """
        try:
            content_prompt = self._create_content_prompt(academic_level, subject, topic)
            
            content = self._get_ai_response(content_prompt)
            
            parsed_content = self._parse_generated_content(content)
            references = self._generate_references(academic_level, subject, topic)
            key_points = self._extract_key_points(parsed_content['content'])
            
            return {
                'content': parsed_content['content'],
                'structure': parsed_content['structure'],
                'references': references,
                'key_points': key_points,
                'word_count': len(parsed_content['content'].split()),
                'academic_level': academic_level,
                'subject': subject,
                'topic': topic
            }
            
        except Exception as e:
            print(f"❌ Content generation error: {e}")
            raise

    def _create_content_prompt(self, academic_level: str, subject: str, topic: str) -> str:
        """
        Create a detailed prompt for content generation
        """
        return f"""
You are a globally renowned educator with expertise in {subject}. Create a comprehensive, well-structured educational in-depth explanation about "{topic}" for {academic_level} level students.

Requirements:
1. Write 2000-3000 words
2. Structure with clear numbered topics and sub-topics
3. Use appropriate academic language for {academic_level} level
4. Include practical examples and applications
5. Make it engaging and educational
6. Use proper formatting with headers and bullet points

Structure your response as:

# {topic}

## 1. Introduction and Overview
[Comprehensive introduction explaining what the topic is and why it's important]

## 2. Fundamental Concepts
[Core concepts and definitions]
### 2.1 [Subtopic]
### 2.2 [Subtopic]

## 3. Detailed Analysis
[In-depth exploration of the topic]
### 3.1 [Subtopic]
### 3.2 [Subtopic]
### 3.3 [Subtopic]

## 4. Practical Applications and Examples
[Real-world applications and detailed examples]

## 5. Advanced Concepts
[More complex aspects for deeper understanding]

## 6. Current Research and Developments
[Latest developments and research in the field]

## 7. Conclusion and Key Takeaways
[Summary of main points and their significance]

Make sure the content is:
- Academically rigorous for {academic_level} level
- Well-researched and factually accurate
- Engaging with clear explanations
- Rich in examples and applications
- Properly structured and numbered
"""

    def _get_groq_response(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 4000
            }
            
            response = requests.post(self.groq_api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"⚠️ Groq API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            return None
    
    def _get_ai_response(self, prompt: str) -> str:
        try:
            if self.groq_api_key:
                groq_response = self._get_groq_response(prompt)
                if groq_response:
                    return groq_response
            
            return self._generate_mock_response(prompt)
                
        except Exception as e:
            print(f"⚠️ AI API Error: {e}")
            return self._generate_mock_response(prompt)
    
    def _generate_mock_response(self, prompt: str) -> str:
        return f"""
# Sample Educational Content

## 1. Introduction and Overview
This is a sample response when no AI APIs are available. Please configure your Groq API key properly.

## 2. Fundamental Concepts
- Key concept 1: Basic understanding required
- Key concept 2: Building blocks of the topic
- Key concept 3: Foundation for advanced learning

## 3. Detailed Analysis
### 3.1 First Analysis Point
Detailed explanation would be provided here with proper academic depth.

### 3.2 Second Analysis Point
More detailed explanation with examples and applications.

### 3.3 Third Analysis Point
Additional analysis with real-world connections.

## 4. Practical Applications and Examples
Real-world examples and practical applications would be provided here to help students understand the relevance.

## 5. Advanced Concepts
Advanced topics for deeper understanding would be covered in this section.

## 6. Current Research and Developments
Latest research and developments in the field would be discussed here.

## 7. Conclusion and Key Takeaways
Summary of main points and their significance for the student's learning journey.
"""

    def _parse_generated_content(self, content: str) -> Dict:
        """
        Parse the generated content to extract structure
        """
        lines = content.split('\n')
        structure = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('## '):
                current_section = {
                    'title': line.replace('## ', ''),
                    'subsections': []
                }
                structure.append(current_section)
            elif line.startswith('### ') and current_section:
                current_section['subsections'].append(line.replace('### ', ''))
        
        return {
            'content': content,
            'structure': structure
        }

    def _generate_references(self, academic_level: str, subject: str, topic: str) -> List[Dict]:
        """
        Generate realistic reference links based on the topic
        """
        references = []
        
        base_references = {
            'high_school': [
                {
                    'title': f'{topic} - Khan Academy',
                    'url': f'https://www.khanacademy.org/search?search_again=1&page_search_query={topic.replace(" ", "%20")}',
                    'type': 'Educational Resource'
                },
                {
                    'title': f'{topic} - Britannica',
                    'url': f'https://www.britannica.com/search?query={topic.replace(" ", "+")}',
                    'type': 'Encyclopedia'
                },
                {
                    'title': f'{subject}: {topic} - National Geographic Education',
                    'url': f'https://education.nationalgeographic.org/resource/{topic.lower().replace(" ", "-")}',
                    'type': 'Educational Article'
                }
            ],
            'undergraduate': [
                {
                    'title': f'{topic} - MIT OpenCourseWare',
                    'url': f'https://ocw.mit.edu/search/?q={topic.replace(" ", "+")}',
                    'type': 'Academic Course'
                },
                {
                    'title': f'{topic} - Stanford Encyclopedia of Philosophy',
                    'url': f'https://plato.stanford.edu/search/searcher.py?query={topic.replace(" ", "+")}',
                    'type': 'Academic Reference'
                },
                {
                    'title': f'{subject} and {topic} - Coursera',
                    'url': f'https://www.coursera.org/search?query={topic.replace(" ", "%20")}',
                    'type': 'Online Course'
                },
                {
                    'title': f'{topic} Research - Google Scholar',
                    'url': f'https://scholar.google.com/scholar?q={topic.replace(" ", "+")}',
                    'type': 'Academic Papers'
                }
            ],
            'graduate': [
                {
                    'title': f'{topic} - Nature Journal',
                    'url': f'https://www.nature.com/search?q={topic.replace(" ", "+")}',
                    'type': 'Scientific Journal'
                },
                {
                    'title': f'{topic} Research - PubMed',
                    'url': f'https://pubmed.ncbi.nlm.nih.gov/?term={topic.replace(" ", "+")}',
                    'type': 'Medical Research'
                },
                {
                    'title': f'{topic} - IEEE Xplore',
                    'url': f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={topic.replace(" ", "+")}',
                    'type': 'Technical Papers'
                },
                {
                    'title': f'{topic} - ResearchGate',
                    'url': f'https://www.researchgate.net/search?q={topic.replace(" ", "+")}',
                    'type': 'Research Network'
                },
                {
                    'title': f'{subject}: {topic} - arXiv',
                    'url': f'https://arxiv.org/search/?query={topic.replace(" ", "+")}&searchtype=all',
                    'type': 'Preprint Repository'
                }
            ]
        }
        
        level_key = academic_level.lower().replace(' ', '_')
        if level_key in base_references:
            references.extend(base_references[level_key])
        else:
            references.extend(base_references['undergraduate'])
        
        subject_specific = self._get_subject_specific_references(subject, topic)
        references.extend(subject_specific)
        
        return references

    def _get_subject_specific_references(self, subject: str, topic: str) -> List[Dict]:
        """
        Get subject-specific reference sources
        """
        subject_refs = {
            'Mathematics': [
                {
                    'title': f'{topic} - Wolfram MathWorld',
                    'url': f'https://mathworld.wolfram.com/search/?query={topic.replace(" ", "+")}',
                    'type': 'Mathematical Reference'
                }
            ],
            'Physics': [
                {
                    'title': f'{topic} - Physics World',
                    'url': f'https://physicsworld.com/search/{topic.replace(" ", "-")}/',
                    'type': 'Physics Journal'
                }
            ],
            'Chemistry': [
                {
                    'title': f'{topic} - Chemical & Engineering News',
                    'url': f'https://cen.acs.org/search.html?q={topic.replace(" ", "+")}',
                    'type': 'Chemistry News'
                }
            ],
            'Biology': [
                {
                    'title': f'{topic} - Biology Online',
                    'url': f'https://www.biologyonline.com/search?q={topic.replace(" ", "+")}',
                    'type': 'Biology Resource'
                }
            ],
            'Computer Science': [
                {
                    'title': f'{topic} - ACM Digital Library',
                    'url': f'https://dl.acm.org/action/doSearch?AllField={topic.replace(" ", "+")}',
                    'type': 'Computer Science Papers'
                }
            ],
            'History': [
                {
                    'title': f'{topic} - History.com',
                    'url': f'https://www.history.com/search?q={topic.replace(" ", "+")}',
                    'type': 'Historical Resource'
                }
            ]
        }
        
        return subject_refs.get(subject, [])

    def _extract_key_points(self, content: str) -> List[str]:
        """
        Extract key learning points from the content
        """
        key_points = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('## ') and not line.startswith('## 1. Introduction'):
                key_points.append(line.replace('## ', '').replace('#', ''))
            elif line.startswith('- ') or line.startswith('* '):
                key_points.append(line.replace('- ', '').replace('* ', ''))
        
        return key_points[:10]
