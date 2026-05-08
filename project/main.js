// ============================================
// STUDYMIND AI - QUESTION ANSWERING SYSTEM
// Frontend JavaScript
// ============================================

let currentSubject = 'All Subjects';
let questionCount = 0;
let sessionStart = Date.now();
let chatHistory = [];
let isLoading = false;

const subjectSuggestions = {
  'All Subjects': [
    "What is Newton's Second Law?",
    "Explain photosynthesis step by step",
    "What is Pythagoras theorem?",
    "How does DNA replication work?"
  ],
  'Mathematics': [
    "Solve: x² - 5x + 6 = 0",
    "What is the derivative of sin(x)?",
    "Explain integration by parts",
    "What is a prime number?"
  ],
  'Physics': [
    "What is Newton's 2nd law?",
    "Explain Ohm's law with formula",
    "What is quantum mechanics?",
    "Define electric potential"
  ],
  'Chemistry': [
    "What is a covalent bond?",
    "Explain the periodic table",
    "What is oxidation and reduction?",
    "Explain Le Chatelier's principle"
  ],
  'Biology': [
    "How does DNA replicate?",
    "Explain photosynthesis",
    "What is mitosis vs meiosis?",
    "What is the function of the kidney?"
  ],
  'Computer Science': [
    "What is Big O notation?",
    "Explain recursion with example",
    "What is a binary search tree?",
    "Difference between stack and queue?"
  ],
  'History': [
    "What caused World War 1?",
    "Who was Napoleon Bonaparte?",
    "Explain the French Revolution",
    "What was the Cold War?"
  ],
  'English': [
    "What is a metaphor? Give example",
    "Difference between simile and metaphor",
    "What are literary devices?",
    "How to write a good essay?"
  ],
  'Urdu': [
    "غزل کی تعریف کریں",
    "نظم اور غزل میں فرق",
    "اردو ادب کے بڑے شاعر کون ہیں؟",
    "مرزا غالب کے بارے میں بتائیں"
  ],
  'Islamiat': [
    "پانچ ارکان اسلام کیا ہیں؟",
    "قرآن کا نزول کب ہوا؟",
    "حضرت محمد ﷺ کی حیات مبارکہ",
    "زکوٰۃ کی اہمیت"
  ]
};

// === INIT ===
document.addEventListener('DOMContentLoaded', () => {
  generateParticles();
  updateSuggestions();
  startSessionTimer();
});

