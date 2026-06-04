const API_BASE_URL = 'http://localhost:5000/api';

const API = {
    async register(username, password, role = 0) {
        const res = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password, role})
        });
        return res.json();
    },

    async login(username, password) {
        const res = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        return res.json();
    },

    async getUserInfo(userId) {
        const res = await fetch(`${API_BASE_URL}/user/info?user_id=${userId}`);
        return res.json();
    },

    async getExams(userId) {
        let url = `${API_BASE_URL}/exams`;
        if (userId) url += `?user_id=${userId}`;
        const res = await fetch(url);
        return res.json();
    },

    async getExamDetail(examId, recordId) {
        let url = `${API_BASE_URL}/exam/${examId}`;
        if (recordId) url += `?record_id=${recordId}`;
        const res = await fetch(url);
        return res.json();
    },

    async createExam(examName, durationMinutes, questionIds, shuffleEnabled = 0) {
        const res = await fetch(`${API_BASE_URL}/exam/create`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({exam_name: examName, duration_minutes: durationMinutes, question_ids: questionIds, shuffle_enabled: shuffleEnabled})
        });
        return res.json();
    },

    async startExam(userId, examId) {
        const res = await fetch(`${API_BASE_URL}/exam/start`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: userId, exam_id: examId})
        });
        return res.json();
    },

    async submitExam(recordId, answers) {
        const res = await fetch(`${API_BASE_URL}/exam/submit`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({record_id: recordId, answers})
        });
        return res.json();
    },

    async getExamRecords(userId) {
        const res = await fetch(`${API_BASE_URL}/exam/records?user_id=${userId}`);
        return res.json();
    },

    async getAllExamRecords() {
        const res = await fetch(`${API_BASE_URL}/exam/records/all`);
        return res.json();
    },

    async getExamsManage() {
        const res = await fetch(`${API_BASE_URL}/exams/manage`);
        return res.json();
    },

    async deleteExam(examId) {
        const res = await fetch(`${API_BASE_URL}/exam/${examId}/delete`, {
            method: 'DELETE'
        });
        return res.json();
    },

    async getStudents() {
        const res = await fetch(`${API_BASE_URL}/students`);
        return res.json();
    },

    async getWrongQuestions(userId) {
        const res = await fetch(`${API_BASE_URL}/wrong_questions?user_id=${userId}`);
        return res.json();
    },

    async getQuestions(page = 1, pageSize = 20, knowledge = '', difficulty = '') {
        let url = `${API_BASE_URL}/questions?page=${page}&page_size=${pageSize}`;
        if (knowledge) url += `&knowledge=${encodeURIComponent(knowledge)}`;
        if (difficulty) url += `&difficulty=${difficulty}`;
        const res = await fetch(url);
        return res.json();
    },

    async createQuestion(questionData) {
        const res = await fetch(`${API_BASE_URL}/question/create`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(questionData)
        });
        return res.json();
    },

    async updateQuestion(questionId, questionData) {
        const res = await fetch(`${API_BASE_URL}/question/update/${questionId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(questionData)
        });
        return res.json();
    },

    async deleteQuestion(questionId) {
        const res = await fetch(`${API_BASE_URL}/question/delete/${questionId}`, {
            method: 'DELETE'
        });
        return res.json();
    },

    async aiExplain(questionId, userId, userAnswer) {
        const res = await fetch(`${API_BASE_URL}/ai/explain`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question_id: questionId, user_id: userId, user_answer: userAnswer})
        });
        return res.json();
    },

    async aiGenerateQuestions(knowledge, difficulty, count) {
        const res = await fetch(`${API_BASE_URL}/ai/generate/questions`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({knowledge, difficulty, count})
        });
        return res.json();
    },

    async aiSummary(recordId) {
        const res = await fetch(`${API_BASE_URL}/ai/summary`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({record_id: recordId})
        });
        return res.json();
    },

    async getAiConfigStatus() {
        const res = await fetch(`${API_BASE_URL}/ai/config`);
        return res.json();
    }
};

const Auth = {
    saveUser(userData) {
        localStorage.setItem('user', JSON.stringify(userData));
    },

    getUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    logout() {
        localStorage.removeItem('user');
        window.location.href = '/login';
    },

    requireAuth() {
        const user = this.getUser();
        if (!user) {
            window.location.href = '/login';
            return null;
        }
        return user;
    }
};

function showError(msg) {
    const el = document.querySelector('.error-msg');
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
    }
}

function showSuccess(msg) {
    const el = document.querySelector('.success-msg');
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
    }
}

function hideMsg() {
    const errorEl = document.querySelector('.error-msg');
    const successEl = document.querySelector('.success-msg');
    if (errorEl) errorEl.style.display = 'none';
    if (successEl) successEl.style.display = 'none';
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const d = new Date(dateStr);
    return d.toLocaleString('zh-CN');
}
