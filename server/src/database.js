const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, '..', 'soulsync.db');
const db = new Database(dbPath);

function initializeDatabase() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      device_id TEXT UNIQUE,
      email TEXT UNIQUE,
      password TEXT NOT NULL,
      subscription_status TEXT DEFAULT 'trial',
      trial_start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
      subscription_expire_date DATETIME,
      session_token TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS memories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      content TEXT NOT NULL,
      version INTEGER DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS connections (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      socket_id TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS profiles (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      file_path TEXT NOT NULL,
      content TEXT NOT NULL,
      version INTEGER DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(user_id, file_path),
      FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories(user_id);
    CREATE INDEX IF NOT EXISTS idx_connections_user_id ON connections(user_id);
    CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
    CREATE INDEX IF NOT EXISTS idx_profiles_file_path ON profiles(file_path);
  `);
}

function getUserById(id) {
  return db.prepare('SELECT * FROM users WHERE id = ?').get(id);
}

function getUserByDeviceId(deviceId) {
  return db.prepare('SELECT * FROM users WHERE device_id = ?').get(deviceId);
}

function getUserByEmail(email) {
  return db.prepare('SELECT * FROM users WHERE email = ?').get(email);
}

function createUser(deviceId, email, password) {
  const trialExpireDate = new Date();
  trialExpireDate.setDate(trialExpireDate.getDate() + 7);
  
  const stmt = db.prepare(`
    INSERT INTO users (device_id, email, password, subscription_status, subscription_expire_date)
    VALUES (?, ?, ?, 'trial', ?)
  `);
  const result = stmt.run(deviceId, email, password, trialExpireDate.toISOString());
  return getUserById(result.lastInsertRowid);
}

function updateUserSession(userId, sessionToken) {
  const stmt = db.prepare(`
    UPDATE users SET session_token = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
  `);
  return stmt.run(sessionToken, userId);
}

function updateUserSubscription(userId, status, expireDate) {
  const stmt = db.prepare(`
    UPDATE users SET subscription_status = ?, subscription_expire_date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
  `);
  return stmt.run(status, expireDate, userId);
}

function bindEmail(userId, email, password) {
  const stmt = db.prepare(`
    UPDATE users SET email = ?, password = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
  `);
  return stmt.run(email, password, userId);
}

function getMemoryByUserId(userId) {
  return db.prepare('SELECT * FROM memories WHERE user_id = ? ORDER BY version DESC LIMIT 1').get(userId);
}

function getMemoryByUserIdAfterVersion(userId, version) {
  return db.prepare('SELECT * FROM memories WHERE user_id = ? AND version > ? ORDER BY version ASC').all(userId, version);
}

function createOrUpdateMemory(userId, content) {
  const existing = getMemoryByUserId(userId);
  const newVersion = existing ? existing.version + 1 : 1;
  
  if (existing) {
    const stmt = db.prepare(`
      UPDATE memories SET content = ?, version = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    `);
    stmt.run(content, newVersion, existing.id);
    return { ...existing, content, version: newVersion };
  } else {
    const stmt = db.prepare(`
      INSERT INTO memories (user_id, content, version) VALUES (?, ?, ?)
    `);
    const result = stmt.run(userId, content, newVersion);
    return { id: result.lastInsertRowid, user_id: userId, content, version: newVersion };
  }
}

function addConnection(userId, socketId) {
  const stmt = db.prepare('INSERT INTO connections (user_id, socket_id) VALUES (?, ?)');
  return stmt.run(userId, socketId);
}

function removeConnection(socketId) {
  const stmt = db.prepare('DELETE FROM connections WHERE socket_id = ?');
  return stmt.run(socketId);
}

function getConnectionsByUserId(userId) {
  return db.prepare('SELECT * FROM connections WHERE user_id = ?').all(userId);
}

function getProfilesByUserId(userId) {
  return db.prepare('SELECT * FROM profiles WHERE user_id = ?').all(userId);
}

function getProfileByUserIdAndPath(userId, filePath) {
  return db.prepare('SELECT * FROM profiles WHERE user_id = ? AND file_path = ?').get(userId, filePath);
}

function createOrUpdateProfile(userId, filePath, content, version) {
  const existing = getProfileByUserIdAndPath(userId, filePath);
  
  if (existing) {
    if (version !== existing.version) {
      return { conflict: true, existing };
    }
    const newVersion = existing.version + 1;
    const stmt = db.prepare(`
      UPDATE profiles SET content = ?, version = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    `);
    stmt.run(content, newVersion, existing.id);
    return { conflict: false, ...existing, content, version: newVersion };
  } else {
    const stmt = db.prepare(`
      INSERT INTO profiles (user_id, file_path, content, version) VALUES (?, ?, ?, 1)
    `);
    const result = stmt.run(userId, filePath, content);
    return { conflict: false, id: result.lastInsertRowid, user_id: userId, file_path: filePath, content, version: 1 };
  }
}

function getProfilesUpdatedAfter(userId, since) {
  if (!since || since === '0') {
    return db.prepare('SELECT * FROM profiles WHERE user_id = ? ORDER BY updated_at ASC').all(userId);
  }
  return db.prepare('SELECT * FROM profiles WHERE user_id = ? AND updated_at > ? ORDER BY updated_at ASC').all(userId, since);
}

module.exports = {
  db,
  initializeDatabase,
  getUserById,
  getUserByDeviceId,
  getUserByEmail,
  createUser,
  updateUserSession,
  updateUserSubscription,
  bindEmail,
  getMemoryByUserId,
  getMemoryByUserIdAfterVersion,
  createOrUpdateMemory,
  addConnection,
  removeConnection,
  getConnectionsByUserId,
  getProfilesByUserId,
  getProfileByUserIdAndPath,
  createOrUpdateProfile,
  getProfilesUpdatedAfter
};
