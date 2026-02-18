const WebSocket = require('ws');
const db = require('./database');

let wss = null;

function initializeWebSocket(server) {
  wss = new WebSocket.Server({ noServer: true });
  
  wss.on('connection', (ws, req) => {
    console.log('WebSocket client connected');
    ws.authenticated = false;
    ws.userId = null;
    ws.socketId = null;
    
    ws.on('message', (message) => {
      try {
        const data = JSON.parse(message);
        
        if (data.type === 'auth') {
          handleAuth(ws, data.token);
        } else if (data.type === 'ping') {
          ws.send(JSON.stringify({ type: 'pong' }));
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    });
    
    ws.on('close', () => {
      if (ws.socketId) {
        db.removeConnection(ws.socketId);
        console.log(`WebSocket client disconnected: ${ws.socketId}`);
      }
    });
    
    ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  });
  
  return wss;
}

function handleAuth(ws, token) {
  try {
    const parts = token.split(':');
    if (parts.length !== 2) {
      ws.send(JSON.stringify({ type: 'error', message: 'Invalid token format' }));
      return;
    }
    
    const userId = parseInt(parts[0]);
    const sessionToken = parts[1];
    
    const user = db.getUserById(userId);
    if (!user || user.session_token !== sessionToken) {
      ws.send(JSON.stringify({ type: 'error', message: 'Invalid token' }));
      return;
    }
    
    ws.authenticated = true;
    ws.userId = userId;
    ws.socketId = `ws_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    db.addConnection(userId, ws.socketId);
    
    ws.send(JSON.stringify({ 
      type: 'authenticated', 
      user_id: userId,
      socket_id: ws.socketId
    }));
    
    console.log(`WebSocket client authenticated: user=${userId}, socket=${ws.socketId}`);
  } catch (error) {
    console.error('WebSocket auth error:', error);
    ws.send(JSON.stringify({ type: 'error', message: 'Authentication failed' }));
  }
}

function broadcastToUser(userId, event, data) {
  if (!wss) return;
  
  const connections = db.getConnectionsByUserId(userId);
  
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN && client.authenticated && client.userId === userId) {
      client.send(JSON.stringify({ event, data }));
    }
  });
}

function getWebSocketServer() {
  return wss;
}

module.exports = {
  initializeWebSocket,
  broadcastToUser,
  getWebSocketServer
};
