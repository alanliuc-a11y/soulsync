const db = require('../database');

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }
  
  const token = authHeader.substring(7);
  const parts = token.split(':');
  
  if (parts.length !== 2) {
    return res.status(401).json({ error: 'Invalid token format' });
  }
  
  const userId = parseInt(parts[0]);
  const sessionToken = parts[1];
  
  const user = db.getUserById(userId);
  
  if (!user) {
    return res.status(401).json({ error: 'User not found' });
  }
  
  if (user.session_token !== sessionToken) {
    return res.status(401).json({ error: 'Invalid session token' });
  }
  
  req.user = user;
  next();
}

function optionalAuthMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return next();
  }
  
  const token = authHeader.substring(7);
  const parts = token.split(':');
  
  if (parts.length !== 2) {
    return next();
  }
  
  const userId = parseInt(parts[0]);
  const sessionToken = parts[1];
  
  const user = db.getUserById(userId);
  
  if (user && user.session_token === sessionToken) {
    req.user = user;
  }
  
  next();
}

module.exports = {
  authMiddleware,
  optionalAuthMiddleware
};
