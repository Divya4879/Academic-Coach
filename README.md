# 🧠 EduMind AI - Intelligent Learning Platform

A revolutionary educational platform that uses AI to generate structured learning content and provides voice-based assessment with detailed feedback. Built with Flask, Assembly AI, Groq API, and modern web technologies.

## ✨ Features

- **Adaptive Content Generation**: Creates 2000-3000 word educational content tailored to academic level
- **Voice-Based Assessment**: Uses Assembly AI for speech-to-text transcription
- **AI-Powered Analysis**: Acts as a globally renowned educator providing detailed feedback
- **Intelligent Grading**: Grades responses out of 10 with detailed explanations
- **Progress Tracking**: Students must score 9+ to advance to next topics
- **Celebration System**: 3-second emoji overlay for excellent performance (🥳🎉🎊)
- **Mobile Responsive**: Darker blue theme with high contrast design
- **Real References**: Provides working, relevant reference links
- **Multiple Academic Levels**: High School, Undergraduate, Graduate, Professional
- **Custom Subject Input**: Users can input any subject of their interest
- **Header Image Section**: Beautiful 40vh header with gradient background
- **Production Ready**: Modern glass morphism design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (Free tier available)
- Assembly AI API Key (Free tier available)

### Local Development

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd ai-learning-platform
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   
   Create `utils/api_keys_config.py`:
   ```python
   GROQ_API_KEY = "gsk_your-groq-api-key-here"
   ASSEMBLYAI_API_KEY = "your-assemblyai-api-key-here"
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```
   
   Access at: `https://localhost:5000` (HTTPS required for microphone access)

## 🌐 Netlify Deployment

### Step 1: Environment Variables

In your Netlify dashboard, go to **Site Settings > Environment Variables** and add:

| Variable Name | Description | Example |
|---------------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key for content generation and analysis | `gsk_...` |
| `ASSEMBLYAI_API_KEY` | Your Assembly AI API key for voice transcription | `your-assemblyai-key` |

### Step 2: Deploy

1. Connect your GitHub repository to Netlify
2. Set the build command: `pip install -r requirements.txt`
3. Set the publish directory: `.`
4. Add environment variables as listed above
5. Deploy!

## 🔧 API Keys Setup

### Groq API Key (FREE TIER AVAILABLE)
1. Visit [Groq Console](https://console.groq.com/)
2. Create account and generate API key
3. Add to environment variables as `GROQ_API_KEY`
4. **Model Used**: `llama3-8b-8192` (Free tier compatible)

### Assembly AI API Key (FREE TIER AVAILABLE)
1. Visit [Assembly AI](https://www.assemblyai.com/)
2. Sign up for free account
3. Go to dashboard and copy your API key
4. Add to environment variables as `ASSEMBLYAI_API_KEY`

## 📁 Project Structure

```
ai-learning-platform/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies (simplified)
├── README.md                      # This file
├── netlify.toml                   # Netlify configuration
├── utils/
│   ├── api_keys.py               # API key management (Groq + Assembly AI only)
│   ├── api_keys_config.py        # Local API keys (create this)
│   ├── api_keys_config_template.py # Template for API keys
│   ├── content_generator.py      # AI content generation (Groq only)
│   ├── voice_manager.py          # Assembly AI integration
│   └── ai_analyzer.py            # Response analysis and grading (Groq only)
├── templates/
│   └── index.html                # Main HTML template
├── static/
│   └── js/
│       └── app.js                # Frontend JavaScript
└── temp/                         # Temporary audio files (auto-created)
```

## 🎯 How It Works

### 1. Content Generation
- User selects academic level and inputs custom subject and topic
- AI generates comprehensive 2000-3000 word content using **Groq's llama3-8b-8192 model**
- Content is structured with numbered topics and subtopics
- Real reference links are provided based on academic level

### 2. Voice Assessment
- User explains what they learned via voice recording
- **Assembly AI** transcribes speech to text with high accuracy
- Alternative: Users can type their response

### 3. AI Analysis
- Acts as a globally renowned educator using **Groq's llama3-8b-8192 model**
- Analyzes response for accuracy, completeness, and understanding
- Provides detailed feedback on strengths and areas for improvement
- Grades out of 10 with specific explanations

### 4. Progress System
- Students need 9+ grade to advance
- 3-second celebration animation for excellent performance
- Detailed next steps provided for improvement

## 🔧 Technical Configuration

### Groq API Configuration (Exact from Sassy-Debate-Coach)
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **Model**: `llama3-8b-8192`
- **Temperature**: 0.8
- **Max Tokens**: 4000 (content) / 2000 (analysis)
- **Free Tier**: Available with generous limits

### Assembly AI Configuration
- **High-accuracy transcription**
- **Language detection enabled**
- **Punctuation and formatting enabled**
- **Free Tier**: Available with monthly limits

## 🎨 Design Features

- **Darker Blue Theme**: Professional, easy on the eyes with deeper blues
- **High Contrast**: Excellent readability and accessibility
- **Mobile Responsive**: Works perfectly on all devices
- **Glass Morphism**: Modern UI with enhanced backdrop blur effects
- **Header Image Section**: 40vh beautiful gradient header
- **Smooth Animations**: Enhanced user experience with better transitions
- **Loading States**: Clear feedback during processing
- **Full Width Footer**: "Made with ❤️ by Divya"

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify Groq API key is valid and has credits
   - Check Assembly AI API key and quotas
   - Ensure proper formatting (no extra spaces)

2. **Content Generation Fails**
   - Check Groq API key and free tier limits
   - Verify internet connection
   - Try with simpler topics first

3. **Assembly AI Transcription Issues**
   - Verify Assembly AI API key
   - Check audio file size (max 100MB)
   - Ensure clear audio recording

4. **Microphone Not Working**
   - Ensure HTTPS connection (required for microphone access)
   - Check browser permissions
   - Use localhost, not IP addresses

## 🚀 Performance Optimization

- **Simplified Dependencies**: Only essential packages
- **Efficient API Calls**: Single provider for content generation and analysis
- **Free Tier Friendly**: Optimized for free tier usage
- **Fast Response Times**: Groq's high-speed inference

## 🔒 Security Features

- **HTTPS Enforcement**: Required for microphone access
- **API Key Protection**: Environment variables only
- **Input Validation**: Sanitized user inputs
- **File Upload Limits**: Restricted audio file sizes

## 💰 Cost Efficiency

- **Groq Free Tier**: Generous limits for educational use
- **Assembly AI Free Tier**: Monthly transcription allowance
- **No Premium APIs**: Designed for free tier usage
- **Optimized Prompts**: Efficient token usage

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Assembly AI** for speech-to-text capabilities
- **Groq** for fast, free AI inference
- **Tailwind CSS** for beautiful, responsive design
- **Flask** for the robust web framework

## 📞 Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create new issue with detailed description
4. Include error messages and steps to reproduce

---

**Made with ❤️ by Divya**
