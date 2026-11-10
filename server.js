const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = "super_secret_game_key_123";
const DB_FILE = path.join(__dirname, 'database.json');

// --- НАСТРОЙКА ПОЧТЫ ---
// ВАЖНО: Если не хотите настраивать почту, закомментируйте блок ниже,
// иначе сервер может падать при регистрации.
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'ВАША_ПОЧТА@gmail.com', 
        pass: 'ВАШ_ПАРОЛЬ_ПРИЛОЖЕНИЯ' 
    }
});

async function sendEmail(to, subject, text) {
    try {
        await transporter.sendMail({
            from: '"Сервер игры" <ВАША_ПОЧТА@gmail.com>',
            to: to,
            subject: subject,
            text: text
        });
        console.log(`Письмо успешно отправлено на ${to}`);
    } catch (error) {
        console.error("Ошибка при отправке письма:", error);
    }
}

// --- БАЗА ДАННЫХ ---
let db = { users: [], messages: [] };
if (fs.existsSync(DB_FILE)) {
    try { db = JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); } catch (e) {}
}
function saveDB() { fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2)); }

// --- ТОКЕНЫ ---
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    if (!token) return res.status(401).json({ error: "Нет доступа. Войдите в аккаунт." });

    jwt.verify(token, JWT_SECRET, (err, decoded) => {
        if (err) return res.status(403).json({ error: "Неверный токен" });
        req.userId = decoded.userId;
        next();
    });
}

// ==========================================
// 1. АККАУНТЫ (ИСПРАВЛЕНЫ ПУТИ И ПОЛЯ)
// ==========================================

app.post('/register', async (req, res) => {
    try {
        // Принимаем name, nick или username (что пришлёт клиент)
        const { email, password } = req.body;
        const name = req.body.name || req.body.nick || req.body.username;

        if (!email || !password || !name) {
            return res.status(400).json({ error: "Заполните все поля (имя, почта, пароль)" });
        }

        const existingUser = db.users.find(u => u.email === email);
        if (existingUser) return res.status(400).json({ error: "Этот email уже занят" });

        const salt = await bcrypt.genSalt(10);
        const passwordHash = await bcrypt.hash(password, salt);

        const newUser = { id: Date.now().toString(), email, passwordHash, name, level: 1 };

        db.users.push(newUser);
        saveDB(); 

        // Отправляем письмо (если почта настроена)
        sendEmail(email, "Успешная регистрация", `Привет, ${name}! Твой аккаунт на сервере Veljano успешно создан.`);

        res.json({ success: true, message: "Аккаунт создан!", user: { id: newUser.id, name: newUser.name, email: newUser.email } });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Ошибка сервера" });
    }
});

app.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = db.users.find(u => u.email === email);
        if (!user) return res.status(400).json({ error: "Неверный email или пароль" });

        const isMatch = await bcrypt.compare(password, user.passwordHash);
        if (!isMatch) return res.status(400).json({ error: "Неверный email или пароль" });

        const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

        sendEmail(email, "Вход в аккаунт", `Вы только что вошли в свой аккаунт ${user.name}.`);

        res.json({ success: true, token, user: { id: user.id, name: user.name, email: user.email } });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Ошибка сервера" });
    }
});

// ==========================================
// 2. ПРОФИЛИ И ПОИСК
// ==========================================

app.get('/profile', authenticateToken, (req, res) => {
    const user = db.users.find(u => u.id === req.userId);
    if (!user) return res.status(404).json({ error: "Пользователь не найден" });
    const { passwordHash, ...safeUser } = user;
    res.json(safeUser);
});

app.get('/search', (req, res) => {
    const searchName = req.query.name;
    if (!searchName) return res.status(400).json({ error: "Укажите ник" });

    const players = db.users
        .filter(u => u.name.toLowerCase().includes(searchName.toLowerCase()))
        .map(u => ({ id: u.id, name: u.name, level: u.level }));

    res.json(players);
});

app.get('/player/:id', (req, res) => {
    const player = db.users.find(u => u.id === req.params.id);
    if (!player) return res.status(404).json({ error: "Игрок не найден" });
    res.json({ id: player.id, name: player.name, level: player.level });
});

// ==========================================
// 3. ЧАТ
// ==========================================

app.post('/chat', authenticateToken, (req, res) => {
    const { text } = req.body;
    if (!text) return res.status(400).json({ error: "Пустое сообщение" });

    const user = db.users.find(u => u.id === req.userId);
    const newMessage = { playerId: user.id, playerName: user.name, text, timestamp: new Date().toISOString() };

    db.messages.push(newMessage);
    if (db.messages.length > 100) db.messages.shift();
    saveDB(); 

    res.json({ success: true });
});

app.get('/chat', (req, res) => {
    res.json(db.messages);
});

// --- ЗАПУСК ---
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Сервер запущен на порту ${PORT}`));
