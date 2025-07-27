# 🧠✨📈 Grasp Articulate Refine

Your smart study coach, powered by AI - designed to help you truly understand what you learn, speak it with confidence, and get thoughtful feedback so you grow smarter, faster.

My project at a glimpse:-

<img width="1920" height="6177" alt="screencapture-localhost-5000-2025-07-28-02_44_24" src="https://github.com/user-attachments/assets/f87e5080-f1e6-4c89-8cbd-db9169b655e5" />

Check it out here live:- [Grasp Articulate Refine](https://academic-coach.onrender.com/)

---

## ✨ Features

- **Adaptive Content Generation**: Creates 2000-3000 word educational content tailored to your academic level
- **Voice-Based Assessment**: Uses Assembly AI for speech-to-text transcription
- **AI-Powered Analysis**: Acts as a globally renowned educator providing detailed feedback
- **Intelligent Grading**: Grades responses out of 10 with detailed explanations
- **Progress Tracking**: Students must score 9+ to advance to next topics
- **Celebration System**: 3-second emoji overlay for excellent performance (🥳🎉🎊)
- **Mobile Responsive**: Darker blue theme with high contrast design
- **Real References**: Provides working, relevant reference links for the explanation provided
- **Multiple Academic Levels**: High School, Undergraduate, Graduate, Professional
- **Custom Subject Input**: Users can input any subject of their interest
- **Header Image Section**: Beautiful 50vh header with a gradient background
- **Production Ready**: Modern glass morphism design with smooth animations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (Free tier available)
- Assembly AI API Key (Free tier available)

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/Divya4879/Academic-Coach.git
   cd Academic-Coach
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

---

## 🌐 Render Deployment - Complete Guide

### Step 1: Create Render Account

1. **Visit Render**: Go to [render.com](https://render.com)
2. **Sign Up**: Click "Get Started" → "Sign up with GitHub" (recommended)
3. **Authorize GitHub**: Allow Render to access your repositories
4. **Verify Email**: Check your email and verify your account

### Step 2: Prepare Your Repository

### Step 3: Connect GitHub Repository

1. **Login to Render Dashboard**: Go to [dashboard.render.com](https://dashboard.render.com)
2. **New Web Service**: Click "New +" → "Web Service"
3. **Connect Repository**: 
   - If first time: Click "Connect GitHub" → Authorize Render
   - Select your `Academic-Coach` repository
   - Click "Connect"

### Step 4: Configure Web Service

#### Basic Configuration:
- **Name**: `Academic-Coach` (or your preferred name)
- **Region**: Choose closest to your users (e.g., Oregon, Frankfurt, Singapore)
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave blank (uses repository root)

#### Build & Deploy Settings:
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

#### Advanced Settings:
- **Instance Type**: `Free` (for testing) or `Starter` ($7/month for production)
- **Auto-Deploy**: `Yes` (deploys automatically on git push)

### Step 5: Environment Variables

In the **Environment** section, add these variables:

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `GROQ_API_KEY` | `gsk_your-actual-groq-key` | Get from [console.groq.com](https://console.groq.com) |
| `ASSEMBLYAI_API_KEY` | `your-actual-assemblyai-key` | Get from [assemblyai.com](https://www.assemblyai.com) |

**To add environment variables:**
1. Scroll to "Environment Variables" section
2. Click "Add Environment Variable"
3. Enter key and value
4. Click "Save Changes"

### Step 6: Deploy

1. **Review Settings**: Double-check all configurations
2. **Create Web Service**: Click "Create Web Service"
3. **Monitor Build**: Watch the build logs in real-time
4. **Wait for Deployment**: First deployment takes 2-5 minutes

### Step 7: Verify Deployment

1. **Check Build Logs**: Ensure no errors during installation
2. **Test Your App**: Visit your Render URL (e.g., `https://Academic-Coach.onrender.com`)
3. **Test Features**:
   - Content generation
   - Voice recording (HTTPS automatically enabled)
   - AI analysis and grading

---

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

---

## 📁 Project Structure

```
ai-learning-platform/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies (simplified)
├── README.md                      # This file
├── utils/
│   ├── api_keys.py               # API key management (Groq + Assembly AI only)
│   ├── api_keys_config.py        # Local API keys (create this)
│   ├── api_keys_config_template.py # Template for API keys
│   ├── content_generator.py      # AI content generation (Groq API)
│   ├── voice_manager.py          # Assembly AI integration
│   └── ai_analyzer.py            # Response analysis and grading (Assembly Ai + Groq ai api)
├── templates/
│   └── index.html                # Main HTML template
├── static/
│   └── js/
│       └── app.js                # Frontend JavaScript
└── temp/                         # Temporary audio files (auto-created)
```

---

## 🎯 How It Works

### 1. Content Generation
- User selects their academic level and inputs custom subject and topic
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
- Detailed next steps provided for improvement if needed

---

## 🔧 Technical Configuration

### Groq API Configuration
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

---

## 🎨 Design Features

- **Dark Blue Theme**: Professional, easy on the eyes with deeper blues
- **High Contrast**: Excellent readability and accessibility
- **Mobile Responsive**: Works perfectly on all devices
- **Glass Morphism**: Modern UI with enhanced backdrop blur effects
- **Header Image Section**: 50vh beautiful gradient header
- **Smooth Animations**: Enhanced user experience with better transitions
- **Loading States**: Clear feedback during processing
- **Full Width Footer**: "Made with ❤️ by Divya"

---

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

---


## 🔒 Security Features

- **HTTPS Enforcement**: Required for microphone access
- **API Key Protection**: Environment variables only
- **Input Validation**: Sanitized user inputs
- **File Upload Limits**: Restricted audio file sizes

---

## 🤝 Contributions

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Assembly AI** for speech-to-text capabilities
- **Groq** for fast, free AI inference
- **Tailwind CSS** for beautiful, responsive design
- **Flask** for the robust web framework
- **Render** for free Python applications deployment

---

**Made with ❤️ by Divya**
