// web/desktop/preload.js
/**
 * GAIA Desktop Preload Script
 * Secure bridge between renderer and main process.
 * 
 * Factor 11 (Order): Typed API contract, explicit permissions
 * Factor 13 (Heart): Crisis functions always exposed
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose GAIA API to renderer process
contextBridge.exposeInMainWorld('gaiaAPI', {
  // User Communication
  sendMessage: (message) => ipcRenderer.invoke('send-user-message', message),
  
  // Z Score Queries
  requestZScore: () => ipcRenderer.invoke('request-zscore'),
  
  // Crisis Protocol - Factor 13
  triggerCrisisAlert: (data) => ipcRenderer.invoke('trigger-crisis-alert', data),
  
  // Connection Status
  getConnectionStatus: () => ipcRenderer.invoke('get-connection-status'),
  
  // Event Listeners - WebSocket messages from backend
  onCoreMessage: (callback) => {
    ipcRenderer.on('core-message', (event, data) => callback(data));
  },
  
  onBridgeMessage: (callback) => {
    ipcRenderer.on('bridge-message', (event, data) => callback(data));
  },
  
  onOverlayMessage: (callback) => {
    ipcRenderer.on('overlay-message', (event, data) => callback(data));
  },
  
  onWebSocketStatus: (callback) => {
    ipcRenderer.on('ws-status', (event, data) => callback(data));
  },
  
  onCrisisMode: (callback) => {
    ipcRenderer.on('trigger-crisis-mode', (event, data) => callback(data));
  },
  
  // Remove listeners (cleanup)
  removeListener: (channel, callback) => {
    ipcRenderer.removeListener(channel, callback);
  }
});

console.log('[GAIA Preload] API bridge established');
