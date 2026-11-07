const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const fs = require('fs'); // Встроенный модуль для работы с файлами
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = "super_secret_game_key_123";
const DB_FILE = path.join(__dirname, 'database.json');

// --- ИНИЦИАЛИЗАЦИЯ "БАЗЫ ДАННЫХ" (ФАЙЛА) ---
let db = { users: [], messages: [] };

// Если файл с базой существует — читаем его при запуске
if (fs.existsSync(DB_FILE)) {
    try {
        const data = fs.readFileSync(DB_FILE, 'utf8');
        db = JSON.parse(data);
    } catch (e) {
        console.log("Ошибка чтения базы, создаем новую.");
    }
}

// Функция для сохранения изменений в файл
function saveDB() {
    fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
}

// --- MIDDLEWARE (Проверка токена) ---
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) return res.status(401).json({ error: "Нет доступа. Войдите в аккаунт." });

    jwt.verify(token, JWT_SECRET, (err, decoded) => {
        if (err) return res.status(403).json({ error: "Неверный или истекший токен" });
        req.userId = decoded.userId;
        next();
    });
}

// ==========================================
// 1. АККАУНТЫ (РЕГИСТРАЦИЯ И ВХОД)
// ==========================================

app.post('/api/register', async (req, res) => {
    try {
        const { email, password, name } = req.body;

        if (!email || !password || !name) {
            return res.status(400).json({ error: "Заполните email, пароль и имя" });
        }

        const existingUser = db.users.find(u => u.email === email);
        if (existingUser) {
            return res.status(400).json({ error: "Этот email уже зарегистрирован" });
        }

        const salt = await bcrypt.genSalt(10);
        const passwordHash = await bcrypt.hash(password, salt);

        const newUser = {
            id: Date.now().toString(),
            email: email,
            passwordHash: passwordHash,
            name: name,
            level: 1
        };

        db.users.push(newUser);
        saveDB(); // Сохраняем в файл

        res.json({ success: true, message: "Аккаунт успешно создан!" });
    } catch (error) {
        res.status(500).json({ error: "Ошибка сервера при регистрации" });
    }
});

app.post('/api/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        const user = db.users.find(u => u.email === email);
        if (!user) {
            return res.status(400).json({ error: "Неверный email или пароль" });
        }

        const isMatch = await bcrypt.compare(password, user.passwordHash);
        if (!isMatch) {
            return res.status(400).json({ error: "Неверный email или пароль" });
        }

        const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

        res.json({ 
            success: true, 
            token: token, 
            user: { id: user.id, name: user.name, email: user.email } 
        });
    } catch (error) {
        res.status(500).json({ error: "Ошибка сервера при входе" });
    }
});

// ==========================================
// 2. ПРОФИЛИ И ПОИСК ИГРОКОВ
// ==========================================

app.get('/api/profile', authenticateToken, (req, res) => {
    const user = db.users.find(u => u.id === req.userId);
    if (!user) return res.status(404).json({ error: "Пользователь не найден" });
    
    // Убираем пароль из ответа
    const { passwordHash, ...safeUser } = user;
    res.json(safeUser);
});

app.get('/api/search', (req, res) => {
    const searchName = req.query.name;
    if (!searchName) return res.status(400).json({ error: "Укажите ник для поиска" });

    // Ищем совпадения без учета регистра
    const players = db.users
        .filter(u => u.name.toLowerCase().includes(searchName.toLowerCase()))
        .map(u => ({ id: u.id, name: u.name, level: u.level })); // Не отдаем email и пароли

    res.json(players);
});

app.get('/api/player/:id', (req, res) => {
    const player = db.users.find(u => u.id === req.params.id);
    if (!player) return res.status(404).json({ error: "Игрок не найден" });
    
    res.json({ id: player.id, name: player.name, level: player.level });
});

// ==========================================
// 3. ЧАТ
// ==========================================

app.post('/api/chat', authenticateToken, (req, res) => {
    const { text } = req.body;
    if (!text) return res.status(400).json({ error: "Пустое сообщение" });

    const user = db.users.find(u => u.id === req.userId);

    const newMessage = {
        playerId: user.id,
        playerName: user.name,
        text: text,
        timestamp: new Date().toISOString()
    };

    db.messages.push(newMessage);
    
    // Храним только последние 100 сообщений, чтобы файл не разрастался
    if (db.messages.length > 100) {
        db.messages.shift();
    }

    saveDB(); // Сохраняем в файл
    res.json({ success: true });
});

app.get('/api/chat', (req, res) => {
    res.json(db.messages);
});

// --- ЗАПУСК ---
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Сервер запущен на порту ${PORT}`));
