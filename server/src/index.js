const express = require('express');
const http = require('http');
const cors = require('cors');
const path = require('path');

const db = require('./database');
const authMiddleware = require('./middleware/auth');
const authRoutes = require('./routes/auth');
const memoriesRoutes = require('./routes/memories');
const profilesRoutes = require('./routes/profiles');
const { initializeWebSocket, getWebSocketServer } = require('./websocket');

const app = express();
const server = http.createServer(app);

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '0.0.0.0';

app.use(cors());
app.use(express.json({ limit: '10mb' }));

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.use('/api/auth', authRoutes);
app.use('/api/memories', memoriesRoutes);
app.use('/api/profiles', profilesRoutes);

initializeWebSocket(server);

server.on('upgrade', (request, socket, head) => {
  const wss = getWebSocketServer();
  if (wss) {
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit('connection', ws, request);
    });
  } else {
    socket.destroy();
  }
});

db.initializeDatabase();
console.log('Database initialized');

server.listen(PORT, HOST, () => {
  console.log(`SoulSync server running on http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}`);
  console.log(`WebSocket server running on ws://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}`);
});

module.exports = { app, server };
