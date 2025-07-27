import requests
import json
from typing import Dict, List, Optional
import re

class AIAnalyzer:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.groq_api_key = None
        
        if api_keys.get('GROQ_API_KEY'):
            try:
                self.groq_api_key = api_keys['GROQ_API_KEY']
                self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
                self.groq_model = "llama3-8b-8192"
                print("✅ Groq API configured successfully for analysis")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
                self.groq_api_key = None
        else:
            print("⚠️ No Groq API key provided")
        
        if not self.groq_api_key:
            print("⚠️ No AI analysis API available")

    def analyze_user_response(self, user_response: str, original_content: Dict, 
                            academic_level: str, subject: str, topic: str) -> Dict:
        """
        Analyze user's response as a globally renowned educator
        """
        try:
            analysis_prompt = self._create_analysis_prompt(
                user_response, original_content, academic_level, subject, topic
            )
            
            analysis_text = self._get_ai_response(analysis_prompt)
            parsed_analysis = self._parse_analysis(analysis_text)
            
            return {
                'strengths': parsed_analysis['strengths'],
                'false_points': parsed_analysis['false_points'],
                'missing_points': parsed_analysis['missing_points'],
                'examples_quality': parsed_analysis['examples_quality'],
                'areas_lacking': parsed_analysis['areas_lacking'],
                'improvements': parsed_analysis['improvements'],
                'grade': parsed_analysis['grade'],
                'grade_explanation': parsed_analysis['grade_explanation'],
                'can_proceed': parsed_analysis['grade'] >= 9,
                'celebration_worthy': parsed_analysis['grade'] >= 9,
                'detailed_feedback': parsed_analysis['detailed_feedback'],
                'next_steps': parsed_analysis['next_steps']
            }
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            raise

    def _create_analysis_prompt(self, user_response: str, original_content: Dict, 
                              academic_level: str, subject: str, topic: str) -> str:
        """
        Create detailed analysis prompt
        """
        key_points = original_content.get('key_points', [])
        content_structure = original_content.get('structure', [])
        
        return f"""
You are a globally renowned educator with decades of experience teaching diverse students across different fields and personalities. You have taught at prestigious institutions worldwide and are known for your insightful, constructive, detailed, actionable and encouraging feedback.

STUDENT DETAILS:
- Academic Level: {academic_level}
- Subject: {subject}
- Topic: {topic}

ORIGINAL LEARNING CONTENT KEY POINTS:
{chr(10).join([f"• {point}" for point in key_points[:15]])}

CONTENT STRUCTURE COVERED:
{chr(10).join([f"• {section.get('title', '')}" for section in content_structure])}

STUDENT'S RESPONSE:
"{user_response}"

As a world-class educator, provide a comprehensive analysis following this EXACT format:

## STRENGTHS
[List 3-5 specific strengths in the student's response, being encouraging but brutally honest]

## FALSE POINTS
[Identify any incorrect information or misconceptions, explain why they're wrong and provide correct information]

## MISSING POINTS
[List important concepts from the original content that the student didn't mention or address adequately]

## EXAMPLES QUALITY
[Evaluate the quality, relevance, and accuracy of any examples the student provided]

## AREAS LACKING
[Identify areas where the student's understanding seems shallow or incomplete]

## IMPROVEMENTS
[Provide specific, actionable suggestions for improvement]

## GRADE
[Assign a grade from 1-10 based on:
- Accuracy of information (30%)
- Completeness of coverage (25%)
- Understanding depth (20%)
- Use of examples (15%)
- Clarity of explanation (10%)
Grade: X/10]

## GRADE EXPLANATION
[Explain in 2-3 sentences why you gave this specific grade]

## DETAILED FEEDBACK
[Provide encouraging, constructive feedback that acknowledges the student's effort while guiding improvement]

## NEXT STEPS
[Suggest specific next steps - if grade is 9-10, encourage moving to next topic; if lower, suggest focused study areas]

Remember to:
- Be encouraging and supportive while maintaining academic rigor
- Adapt your language to the {academic_level} level
- Consider diverse learning styles and personalities
- Provide specific, actionable feedback
- Balance criticism with encouragement
- Recognize effort and improvement potential
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
                "max_tokens": 2000
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
            
            return self._generate_mock_analysis()
                
        except Exception as e:
            print(f"⚠️ AI API Error: {e}")
            return self._generate_mock_analysis()
    
    def _generate_mock_analysis(self) -> str:
        return """
