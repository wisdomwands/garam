
let contents = [];
let currentIndex = 0;
let isPlaying = false;
let synth = window.speechSynthesis;
let utterance = null;
let voices = [];

// Select elements
const playPauseBtn = document.getElementById('play-pause-btn');
const playIcon = document.getElementById('play-icon');
const pauseIcon = document.getElementById('pause-icon');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const currentSpeaker = document.getElementById('current-speaker');
const currentText = document.getElementById('current-text');
const playlist = document.getElementById('playlist');
const progressBar = document.getElementById('progress-bar');
const currentIndexEl = document.getElementById('current-index');
const totalCountEl = document.getElementById('total-count');
const speedRange = document.getElementById('speed-range');
const speedVal = document.getElementById('speed-val');
const voiceSelect = document.getElementById('voice-select');

// Initialize
async function init() {
    try {
        const response = await fetch('content.json');
        contents = await response.json();
        totalCountEl.textContent = contents.length;
        renderPlaylist();
        loadIndex(0);
        
        // Load voices
        loadVoices();
        if (synth.onvoiceschanged !== undefined) {
            synth.onvoiceschanged = loadVoices;
        }
    } catch (error) {
        console.error('Content load failed:', error);
        currentText.textContent = '데이터를 불러오는 데 실패했습니다.';
    }
}

function loadVoices() {
    voices = synth.getVoices();
    const krVoices = voices.filter(v => v.lang.includes('KO') || v.lang.includes('ko'));
    
    voiceSelect.innerHTML = '';
    
    if (krVoices.length === 0) {
        const option = document.createElement('option');
        option.textContent = '한국어 음성을 찾을 수 없습니다';
        voiceSelect.appendChild(option);
        return;
    }

    krVoices.forEach(voice => {
        const option = document.createElement('option');
        option.textContent = `${voice.name} ${voice.default ? '(기본)' : ''}`;
        option.value = voice.name;
        voiceSelect.appendChild(option);
    });

    // Auto-select best voice: Priority: Google > Natural > Others
    const bestVoice = krVoices.find(v => v.name.includes('Google')) || 
                      krVoices.find(v => v.name.includes('Natural')) ||
                      krVoices[0];
    
    if (bestVoice) {
        voiceSelect.value = bestVoice.name;
    }
}

function renderPlaylist() {
    playlist.innerHTML = '';
    contents.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = `playlist-item ${index === currentIndex ? 'active' : ''}`;
        div.innerHTML = `
            <span class="p-speaker">${item.speaker === 'Wonju' ? '원주(原柱)' : '재민(Gemini)'}</span>
            <span class="p-text">${item.text}</span>
        `;
        div.onclick = () => {
            loadIndex(index);
            if (isPlaying) startPlaying();
        };
        playlist.appendChild(div);
    });
}

function loadIndex(index) {
    currentIndex = index;
    const item = contents[currentIndex];
    currentSpeaker.textContent = item.speaker === 'Wonju' ? '원주(原柱)' : '재민(Gemini)';
    currentText.textContent = item.text;
    currentIndexEl.textContent = currentIndex + 1;
    
    // Update progress
    const progress = ((currentIndex + 1) / contents.length) * 100;
    progressBar.style.width = `${progress}%`;

    // Update playlist active state
    document.querySelectorAll('.playlist-item').forEach((el, i) => {
        el.classList.toggle('active', i === currentIndex);
    });

    // Scroll active item into view
    const activeItem = document.querySelector('.playlist-item.active');
    if (activeItem) {
        activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function startPlaying() {
    synth.cancel();
    
    utterance = new SpeechSynthesisUtterance(contents[currentIndex].text);
    utterance.lang = 'ko-KR';
    utterance.rate = parseFloat(speedRange.value);
    
    // Assign selected voice
    const selectedVoiceName = voiceSelect.value;
    const selectedVoice = voices.find(v => v.name === selectedVoiceName);
    if (selectedVoice) {
        utterance.voice = selectedVoice;
    }

    utterance.onend = () => {
        if (currentIndex < contents.length - 1) {
            currentIndex++;
            loadIndex(currentIndex);
            startPlaying();
        } else {
            togglePlayState(false);
        }
    };

    synth.speak(utterance);
    togglePlayState(true);
}

function togglePlayState(play) {
    isPlaying = play;
    if (isPlaying) {
        playIcon.classList.add('hidden');
        pauseIcon.classList.remove('hidden');
    } else {
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
    }
}

playPauseBtn.onclick = () => {
    if (isPlaying) {
        synth.pause();
        togglePlayState(false);
    } else {
        if (synth.paused && utterance) {
            synth.resume();
            togglePlayState(true);
        } else {
            startPlaying();
        }
    }
};

prevBtn.onclick = () => {
    if (currentIndex > 0) {
        currentIndex--;
        loadIndex(currentIndex);
        if (isPlaying) startPlaying();
    }
};

nextBtn.onclick = () => {
    if (currentIndex < contents.length - 1) {
        currentIndex++;
        loadIndex(currentIndex);
        if (isPlaying) startPlaying();
    }
};

speedRange.oninput = () => {
    speedVal.textContent = `${speedRange.value}x`;
};

voiceSelect.onchange = () => {
    if (isPlaying) startPlaying();
};

init();
