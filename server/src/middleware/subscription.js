const db = require('../database');

function subscriptionMiddleware(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  const { subscription_status, subscription_expire_date } = req.user;
  const now = new Date();
  
  if (subscription_status === 'expired') {
    return res.status(403).json({ 
      error: 'Subscription expired',
      code: 'SUBSCRIPTION_EXPIRED'
    });
  }
  
  if (subscription_status === 'trial') {
    if (!subscription_expire_date) {
      return res.status(403).json({ 
        error: 'Trial expired',
        code: 'TRIAL_EXPIRED'
      });
    }
    
    const expireDate = new Date(subscription_expire_date);
    if (now > expireDate) {
      db.updateUserSubscription(req.user.id, 'expired', null);
      return res.status(403).json({ 
        error: 'Trial expired',
        code: 'TRIAL_EXPIRED'
      });
    }
  }
  
  if (subscription_status === 'active') {
    if (subscription_expire_date) {
      const expireDate = new Date(subscription_expire_date);
      if (now > expireDate) {
        db.updateUserSubscription(req.user.id, 'expired', null);
        return res.status(403).json({ 
          error: 'Subscription expired',
          code: 'SUBSCRIPTION_EXPIRED'
        });
      }
    }
  }
  
  next();
}

function getSubscriptionInfo(user) {
  const now = new Date();
  let status = user.subscription_status;
  let daysRemaining = 0;
  let isActive = false;
  
  if (status === 'trial' && user.subscription_expire_date) {
    const expireDate = new Date(user.subscription_expire_date);
    if (now <= expireDate) {
      daysRemaining = Math.ceil((expireDate - now) / (1000 * 60 * 60 * 24));
      isActive = true;
    } else {
      status = 'expired';
    }
  } else if (status === 'active' && user.subscription_expire_date) {
    const expireDate = new Date(user.subscription_expire_date);
    if (now <= expireDate) {
      daysRemaining = Math.ceil((expireDate - now) / (1000 * 60 * 60 * 24));
      isActive = true;
    } else {
      status = 'expired';
    }
  }
  
  return {
    status,
    daysRemaining,
    isActive,
    expireDate: user.subscription_expire_date
  };
}

module.exports = {
  subscriptionMiddleware,
  getSubscriptionInfo
};
