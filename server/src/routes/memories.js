const express = require('express');
const db = require('../database');
const { authMiddleware } = require('../middleware/auth');
const { subscriptionMiddleware } = require('../middleware/subscription');
const { getSubscriptionInfo } = require('../middleware/subscription');

const router = express.Router();

let websocketServer = null;

function setWebSocketServer(wsServer) {
  websocketServer = wsServer;
}

function broadcastToUser(userId, event, data) {
  if (!websocketServer) return;
  
  const connections = db.getConnectionsByUserId(userId);
  connections.forEach(conn => {
    websocketServer.clients.forEach(client => {
      if (client.socketId === conn.socket_id && client.readyState === 1) {
        client.send(JSON.stringify({ event, data }));
      }
    });
  });
}

router.get('/', authMiddleware, (req, res) => {
  try {
    const memory = db.getMemoryByUserId(req.user.id);
    
    if (!memory) {
      return res.json({ content: '', version: 0 });
    }
    
    res.json({
      content: memory.content,
      version: memory.version,
      updated_at: memory.updated_at
    });
  } catch (error) {
    console.error('Get memories error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/', authMiddleware, subscriptionMiddleware, (req, res) => {
  try {
    const { content } = req.body;
    
    if (content === undefined) {
      return res.status(400).json({ error: 'content is required' });
    }
    
    const memory = db.createOrUpdateMemory(req.user.id, content);
    
    broadcastToUser(req.user.id, 'new_memory', {
      version: memory.version,
      updated_at: memory.updated_at
    });
    
    res.json({
      id: memory.id,
      version: memory.version,
      content: memory.content,
      updated_at: memory.updated_at
    });
  } catch (error) {
    console.error('Create/update memory error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/sync', authMiddleware, subscriptionMiddleware, (req, res) => {
  try {
    const version = parseInt(req.query.version) || 0;
    
    const memories = db.getMemoryByUserIdAfterVersion(req.user.id, version);
    
    res.json({
      version,
      updates: memories.map(m => ({
        content: m.content,
        version: m.version,
        updated_at: m.updated_at
      }))
    });
  } catch (error) {
    console.error('Sync error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/profile', authMiddleware, (req, res) => {
  try {
    const memory = db.getMemoryByUserId(req.user.id);
    const subscriptionInfo = getSubscriptionInfo(req.user);
    
    res.json({
      user_id: req.user.id,
      device_id: req.user.device_id,
      email: req.user.email,
      subscription: subscriptionInfo,
      memory: memory ? {
        version: memory.version,
        updated_at: memory.updated_at
      } : null
    });
  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/bind-email', authMiddleware, (req, res) => {
  try {
    const { email, password } = req.body;
    
    if (!email || !password) {
      return res.status(400).json({ error: 'email and password are required' });
    }
    
    if (req.user.email && req.user.email !== email) {
      return res.status(409).json({ error: 'Email already bound' });
    }
    
    const existingUser = db.getUserByEmail(email);
    if (existingUser && existingUser.id !== req.user.id) {
      return res.status(409).json({ error: 'Email already in use' });
    }
    
    db.bindEmail(req.user.id, email, password);
    
    const updatedUser = db.getUserById(req.user.id);
    
    res.json({
      user_id: updatedUser.id,
      device_id: updatedUser.device_id,
      email: updatedUser.email,
      subscription_status: updatedUser.subscription_status
    });
  } catch (error) {
    console.error('Bind email error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
module.exports.setWebSocketServer = setWebSocketServer;