// === PARTICLES ===
function generateParticles() {
  const container = document.getElementById('particles');
  for (let i = 0; i < 35; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      width: ${Math.random() * 3 + 1}px;
      height: ${Math.random() * 3 + 1}px;
      animation-duration: ${Math.random() * 25 + 15}s;
      animation-delay: ${Math.random() * 25}s;
      opacity: ${Math.random() * 0.6 + 0.2};
    `;
    container.appendChild(p);
  }
}

// === SESSION TIMER ===
function startSessionTimer() {
  setInterval(() => {
    const mins = Math.floor((Date.now() - sessionStart) / 60000);
    const el = document.getElementById('session-time');
    if (el) el.textContent = mins + 'm';
  }, 15000);
}

// === SUBJECT MANAGEMENT ===
function setSubject(el, fromChips = false) {
  currentSubject = el.dataset.subject;

  // Update sidebar nav
  document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
  const matching = document.querySelector(`.nav-item[data-subject="${currentSubject}"]`);
  if (matching) matching.classList.add('active');

  // Update chips
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  const matchingChip = document.querySelector(`.chip[data-subject="${currentSubject}"]`);
  if (matchingChip) matchingChip.classList.add('active');

  // Update topbar label
  const label = document.getElementById('current-subject-label');
  if (label) label.textContent = el.textContent.trim();

  updateSuggestions();

  // Close sidebar on mobile
  if (fromChips) closeSidebar();
}

function updateSuggestions() {
  const qs = subjectSuggestions[currentSubject] || subjectSuggestions['All Subjects'];
  const grid = document.getElementById('suggestions-grid');
  if (!grid) return;
  grid.innerHTML = qs.map(q =>
    `<button class="qs-btn" onclick="useSuggestion(this)">${q}</button>`
  ).join('');
}

function useSuggestion(el) {
  const input = document.getElementById('question-input');
  input.value = el.textContent;
  autoResize(input);
  input.focus();
}

// === SIDEBAR TOGGLE ===
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
}

// === INPUT HANDLERS ===
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    askQuestion();
  }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 140) + 'px';
}

// === CLEAR CHAT ===
function clearChat() {
  chatHistory = [];
  questionCount = 0;
  const el = document.getElementById('q-count');
  if (el) el.textContent = '0';

  document.getElementById('chat').innerHTML = `
    <div class="welcome-state">
      <div class="welcome-icon">🎓</div>
      <h3>Welcome to StudyMind AI</h3>
      <p>Ask any study-related question and get instant, intelligent answers powered by Claude AI.</p>
      <div class="quick-start">
        <div class="qs-label">TRY THESE QUESTIONS</div>
        <div class="qs-grid" id="suggestions-grid"></div>
      </div>
    </div>
  `;
  updateSuggestions();
}

// === ASK QUESTION ===
async function askQuestion() {
  if (isLoading) return;

  const input = document.getElementById('question-input');
  const question = input.value.trim();
  if (!question) return;

  const sendBtn = document.getElementById('send-btn');
  isLoading = true;
  sendBtn.disabled = true;
  input.value = '';
  autoResize(input);

  // Remove welcome state
  const welcome = document.querySelector('.welcome-state');
  if (welcome) welcome.remove();

  // Add user bubble
  appendMessage('user', question);

  // Update stats
  questionCount++;
  const qEl = document.getElementById('q-count');
  if (qEl) qEl.textContent = questionCount;

  // Add typing indicator
  const typingId = 'typing-' + Date.now();
  appendTyping(typingId);

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        subject: currentSubject,
        history: chatHistory
      })
    });

    const data = await response.json();

    // Remove typing indicator
    removeTyping(typingId);

    if (data.error) {
      appendError(data.error);
    } else {
      // Update history
      chatHistory.push({ role: 'user', content: question });
      chatHistory.push({ role: 'assistant', content: data.answer });

      // Keep history manageable
      if (chatHistory.length > 20) {
        chatHistory = chatHistory.slice(-20);
      }

      appendMessage('ai', data.answer, data.timestamp);
    }

  } catch (err) {
    removeTyping(typingId);
    appendError('Server se connection fail. Flask server chal raha hai? (python app.py)');
  }

  isLoading = false;
  sendBtn.disabled = false;
  input.focus();
}

// === DOM HELPERS ===
function appendMessage(role, text, timestamp = null) {
  const chat = document.getElementById('chat');
  const wrap = document.createElement('div');
  wrap.className = `msg-wrap ${role}`;

  const now = timestamp || new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

  if (role === 'user') {
    wrap.innerHTML = `
      <div>
        <div class="bubble-user">${escHtml(text)}</div>
        <div class="msg-meta" style="text-align:right">${now}</div>
      </div>
    `;
  } else {
    wrap.innerHTML = `
      <div class="ai-row">
        <div class="ai-avatar">🎓</div>
        <div>
          <div class="bubble-ai">${formatAnswer(text)}</div>
          <div class="msg-meta">${now} · StudyMind AI</div>
        </div>
      </div>
    `;
  }

  chat.appendChild(wrap);
  wrap.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function appendTyping(id) {
  const chat = document.getElementById('chat');
  const wrap = document.createElement('div');
  wrap.className = 'msg-wrap ai';
  wrap.id = id;
  wrap.innerHTML = `
    <div class="ai-row">
      <div class="ai-avatar">🎓</div>
      <div class="bubble-ai">
        <div class="typing-dots">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
    </div>
  `;
  chat.appendChild(wrap);
  wrap.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function appendError(msg) {
  const chat = document.getElementById('chat');
  const wrap = document.createElement('div');
  wrap.className = 'msg-wrap ai';
  wrap.innerHTML = `
    <div class="ai-row">
      <div class="ai-avatar">⚠️</div>
      <div class="bubble-error">⚠️ ${escHtml(msg)}</div>
    </div>
  `;
  chat.appendChild(wrap);
  wrap.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

// === FORMAT HELPERS ===
function escHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatAnswer(text) {
  // Code blocks
  text = text.replace(/```([\s\S]*?)```/g, (_, code) =>
    `<div class="code-block">${escHtml(code.trim())}</div>`
  );

  // Bold
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Italic
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Inline code
  text = text.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;font-size:12px;color:#7dd3fc">$1</code>');

  // Paragraphs
  text = text.replace(/\n\n/g, '</p><p style="margin-top:10px">');
  text = text.replace(/\n/g, '<br>');

  return '<p>' + text + '</p>';
}
