const express = require('express');
const db = require('../database');
const { authMiddleware } = require('../middleware/auth');
const { subscriptionMiddleware } = require('../middleware/subscription');

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
    const { path } = req.query;
    
    if (path) {
      const profile = db.getProfileByUserIdAndPath(req.user.id, path);
      if (!profile) {
        return res.status(404).json({ error: 'File not found' });
      }
      return res.json({
        files: [{
          file_path: profile.file_path,
          content: profile.content,
          version: profile.version,
          updated_at: profile.updated_at
        }]
      });
    }
    
    const profiles = db.getProfilesByUserId(req.user.id);
    res.json({
      files: profiles.map(p => ({
        file_path: p.file_path,
        content: p.content,
        version: p.version,
        updated_at: p.updated_at
      }))
    });
  } catch (error) {
    console.error('Get profiles error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/', authMiddleware, subscriptionMiddleware, (req, res) => {
  try {
    const { file_path, content, version } = req.body;
    
    if (!file_path || content === undefined) {
      return res.status(400).json({ error: 'file_path and content are required' });
    }
    
    const result = db.createOrUpdateProfile(req.user.id, file_path, content, version || 0);
    
    if (result.conflict) {
      return res.status(409).json({
        error: 'Version conflict',
        code: 'VERSION_CONFLICT',
        latest_content: result.existing.content,
        latest_version: result.existing.version
      });
    }
    
    broadcastToUser(req.user.id, 'file_updated', {
      file_path: result.file_path,
      version: result.version
    });
    
    res.json({
      file_path: result.file_path,
      version: result.version,
      updated_at: result.updated_at
    });
  } catch (error) {
    console.error('Create/update profile error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/sync', authMiddleware, subscriptionMiddleware, (req, res) => {
  try {
    const { since } = req.query;
    
    const profiles = db.getProfilesUpdatedAfter(req.user.id, since || '0');
    
    res.json({
      files: profiles.map(p => ({
        file_path: p.file_path,
        content: p.content,
        version: p.version,
        updated_at: p.updated_at
      })),
      server_time: new Date().toISOString()
    });
  } catch (error) {
    console.error('Sync profiles error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
module.exports.setWebSocketServer = setWebSocketServer;
