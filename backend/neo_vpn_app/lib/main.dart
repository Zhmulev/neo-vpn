import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(NeoVpnApp());
}

class NeoVpnApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NEO VPN',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Color(0xFF0A0A0F),
        primaryColor: Color(0xFF00D4FF),
        fontFamily: 'Segoe UI',
      ),
      home: AuthScreen(),
    );
  }
}

class AuthScreen extends StatefulWidget {
  @override
  _AuthScreenState createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _usernameController = TextEditingController();

  bool _isLogin = true;
  bool _loading = false;
  String _message = '';

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _message = '';
    });

    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();
    final username = _usernameController.text.trim();

    if (email.isEmpty || password.isEmpty || (!_isLogin && username.isEmpty)) {
      setState(() {
        _loading = false;
        _message = 'Заполни все поля';
      });
      return;
    }

    final url = _isLogin
        ? 'http://127.0.0.1:8000/auth/login'
        : 'http://127.0.0.1:8000/auth/register';

    final body = _isLogin
        ? jsonEncode({'email': email, 'password': password})
        : jsonEncode({'email': email, 'username': username, 'password': password});

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: body,
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => HomeScreen(
              userId: data['user_id'] ?? data['id'] ?? 0,
              username: data['username'] ?? (username.isNotEmpty ? username : email.split('@')[0]),
              trialEnd: data['trial_end'] ?? '',
            ),
          ),
        );
      } else {
        final data = jsonDecode(response.body);
        setState(() {
          _loading = false;
          _message = data['detail'] ?? 'Ошибка';
        });
      }
    } catch (e) {
      setState(() {
        _loading = false;
        _message = 'Не удалось подключиться к серверу';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'NEO VPN',
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF00D4FF),
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Сеть нового поколения',
                style: TextStyle(color: Color(0xFF888888), fontSize: 16),
              ),
              SizedBox(height: 40),
              Container(
                padding: EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Color(0xFF141420),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Color(0xFF2A2A3A)),
                ),
                child: Column(
                  children: [
                    if (!_isLogin)
                      TextField(
                        controller: _usernameController,
                        style: TextStyle(color: Colors.white),
                        decoration: InputDecoration(
                          labelText: 'Username',
                          labelStyle: TextStyle(color: Color(0xFF888888)),
                          enabledBorder: UnderlineInputBorder(
                            borderSide: BorderSide(color: Color(0xFF2A2A3A)),
                          ),
                          focusedBorder: UnderlineInputBorder(
                            borderSide: BorderSide(color: Color(0xFF00D4FF)),
                          ),
                        ),
                      ),
                    TextField(
                      controller: _emailController,
                      style: TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        labelText: 'Email',
                        labelStyle: TextStyle(color: Color(0xFF888888)),
                        enabledBorder: UnderlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF2A2A3A)),
                        ),
                        focusedBorder: UnderlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF00D4FF)),
                        ),
                      ),
                    ),
                    TextField(
                      controller: _passwordController,
                      obscureText: true,
                      style: TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        labelText: 'Пароль',
                        labelStyle: TextStyle(color: Color(0xFF888888)),
                        enabledBorder: UnderlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF2A2A3A)),
                        ),
                        focusedBorder: UnderlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF00D4FF)),
                        ),
                      ),
                    ),
                    SizedBox(height: 24),
                    _loading
                        ? CircularProgressIndicator(color: Color(0xFF00D4FF))
                        : ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Color(0xFF00D4FF),
                              foregroundColor: Colors.black,
                              minimumSize: Size(double.infinity, 50),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(10),
                              ),
                            ),
                            onPressed: _submit,
                            child: Text(
                              _isLogin ? 'Войти' : 'Создать аккаунт',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                    if (_message.isNotEmpty)
                      Padding(
                        padding: EdgeInsets.only(top: 16),
                        child: Text(
                          _message,
                          style: TextStyle(color: Color(0xFFFF4444)),
                          textAlign: TextAlign.center,
                        ),
                      ),
                    TextButton(
                      onPressed: () {
                        setState(() {
                          _isLogin = !_isLogin;
                          _message = '';
                        });
                      },
                      child: Text(
                        _isLogin
                            ? 'Нет аккаунта? Зарегистрируйся'
                            : 'Уже есть аккаунт? Войди',
                        style: TextStyle(color: Color(0xFF00D4FF)),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  final int userId;
  final String username;
  final String trialEnd;

  HomeScreen({required this.userId, required this.username, required this.trialEnd});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool isConnected = false;
  List<dynamic> _servers = [];
  String _selectedServer = 'Загрузка серверов...';
  bool _serversLoaded = false;
  double _balance = 0;
  String _plan = 'trial';

  @override
  void initState() {
    super.initState();
    _loadServers();
    _loadBalance();
  }

  Future<void> _loadBalance() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/payment/balance/${widget.userId}'),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _balance = (data['balance'] ?? 0).toDouble();
        });
      }
    } catch (e) {
      // Ошибка загрузки баланса
    }
  }

  Future<void> _topUpBalance() async {
    final amountController = TextEditingController();
    final result = await showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: Color(0xFF141420),
          title: Text('Пополнить баланс', style: TextStyle(color: Colors.white)),
          content: TextField(
            controller: amountController,
            keyboardType: TextInputType.number,
            style: TextStyle(color: Colors.white),
            decoration: InputDecoration(
              hintText: 'Сумма (₽)',
              hintStyle: TextStyle(color: Color(0xFF888888)),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Отмена', style: TextStyle(color: Color(0xFF888888))),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF00D4FF),
                foregroundColor: Colors.black,
              ),
              onPressed: () => Navigator.pop(context, amountController.text),
              child: Text('Пополнить'),
            ),
          ],
        );
      },
    );

    if (result != null && result.toString().isNotEmpty) {
      final amount = double.tryParse(result.toString());
      if (amount == null || amount <= 0) return;

      try {
        final response = await http.post(
          Uri.parse('http://127.0.0.1:8000/payment/topup'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': widget.userId, 'amount': amount}),
        );
        if (response.statusCode == 200) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('✅ Баланс пополнен на $amount₽'),
              backgroundColor: Color(0xFF00FF88),
            ),
          );
          _loadBalance();
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('❌ Ошибка пополнения')),
        );
      }
    }
  }

  Future<void> _showPlans() async {
    final result = await showModalBottomSheet(
      context: context,
      backgroundColor: Color(0xFF141420),
      builder: (context) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              title: Text('Базовый — 99₽/мес', style: TextStyle(color: Colors.white)),
              onTap: () => Navigator.pop(context, {'plan': 'basic', 'period': 'month'}),
            ),
            ListTile(
              title: Text('Pro — 199₽/мес', style: TextStyle(color: Colors.white)),
              onTap: () => Navigator.pop(context, {'plan': 'pro', 'period': 'month'}),
            ),
            ListTile(
              title: Text('Базовый — 5₽/день', style: TextStyle(color: Colors.white)),
              onTap: () => Navigator.pop(context, {'plan': 'basic', 'period': 'day'}),
            ),
            ListTile(
              title: Text('Pro — 9₽/день', style: TextStyle(color: Colors.white)),
              onTap: () => Navigator.pop(context, {'plan': 'pro', 'period': 'day'}),
            ),
          ],
        );
      },
    );

    if (result != null) {
      try {
        final response = await http.post(
          Uri.parse('http://127.0.0.1:8000/payment/subscribe'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': widget.userId,
            'plan': result['plan'],
            'period': result['period'],
            'auto_renew': false,
          }),
        );
        final data = jsonDecode(response.body);
        if (response.statusCode == 200) {
          setState(() {
            _plan = result['plan'];
          });
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('✅ Подписка активирована!'),
              backgroundColor: Color(0xFF00FF88),
            ),
          );
          _loadBalance();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('❌ ${data['detail'] ?? 'Ошибка'}')),
          );
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('❌ Ошибка соединения')),
        );
      }
    }
  }

  Future<void> _loadServers() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/vpn/servers'),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        setState(() {
          _servers = data;
          _selectedServer = data.isNotEmpty
              ? '${data[0]['country']} — ${data[0]['city']}'
              : 'Нет серверов';
          _serversLoaded = true;
        });
      }
    } catch (e) {
      setState(() {
        _selectedServer = 'Не удалось загрузить';
        _serversLoaded = true;
      });
    }
  }

  void toggleConnection() {
    setState(() {
      isConnected = !isConnected;
    });
  }

  void _showServerList() {
    if (!_serversLoaded || _servers.isEmpty) {
      _loadServers();
      return;
    }
    showModalBottomSheet(
      context: context,
      backgroundColor: Color(0xFF141420),
      builder: (context) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: _servers.map((server) {
            return ListTile(
              title: Text(
                '${server['country']} — ${server['city']}',
                style: TextStyle(color: Colors.white),
              ),
              onTap: () {
                setState(() {
                  _selectedServer = '${server['country']} — ${server['city']}';
                });
                Navigator.pop(context);
              },
            );
          }).toList(),
        );
      },
    );
  }

  Future<void> _openProxyScreen() async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ProxyScreen(userId: widget.userId),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'NEO VPN',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF00D4FF),
                    ),
                  ),
                  Icon(Icons.shield, color: Color(0xFF00D4FF), size: 28),
                ],
              ),
              SizedBox(height: 20),
              Text(
                '👋 ${widget.username}',
                style: TextStyle(color: Colors.white, fontSize: 18),
              ),
              SizedBox(height: 12),
              GestureDetector(
                onTap: _topUpBalance,
                child: Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Color(0xFF141420),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Color(0xFF00D4FF)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Баланс: ${_balance.toStringAsFixed(0)}₽',
                        style: TextStyle(color: Color(0xFF00D4FF), fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(width: 8),
                      Icon(Icons.add_circle, color: Color(0xFF00D4FF), size: 20),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 12),
              GestureDetector(
                onTap: _showPlans,
                child: Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Color(0xFF141420),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Color(0xFF2A2A3A)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Тариф: $_plan',
                        style: TextStyle(color: Colors.white, fontSize: 14),
                      ),
                      SizedBox(width: 8),
                      Icon(Icons.arrow_drop_down, color: Color(0xFF888888)),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 40),
              GestureDetector(
                onTap: toggleConnection,
                child: Container(
                  width: 160,
                  height: 160,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isConnected ? Color(0xFF00D4FF) : Color(0xFF141420),
                    border: Border.all(
                      color: isConnected ? Color(0xFF00D4FF) : Color(0xFF2A2A3A),
                      width: 3,
                    ),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        isConnected ? Icons.lock : Icons.lock_open,
                        size: 40,
                        color: isConnected ? Colors.black : Color(0xFF888888),
                      ),
                      SizedBox(height: 8),
                      Text(
                        isConnected ? 'ON' : 'OFF',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: isConnected ? Colors.black : Color(0xFF888888),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 20),
              Text(
                isConnected ? 'Защищено' : 'Не подключено',
                style: TextStyle(
                  fontSize: 16,
                  color: isConnected ? Color(0xFF00FF88) : Color(0xFF888888),
                ),
              ),
              SizedBox(height: 40),
              GestureDetector(
                onTap: _showServerList,
                child: Container(
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Color(0xFF141420),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Color(0xFF2A2A3A)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.public, color: Color(0xFF00D4FF)),
                          SizedBox(width: 12),
                          Text(
                            _selectedServer,
                            style: TextStyle(color: Colors.white, fontSize: 16),
                          ),
                        ],
                      ),
                      Icon(Icons.arrow_drop_down, color: Color(0xFF888888)),
                    ],
                  ),
                ),
              ),
              SizedBox(height: 20),
              GestureDetector(
                onTap: _openProxyScreen,
                child: Container(
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Color(0xFF141420),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Color(0xFF2A2A3A)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Icon(Icons.alt_route, color: Color(0xFF00D4FF)),
                          SizedBox(width: 12),
                          Text(
                            'Proxy Utility',
                            style: TextStyle(color: Colors.white, fontSize: 16),
                          ),
                        ],
                      ),
                      Icon(Icons.chevron_right, color: Color(0xFF888888)),
                    ],
                  ),
                ),
              ),
              Spacer(),
              Text(
                'NEO VPN © 2026 — Свобода в сети',
                style: TextStyle(color: Color(0xFF888888), fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ProxyScreen extends StatefulWidget {
  final int userId;

  ProxyScreen({required this.userId});

  @override
  _ProxyScreenState createState() => _ProxyScreenState();
}

class _ProxyScreenState extends State<ProxyScreen> {
  List<dynamic> _proxies = [];
  bool _loading = false;
  String _message = '';

  @override
  void initState() {
    super.initState();
    _loadProxies();
  }

  Future<void> _loadProxies() async {
    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/proxy/my?user_id=${widget.userId}'),
      );
      if (response.statusCode == 200) {
        setState(() {
          _proxies = jsonDecode(response.body) as List;
        });
      }
    } catch (e) {
      setState(() {
        _message = 'Не удалось загрузить прокси';
      });
    }
  }

  Future<void> _createProxy() async {
    setState(() {
      _loading = true;
      _message = '';
    });

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/proxy/create?user_id=${widget.userId}&server_id=1&proxy_type=socks5'),
      );
      final data = jsonDecode(response.body);
      if (response.statusCode == 200) {
        setState(() {
          _loading = false;
          _message = '✅ Прокси создан!';
        });
        _loadProxies();
      } else {
        setState(() {
          _loading = false;
          _message = data['detail'] ?? 'Ошибка создания';
        });
      }
    } catch (e) {
      setState(() {
        _loading = false;
        _message = 'Ошибка соединения';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(0xFF0A0A0F),
        title: Text('Proxy Utility', style: TextStyle(color: Colors.white)),
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Color(0xFF00D4FF)),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          children: [
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF00D4FF),
                foregroundColor: Colors.black,
                minimumSize: Size(double.infinity, 50),
              ),
              onPressed: _loading ? null : _createProxy,
              child: Text(
                _loading ? 'Создание...' : '🔀 Создать прокси',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
            if (_message.isNotEmpty)
              Padding(
                padding: EdgeInsets.only(top: 16),
                child: Text(_message, style: TextStyle(color: Color(0xFF00FF88))),
              ),
            SizedBox(height: 24),
            Expanded(
              child: _proxies.isEmpty
                  ? Center(
                      child: Text(
                        'У тебя пока нет прокси',
                        style: TextStyle(color: Color(0xFF888888)),
                      ),
                    )
                  : ListView.builder(
                      itemCount: _proxies.length,
                      itemBuilder: (context, index) {
                        final p = _proxies[index];
                        return Container(
                          margin: EdgeInsets.only(bottom: 12),
                          padding: EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Color(0xFF141420),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Color(0xFF2A2A3A)),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${p['proxy_type'].toUpperCase()} — ${p['proxy_login']}',
                                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                              ),
                              SizedBox(height: 8),
                              Text(
                                '${p['proxy_login']}:${p['proxy_password']}',
                                style: TextStyle(color: Color(0xFF00FF88), fontFamily: 'monospace'),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}