const express = require('express');
const { v4: uuidv4 } = require('uuid');
const db = require('../database');

const router = express.Router();

router.post('/register', (req, res) => {
  try {
    const { device_id, email, password } = req.body;
    
    if (!device_id || !email || !password) {
      return res.status(400).json({ error: 'device_id, email, and password are required' });
    }
    
    const existingByDevice = db.getUserByDeviceId(device_id);
    if (existingByDevice) {
      return res.status(409).json({ error: 'Device already registered' });
    }
    
    const existingByEmail = db.getUserByEmail(email);
    if (existingByEmail) {
      return res.status(409).json({ error: 'Email already registered' });
    }
    
    const user = db.createUser(device_id, email, password);
    const sessionToken = uuidv4();
    db.updateUserSession(user.id, sessionToken);
    
    res.status(201).json({
      user_id: user.id,
      device_id: user.device_id,
      email: user.email,
      subscription_status: user.subscription_status,
      token: `${user.id}:${sessionToken}`
    });
  } catch (error) {
    console.error('Register error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/login', (req, res) => {
  try {
    const { email, password } = req.body;
    
    if (!email || !password) {
      return res.status(400).json({ error: 'email and password are required' });
    }
    
    const user = db.getUserByEmail(email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    if (user.password !== password) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const sessionToken = uuidv4();
    db.updateUserSession(user.id, sessionToken);
    
    res.json({
      user_id: user.id,
      device_id: user.device_id,
      email: user.email,
      subscription_status: user.subscription_status,
      token: `${user.id}:${sessionToken}`
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/device', (req, res) => {
  try {
    const { device_id, email, password } = req.body;
    
    if (!device_id) {
      return res.status(400).json({ error: 'device_id is required' });
    }
    
    let user = db.getUserByDeviceId(device_id);
    
    if (user) {
      if (email && password) {
        if (user.email && user.email !== email) {
          return res.status(409).json({ error: 'Device already bound to different email' });
        }
        db.bindEmail(user.id, email, password);
        user = db.getUserById(user.id);
      }
      
      if (user.password !== (password || '')) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      const sessionToken = uuidv4();
      db.updateUserSession(user.id, sessionToken);
      
      res.json({
        user_id: user.id,
        device_id: user.device_id,
        email: user.email,
        subscription_status: user.subscription_status,
        token: `${user.id}:${sessionToken}`
      });
    } else {
      if (!email || !password) {
        return res.status(400).json({ error: 'New device requires email and password' });
      }
      
      const existingByEmail = db.getUserByEmail(email);
      if (existingByEmail) {
        return res.status(409).json({ error: 'Email already registered, please login with existing account' });
      }
      
      user = db.createUser(device_id, email, password);
      const sessionToken = uuidv4();
      db.updateUserSession(user.id, sessionToken);
      
      res.status(201).json({
        user_id: user.id,
        device_id: user.device_id,
        email: user.email,
        subscription_status: user.subscription_status,
        token: `${user.id}:${sessionToken}`
      });
    }
  } catch (error) {
    console.error('Device auth error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
