class AILearningPlatform {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.currentSession = null;
        
        this.initializeEventListeners();
        this.checkVoiceStatus();
    }
    
    initializeEventListeners() {
        document.getElementById('generateContent').addEventListener('click', () => this.generateContent());
        document.getElementById('startTest').addEventListener('click', () => this.showTestSection());
        document.getElementById('startRecording').addEventListener('click', () => this.startRecording());
        document.getElementById('stopRecording').addEventListener('click', () => this.stopRecording());
        document.getElementById('analyzeResponse').addEventListener('click', () => this.analyzeResponse());
        document.getElementById('analyzeTyped').addEventListener('click', () => this.analyzeTypedResponse());
        document.getElementById('typeResponse').addEventListener('click', () => this.showTypeSection());
        document.getElementById('tryAgain').addEventListener('click', () => this.tryAgain());
        document.getElementById('newTopic').addEventListener('click', () => this.newTopic());
        
        document.getElementById('academicLevel').addEventListener('change', () => this.validateForm());
        document.getElementById('subject').addEventListener('input', () => this.validateForm());
        document.getElementById('topic').addEventListener('input', () => this.validateForm());
    }
    
    async checkVoiceStatus() {
        try {
            const response = await fetch('/voice_status');
            const status = await response.json();
            
            if (!status.assemblyai_available) {
                this.showNotification('Voice recording may not be available. Please ensure AssemblyAI API key is configured.', 'warning');
            }
        } catch (error) {
            console.error('Voice status check failed:', error);
        }
    }
    
    validateForm() {
        const academicLevel = document.getElementById('academicLevel').value;
        const subject = document.getElementById('subject').value.trim();
        const topic = document.getElementById('topic').value.trim();
        
        const generateBtn = document.getElementById('generateContent');
        generateBtn.disabled = !(academicLevel && subject && topic);
    }
    
    async generateContent() {
        const academicLevel = document.getElementById('academicLevel').value;
        const subject = document.getElementById('subject').value.trim();
        const topic = document.getElementById('topic').value.trim();
        
        if (!academicLevel || !subject || !topic) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }
        
        this.setLoadingState('generateContent', true, 'Generating content...');
        
        try {
            const response = await fetch('/generate_content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    academic_level: academicLevel,
                    subject: subject,
                    topic: topic
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayContent(data);
                this.showSection('contentSection');
                this.currentSession = data.session_id;
                this.showNotification('Content generated successfully!', 'success');
            } else {
                throw new Error(data.error || 'Content generation failed');
            }
        } catch (error) {
            console.error('Content generation error:', error);
            this.showNotification(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoadingState('generateContent', false, 'Generate Learning Content');
        }
    }
    
    displayContent(data) {
        const contentDisplay = document.getElementById('contentDisplay');
        const referencesDisplay = document.getElementById('referencesDisplay');
        
        contentDisplay.innerHTML = this.formatContent(data.content);
        
        referencesDisplay.innerHTML = data.references.map(ref => `
            <div class="glass-card rounded-lg p-4">
                <h4 class="font-semibold text-blue-300 mb-2">${ref.title}</h4>
                <p class="text-xs text-blue-400 mb-2">${ref.type}</p>
                <a href="${ref.url}" target="_blank" rel="noopener noreferrer" 
                   class="text-blue-400 hover:text-blue-300 text-sm underline break-all">
                    ${ref.url}
                </a>
            </div>
        `).join('');
    }
    
    formatContent(content) {
        return content
            .replace(/^# (.+)$/gm, '<h1 class="text-3xl font-bold mb-6 text-blue-300">$1</h1>')
            .replace(/^## (.+)$/gm, '<h2 class="text-2xl font-semibold mb-4 mt-8 text-blue-400">$1</h2>')
            .replace(/^### (.+)$/gm, '<h3 class="text-xl font-medium mb-3 mt-6 text-blue-500">$1</h3>')
            .replace(/^\* (.+)$/gm, '<li class="mb-2 text-blue-100">$1</li>')
            .replace(/^- (.+)$/gm, '<li class="mb-2 text-blue-100">$1</li>')
            .replace(/\n\n/g, '</p><p class="mb-4 text-blue-100 leading-relaxed">')
            .replace(/^(?!<[h|l])/gm, '<p class="mb-4 text-blue-100 leading-relaxed">')
            .replace(/(<li.*<\/li>)/gs, '<ul class="list-disc list-inside mb-4 space-y-2">$1</ul>')
            .replace(/<\/p>$/g, '');
    }
    
    showTestSection() {
        this.showSection('testSection');
        document.getElementById('testSection').scrollIntoView({ behavior: 'smooth' });
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                } 
            });
            
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                this.processRecording();
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            document.getElementById('startRecording').disabled = true;
            document.getElementById('stopRecording').disabled = false;
            document.getElementById('recordingStatus').classList.remove('hidden');
            
        } catch (error) {
            console.error('Recording error:', error);
            this.showNotification('Microphone access denied or not available', 'error');
        }
    }
    
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            document.getElementById('startRecording').disabled = false;
            document.getElementById('stopRecording').disabled = true;
            document.getElementById('recordingStatus').classList.add('hidden');
        }
    }
    
    async processRecording() {
        if (this.audioChunks.length === 0) {
            this.showNotification('No audio recorded', 'error');
            return;
        }
        
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        
        this.showNotification('Processing audio...', 'info');
        
        try {
            const response = await fetch('/transcribe_audio', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('transcriptionText').textContent = data.transcription;
                document.getElementById('transcriptionSection').classList.remove('hidden');
                this.showNotification('Audio transcribed successfully!', 'success');
            } else {
                throw new Error(data.error || 'Transcription failed');
            }
        } catch (error) {
            console.error('Transcription error:', error);
            this.showNotification(`Transcription error: ${error.message}`, 'error');
        }
    }
    
    showTypeSection() {
        document.getElementById('typeSection').classList.remove('hidden');
        document.getElementById('typedResponse').focus();
    }
    
    async analyzeResponse() {
        const transcription = document.getElementById('transcriptionText').textContent;
        await this.performAnalysis(transcription);
    }
    
    async analyzeTypedResponse() {
        const typedResponse = document.getElementById('typedResponse').value.trim();
        if (!typedResponse) {
            this.showNotification('Please enter your response', 'error');
            return;
        }
        await this.performAnalysis(typedResponse);
    }
    
    async performAnalysis(userResponse) {
        if (!userResponse) {
            this.showNotification('No response to analyze', 'error');
            return;
        }
        
        this.setLoadingState('analyzeResponse', true, 'Analyzing...');
        
        try {
            const response = await fetch('/analyze_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    response: userResponse
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayAnalysis(data.analysis);
                this.showSection('analysisSection');
                document.getElementById('analysisSection').scrollIntoView({ behavior: 'smooth' });
                
                if (data.analysis.can_proceed) {
                    this.showCelebration(data.analysis.grade);
                }
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification(`Analysis error: ${error.message}`, 'error');
        } finally {
            this.setLoadingState('analyzeResponse', false, 'Analyze My Response');
        }
    }
    
    displayAnalysis(analysis) {
        const gradeCircle = document.getElementById('gradeCircle');
        const gradeNumber = document.getElementById('gradeNumber');
        const gradeExplanation = document.getElementById('gradeExplanation');
        const feedbackText = document.getElementById('feedbackText');
        const nextStepsText = document.getElementById('nextStepsText');
        
        gradeNumber.textContent = `${analysis.grade}/10`;
        gradeExplanation.textContent = analysis.grade_explanation;
        feedbackText.textContent = analysis.detailed_feedback;
        nextStepsText.textContent = analysis.next_steps;
        
        gradeCircle.className = 'grade-circle mb-4 ' + this.getGradeClass(analysis.grade);
        
        this.populateList('strengthsList', analysis.strengths);
        this.populateList('improvementsList', analysis.improvements);
        this.populateList('falsePointsList', analysis.false_points);
        this.populateList('missingPointsList', analysis.missing_points);
    }
    
    getGradeClass(grade) {
        if (grade >= 9) return 'grade-excellent';
        if (grade >= 7) return 'grade-good';
        if (grade >= 5) return 'grade-fair';
        return 'grade-poor';
    }
    
    populateList(listId, items) {
        const list = document.getElementById(listId);
        if (items && items.length > 0) {
            list.innerHTML = items.map(item => `<li class="flex items-start"><span class="mr-2">•</span><span>${item}</span></li>`).join('');
        } else {
            list.innerHTML = '<li class="text-gray-400 italic">None identified</li>';
        }
    }
    
    showCelebration(grade) {
        if (grade >= 9) {
            const overlay = document.getElementById('celebrationOverlay');
            const message = document.getElementById('celebrationMessage');
            const emojis = document.getElementById('celebrationEmojis');
            
            const messages = [
                'Outstanding Work!',
                'Excellent Mastery!',
                'Brilliant Performance!',
                'Exceptional Understanding!'
            ];
            
            message.textContent = messages[Math.floor(Math.random() * messages.length)];
            emojis.textContent = '🥳🎉🎊';
            
            overlay.classList.remove('hidden');
            
            setTimeout(() => {
                overlay.classList.add('hidden');
            }, 3000);
        }
    }
    
    tryAgain() {
        document.getElementById('analysisSection').classList.add('hidden');
        document.getElementById('transcriptionSection').classList.add('hidden');
        document.getElementById('typeSection').classList.add('hidden');
        document.getElementById('typedResponse').value = '';
        document.getElementById('transcriptionText').textContent = '';
        
        this.showSection('testSection');
        document.getElementById('testSection').scrollIntoView({ behavior: 'smooth' });
    }
    
    newTopic() {
        document.getElementById('academicLevel').value = '';
        document.getElementById('subject').value = '';
        document.getElementById('topic').value = '';
        document.getElementById('typedResponse').value = '';
        document.getElementById('transcriptionText').textContent = '';
        
        this.hideAllSections();
        this.showSection('setupSection');
        this.validateForm();
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    showSection(sectionId) {
        document.getElementById(sectionId).classList.remove('hidden');
    }
    
    hideAllSections() {
        const sections = ['contentSection', 'testSection', 'analysisSection'];
        sections.forEach(section => {
            document.getElementById(section).classList.add('hidden');
        });
        
        document.getElementById('transcriptionSection').classList.add('hidden');
        document.getElementById('typeSection').classList.add('hidden');
    }
    
    setLoadingState(buttonId, loading, text) {
        const button = document.getElementById(buttonId);
        const textElement = document.getElementById(buttonId.replace('Content', 'Text').replace('Response', 'Text'));
        const spinnerElement = document.getElementById(buttonId.replace('Content', 'Spinner').replace('Response', 'Spinner'));
        
        if (loading) {
            button.disabled = true;
            if (textElement) textElement.textContent = text;
            if (spinnerElement) spinnerElement.classList.remove('hidden');
        } else {
            button.disabled = false;
            if (textElement) textElement.textContent = text;
            if (spinnerElement) spinnerElement.classList.add('hidden');
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transition-all duration-300 transform translate-x-full`;
        
        const colors = {
            success: 'bg-green-600 text-white',
            error: 'bg-red-600 text-white',
            warning: 'bg-yellow-600 text-white',
            info: 'bg-blue-600 text-white'
        };
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        notification.className += ` ${colors[type]}`;
        notification.innerHTML = `
            <div class="flex items-center">
                <span class="mr-2">${icons[type]}</span>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 4000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AILearningPlatform();
});
