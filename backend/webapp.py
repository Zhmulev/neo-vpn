from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings

webapp = FastAPI(title="NEO VPN Panel")
API_URL = settings.BACKEND_URL

@webapp.get("/", response_class=HTMLResponse)
async def home():
    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' fill='%2300D4FF'>⚡</text></svg>">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEO VPN + Proxy Utility</title>
    <style>
        :root { --bg: #0a0a0f; --card: #141420; --border: #2a2a3a; --accent: #00d4ff; --text: #fff; --muted: #888; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; scroll-behavior: smooth; }
        body { background: var(--bg); color: var(--text); min-height: 100vh; }
        .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
        nav { display: flex; align-items: center; justify-content: space-between; padding: 24px 20px; border-bottom: 1px solid var(--border); }
        .logo { font-size: 24px; font-weight: 900; color: var(--accent); letter-spacing: 2px; }
        nav a { color: var(--muted); text-decoration: none; margin-left: 24px; font-size: 14px; }
        nav a:hover { color: var(--text); }
        .hero { text-align: center; padding: 80px 20px 60px; }
        .hero h1 { font-size: 56px; font-weight: 900; line-height: 1.1; margin-bottom: 16px; background: linear-gradient(135deg, #00d4ff, #7b2fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { color: var(--muted); font-size: 20px; max-width: 600px; margin: 0 auto 32px; }
        .btn { display: inline-block; padding: 14px 32px; background: var(--accent); color: #000; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; transition: 0.2s; }
        .btn:hover { opacity: 0.85; transform: translateY(-2px); }
        .btn.outline { background: transparent; color: var(--accent); border: 1px solid var(--accent); }
        .btn.small { padding: 10px 20px; font-size: 14px; }
        .section { padding: 60px 20px; }
        .section h2 { font-size: 32px; margin-bottom: 32px; text-align: center; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 32px; text-align: center; }
        .card h3 { margin-bottom: 8px; }
        .card .price { font-size: 40px; font-weight: 900; color: var(--accent); margin: 16px 0; }
        .card ul { list-style: none; text-align: left; margin: 24px 0; }
        .card li { padding: 8px 0; color: var(--muted); }
        .card li::before { content: "✓ "; color: var(--accent); font-weight: bold; }
        .card.featured { border-color: var(--accent); }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
        .feature { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; text-align: center; }
        .feature h4 { margin-bottom: 8px; color: var(--accent); }
        .feature p { color: var(--muted); font-size: 14px; }
        .auth-form { max-width: 400px; margin: 0 auto; }
        .auth-form input { width: 100%; padding: 14px; margin-bottom: 12px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-size: 16px; }
        .auth-form input:focus { outline: none; border-color: var(--accent); }
        .msg { display: none; padding: 16px; border-radius: 8px; margin-top: 16px; }
        .msg.success { display: block; background: #0a2a1a; color: #00ff88; border: 1px solid #00ff88; }
        .msg.error { display: block; background: #2a0a0a; color: #ff4444; border: 1px solid #ff4444; }
        .tabs { display: flex; gap: 12px; justify-content: center; margin-bottom: 24px; }
        .tab { padding: 10px 24px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; cursor: pointer; font-size: 14px; }
        .tab.active { background: var(--accent); color: #000; font-weight: bold; }
        .dashboard { display: none; max-width: 800px; margin: 0 auto; }
        .proxy-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 12px; text-align: left; }
        .proxy-card .copy-btn { float: right; padding: 6px 14px; background: var(--accent); color: #000; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; }
        .proxy-string { font-family: monospace; color: #00ff88; word-break: break-all; }
        .config-block { background: #0d0d14; border: 1px solid var(--border); border-radius: 8px; padding: 16px; font-family: monospace; font-size: 13px; white-space: pre-wrap; word-break: break-all; color: #00ff88; }
        .balance-box { background: var(--card); border: 1px solid var(--accent); border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 24px; }
        .balance-box .amount { font-size: 40px; font-weight: 900; color: var(--accent); }
        footer { text-align: center; padding: 40px 20px; border-top: 1px solid var(--border); color: var(--muted); font-size: 14px; }
        @media (max-width: 768px) {
            .hero h1 { font-size: 36px; }
            nav a { display: none; }
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">NEO VPN</div>
        <div>
            <a href="#features">Возможности</a>
            <a href="#pricing">Тарифы</a>
            <a href="#auth">Вход</a>
        </div>
    </nav>

    <div class="hero">
        <h1>Сеть нового поколения</h1>
        <p>Безопасный VPN и прокси-утилита в одном сервисе. Один ключ от всех дверей интернета.</p>
        <a href="#auth" class="btn">Получить 3 дня бесплатно →</a>
    </div>

    <div class="section" id="features">
        <div class="container">
            <h2>Почему NEO</h2>
            <div class="features">
                <div class="feature">
                    <h4>⚡ V2Ray</h4>
                    <p>Маскировка под обычный трафик</p>
                </div>
                <div class="feature">
                    <h4>🛡 Без логов</h4>
                    <p>Мы не храним историю посещений</p>
                </div>
                <div class="feature">
                    <h4>🔀 Proxy Utility</h4>
                    <p>Создавай SOCKS5/HTTP прокси в 1 клик</p>
                </div>
                <div class="feature">
                    <h4>🌍 География</h4>
                    <p>Серверы в ЕС, США и Азии</p>
                </div>
            </div>
        </div>
    </div>

    <div class="section" id="pricing">
        <div class="container">
            <h2>Тарифы</h2>
            <div class="cards">
                <div class="card">
                    <h3>Базовый</h3>
                    <div class="price">99₽<span style="font-size:16px;color:#888">/мес</span></div>
                    <ul>
                        <li>Все VPN-серверы</li>
                        <li>1 статический прокси</li>
                        <li>Безлимитный трафик</li>
                    </ul>
                    <button class="btn outline" onclick="alert('Оплата скоро!')">Выбрать</button>
                </div>
                <div class="card featured">
                    <h3>Pro</h3>
                    <div class="price">199₽<span style="font-size:16px;color:#888">/мес</span></div>
                    <ul>
                        <li>Все VPN-серверы</li>
                        <li>5 прокси с ротацией</li>
                        <li>Доступ к API</li>
                        <li>Приоритетная поддержка</li>
                    </ul>
                    <button class="btn" onclick="alert('Оплата скоро!')">Выбрать</button>
                </div>
            </div>
        </div>
    </div>

    <div class="section" id="auth">
        <div class="container">
            <h2>Личный кабинет</h2>
            <div class="tabs">
                <div class="tab active" id="tabLogin" onclick="switchTab('login')">Вход</div>
                <div class="tab" id="tabRegister" onclick="switchTab('register')">Регистрация</div>
            </div>

            <div class="auth-form" id="loginForm">
                <input type="email" id="loginEmail" placeholder="Email">
                <input type="password" id="loginPassword" placeholder="Пароль">
                <button class="btn" style="width:100%" onclick="loginUser()">Войти</button>
                <div class="msg" id="loginMsg"></div>
            </div>

            <div class="auth-form" id="registerForm" style="display:none">
                <input type="email" id="regEmail" placeholder="Email">
                <input type="text" id="regUsername" placeholder="Username">
                <input type="password" id="regPassword" placeholder="Пароль">
                <button class="btn" style="width:100%" onclick="registerUser()">Создать аккаунт</button>
                <div class="msg" id="regMsg"></div>
            </div>

            <div class="dashboard" id="dashboard">
                <h3 style="text-align:center;margin-bottom:20px">👋 Добро пожаловать, <span id="userName"></span>!</h3>
                <div class="balance-box">
                    <div style="color:#888;font-size:14px;margin-bottom:8px">Текущий баланс</div>
                    <div class="amount" id="balanceAmount">0₽</div>
                </div>
                <div style="display:flex;gap:12px;justify-content:center;margin-bottom:30px;flex-wrap:wrap">
                    <button class="btn small" onclick="topUpBalance()">💳 Пополнить</button>
                    <button class="btn small" onclick="loadServers()">🌍 Серверы</button>
                    <button class="btn small" onclick="loadConfigs()">📡 VPN конфиги</button>
                    <button class="btn small" onclick="createProxy()">🔀 Создать прокси</button>
                    <button class="btn small" onclick="loadMyProxies()">📋 Мои прокси</button>
                </div>
                <div id="contentArea"></div>
            </div>
        </div>
    </div>

    <footer>
        NEO VPN © 2026 — Свобода в сети
    </footer>

    <script>
        let currentUserId = null;

        function switchTab(tab) {
            if (tab === 'login') {
                document.getElementById('loginForm').style.display = 'block';
                document.getElementById('registerForm').style.display = 'none';
                document.getElementById('tabLogin').classList.add('active');
                document.getElementById('tabRegister').classList.remove('active');
            } else {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('registerForm').style.display = 'block';
                document.getElementById('tabRegister').classList.add('active');
                document.getElementById('tabLogin').classList.remove('active');
            }
        }

        function showDashboard(userId, username) {
            currentUserId = userId;
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            document.getElementById('userName').textContent = username;
            loadBalance();
        }

        async function loadBalance() {
            try {
                const response = await fetch(`http://127.0.0.1:8000/payment/balance/${currentUserId}`);
                const data = await response.json();
                document.getElementById('balanceAmount').textContent = data.balance + '₽';
            } catch (e) {}
        }

        async function topUpBalance() {
            const amount = prompt('Введите сумму пополнения (₽):', '100');
            if (!amount || isNaN(amount)) return;
            try {
                const response = await fetch('http://127.0.0.1:8000/payment/topup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: currentUserId, amount: parseFloat(amount) })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(`✅ Баланс пополнен на ${amount}₽`);
                    loadBalance();
                } else {
                    alert('❌ ' + (data.detail || 'Ошибка'));
                }
            } catch (e) {
                alert('❌ Ошибка соединения');
            }
        }

        async function loginUser() {
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            const msg = document.getElementById('loginMsg');

            if (!email || !password) {
                msg.className = 'msg error';
                msg.textContent = 'Заполни все поля';
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:8000/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await response.json();
                if (response.ok) {
                    msg.className = 'msg success';
                    msg.textContent = '✅ Вход выполнен!';
                    showDashboard(data.user_id, data.username);
                } else {
                    msg.className = 'msg error';
                    msg.textContent = '❌ ' + (data.detail || 'Ошибка входа');
                }
            } catch (e) {
                msg.className = 'msg error';
                msg.textContent = '❌ Не удалось подключиться к серверу';
            }
        }

        async function registerUser() {
            const email = document.getElementById('regEmail').value;
            const username = document.getElementById('regUsername').value;
            const password = document.getElementById('regPassword').value;
            const msg = document.getElementById('regMsg');

            if (!email || !username || !password) {
                msg.className = 'msg error';
                msg.textContent = 'Заполни все поля';
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:8000/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, username, password })
                });
                const data = await response.json();
                if (response.ok) {
                    msg.className = 'msg success';
                    msg.textContent = '✅ Аккаунт создан!';
                    showDashboard(data.id, username);
                } else {
                    msg.className = 'msg error';
                    msg.textContent = '❌ ' + (data.detail || 'Ошибка регистрации');
                }
            } catch (e) {
                msg.className = 'msg error';
                msg.textContent = '❌ Не удалось подключиться к серверу';
            }
        }

        async function loadServers() {
            const area = document.getElementById('contentArea');
            area.innerHTML = '<p style="color:#888">Загрузка серверов...</p>';
            try {
                const response = await fetch('http://127.0.0.1:8000/vpn/servers');
                const servers = await response.json();
                let html = '<h4 style="margin-bottom:16px">🌍 Доступные серверы</h4>';
                servers.forEach(s => {
                    html += `<div class="proxy-card">
                        <strong>${s.name}</strong> — ${s.country}, ${s.city}
                        <span style="color:#00ff88;float:right">● Online</span>
                    </div>`;
                });
                area.innerHTML = html;
            } catch (e) {
                area.innerHTML = '<p style="color:#ff4444">Ошибка загрузки серверов</p>';
            }
        }

        async function loadConfigs() {
            const area = document.getElementById('contentArea');
            area.innerHTML = '<p style="color:#888">Загрузка конфигов...</p>';
            try {
                const response = await fetch('http://127.0.0.1:8000/vpn/servers');
                const servers = await response.json();
                let html = '<h4 style="margin-bottom:16px">📡 VPN конфиги</h4>';
                for (const server of servers) {
                    const config = server.v2ray_config || `vless://${server.public_key}@${server.endpoint}:${server.port}?encryption=none&security=none&type=ws&path=%2Fneo#NEO-VPN`;
                    html += `<div class="proxy-card">
                        <span class="copy-btn" onclick="copyConfig('${server.id}')">Копировать</span>
                        <strong>${server.name}</strong> — ${server.country}, ${server.city}<br><br>
                        <div class="config-block" id="config-${server.id}">${config}</div>
                    </div>`;
                }
                area.innerHTML = html;
            } catch (e) {
                area.innerHTML = '<p style="color:#ff4444">Ошибка загрузки конфигов</p>';
            }
        }

        async function createProxy() {
            if (!currentUserId) {
                alert('Сначала войди!');
                return;
            }
            const area = document.getElementById('contentArea');
            area.innerHTML = '<p style="color:#888">Создаём прокси...</p>';
            try {
                const response = await fetch(`http://127.0.0.1:8000/proxy/create?user_id=${currentUserId}&server_id=1&proxy_type=socks5`, {
                    method: 'POST'
                });
                const data = await response.json();
                if (response.ok) {
                    area.innerHTML = `<div class="proxy-card">
                        <strong>✅ Прокси создан!</strong><br><br>
                        <span>Тип: ${data.proxy_type}</span><br>
                        <span>Сервер: ${data.server} (${data.country})</span><br>
                        <span>Логин: ${data.proxy_login}</span><br>
                        <span>Пароль: ${data.proxy_password}</span><br><br>
                        <span>Строка подключения:</span><br>
                        <span class="proxy-string">${data.proxy_string}</span>
                    </div>`;
                } else {
                    area.innerHTML = `<p style="color:#ff4444">${data.detail || 'Ошибка создания прокси'}</p>`;
                }
            } catch (e) {
                area.innerHTML = '<p style="color:#ff4444">Ошибка соединения</p>';
            }
        }

        async function loadMyProxies() {
            if (!currentUserId) {
                alert('Сначала войди!');
                return;
            }
            const area = document.getElementById('contentArea');
            area.innerHTML = '<p style="color:#888">Загрузка прокси...</p>';
            try {
                const response = await fetch(`http://127.0.0.1:8000/proxy/my?user_id=${currentUserId}`);
                const proxies = await response.json();
                if (proxies.length === 0) {
                    area.innerHTML = '<p style="color:#888">У тебя пока нет прокси.</p>';
                } else {
                    let html = '<h4 style="margin-bottom:16px">📋 Мои прокси</h4>';
                    proxies.forEach(p => {
                        html += `<div class="proxy-card">
                            <span class="copy-btn" onclick="copyText('${p.id}')">Копировать</span>
                            <strong>${p.proxy_type.toUpperCase()}</strong> — ${p.proxy_login}<br>
                            <span class="proxy-string" id="proxy-${p.id}">${p.proxy_login}:${p.proxy_password}@server:${p.local_port}</span>
                        </div>`;
                    });
                    area.innerHTML = html;
                }
            } catch (e) {
                area.innerHTML = '<p style="color:#ff4444">Ошибка загрузки</p>';
            }
        }

        function copyConfig(id) {
            const text = document.getElementById('config-' + id).textContent;
            navigator.clipboard.writeText(text).then(() => alert('Конфиг скопирован!'));
        }

        function copyText(id) {
            const text = document.getElementById('proxy-' + id).textContent;
            navigator.clipboard.writeText(text).then(() => alert('Скопировано!'));
        }
    </script>
</body>
</html>
    """
    return html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(webapp, host="0.0.0.0", port=8080)