## STRENGTHS
- You attempted to engage with the topic, which shows initiative
- Your response demonstrates basic understanding of the subject
- You showed effort in trying to explain the concepts

## FALSE POINTS
- No specific incorrect information identified in this mock analysis
- Please configure your Groq API key for detailed analysis

## MISSING POINTS
- Detailed analysis requires proper API configuration
- Key concepts from the learning material need to be addressed
- Examples and applications should be included

## EXAMPLES QUALITY
Mock analysis - please configure API keys for detailed feedback

## AREAS LACKING
- Depth of understanding needs improvement
- More specific examples would strengthen your response
- Connection to real-world applications could be enhanced

## IMPROVEMENTS
- Review the learning material more thoroughly
- Practice explaining concepts in your own words
- Include specific examples to demonstrate understanding

## GRADE
Grade: 5/10

## GRADE EXPLANATION
This is a mock analysis. Configure your Groq API key to receive detailed, personalized feedback on your responses.

## DETAILED FEEDBACK
To receive comprehensive feedback on your learning progress, please ensure your API keys are properly configured. This will enable detailed analysis of your understanding and personalized recommendations for improvement.

## NEXT STEPS
Configure your API keys and try again to receive detailed analysis and guidance for your learning journey.
"""

    def _parse_analysis(self, analysis_text: str) -> Dict:
        """
        Parse the structured analysis response
        """
        sections = {
            'strengths': [],
            'false_points': [],
            'missing_points': [],
            'examples_quality': '',
            'areas_lacking': [],
            'improvements': [],
            'grade': 5,
            'grade_explanation': '',
            'detailed_feedback': '',
            'next_steps': ''
        }
        
        current_section = None
        lines = analysis_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if '## STRENGTHS' in line:
                current_section = 'strengths'
            elif '## FALSE POINTS' in line:
                current_section = 'false_points'
            elif '## MISSING POINTS' in line:
                current_section = 'missing_points'
            elif '## EXAMPLES QUALITY' in line:
                current_section = 'examples_quality'
            elif '## AREAS LACKING' in line:
                current_section = 'areas_lacking'
            elif '## IMPROVEMENTS' in line:
                current_section = 'improvements'
            elif '## GRADE' in line:
                current_section = 'grade'
            elif '## GRADE EXPLANATION' in line:
                current_section = 'grade_explanation'
            elif '## DETAILED FEEDBACK' in line:
                current_section = 'detailed_feedback'
            elif '## NEXT STEPS' in line:
                current_section = 'next_steps'
            elif line and current_section:
                if current_section == 'grade':
                    grade_match = re.search(r'(\d+)/10', line)
                    if grade_match:
                        sections['grade'] = int(grade_match.group(1))
                elif current_section in ['strengths', 'false_points', 'missing_points', 'areas_lacking', 'improvements']:
                    if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                        sections[current_section].append(line.lstrip('•-* '))
                    elif line and not line.startswith('#'):
                        sections[current_section].append(line)
                else:
                    if sections[current_section]:
                        sections[current_section] += ' ' + line
                    else:
                        sections[current_section] = line
        
        # Ensure we have fallback values
        if not sections['strengths']:
            sections['strengths'] = ['You attempted to engage with the topic, which shows initiative.']
        
        if not sections['improvements']:
            sections['improvements'] = ['Continue studying the material and practice explaining concepts in your own words.']
        
        if not sections['detailed_feedback']:
            sections['detailed_feedback'] = 'Keep working on understanding the core concepts. Learning is a process, and every attempt helps you grow.'
        
        if not sections['next_steps']:
            if sections['grade'] >= 9:
                sections['next_steps'] = 'Excellent work! You can confidently move on to the next topic.'
            else:
                sections['next_steps'] = 'Review the areas mentioned above and try explaining the topic again when you feel ready.'
        
        return sections

    def get_celebration_message(self, grade: int, topic: str) -> Dict:
        """
        Get celebration message for high grades
        """
        if grade >= 9:
            messages = [
                f"🎉 Outstanding work on {topic}! You've mastered this topic brilliantly!",
                f"👏 Exceptional understanding of {topic}! Your knowledge is impressive!",
                f"🏆 Fantastic job! You've demonstrated excellent mastery of {topic}!",
                f"✨ Brilliant work! Your understanding of {topic} is truly commendable!"
            ]
            
            import random
            return {
                'show_celebration': True,
                'message': random.choice(messages),
                'emojis': '🥳🎉🎊',
                'duration': 3000
            }
        
        return {
            'show_celebration': False,
            'message': '',
            'emojis': '',
            'duration': 0
        }
