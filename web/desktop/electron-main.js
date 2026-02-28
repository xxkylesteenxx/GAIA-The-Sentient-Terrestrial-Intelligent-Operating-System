// web/desktop/electron-main.js
/**
 * GAIA Desktop Shell - Electron Main Process
 * Sacred desktop environment where technology and nature harmonize.
 * 
 * Factor 11 (Order): Deterministic window management, typed IPC
 * Factor 10 (Chaos): Asynchronous WebSocket event streams
 * Factor 12 (Balance): Graceful shutdown, resource cleanup
 * Factor 13 (Heart): Crisis mode never blocked
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const WebSocket = require('ws');

let mainWindow;
let coreWS, bridgeWS, overlayWS;

// WebSocket connections to GAIA backend
const WEBSOCKET_URLS = {
  core: 'ws://localhost:8765',
  bridge: 'ws://localhost:8766',
  overlay: 'ws://localhost:8767'
};

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    backgroundColor: '#0a0a0a', // Deep space black
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hidden', // Clean, immersive UI
    frame: false
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Development mode - open DevTools
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
    closeWebSockets();
  });
}

function setupWebSockets() {
  // Core Plane - Z Score, Crisis Detection
  coreWS = new WebSocket(WEBSOCKET_URLS.core);
  
  coreWS.on('open', () => {
    console.log('[GAIA Core] Connected');
    mainWindow.webContents.send('ws-status', { plane: 'core', status: 'connected' });
  });
  
  coreWS.on('message', (data) => {
    const message = JSON.parse(data);
    mainWindow.webContents.send('core-message', message);
    
    // Crisis protocol - immediate UI response
    if (message.type === 'crisis') {
      mainWindow.webContents.send('trigger-crisis-mode', message.data);
    }
  });
  
  coreWS.on('error', (error) => {
    console.error('[GAIA Core] Error:', error);
    mainWindow.webContents.send('ws-status', { plane: 'core', status: 'error', error: error.message });
  });

  coreWS.on('close', () => {
    console.log('[GAIA Core] Disconnected');
    mainWindow.webContents.send('ws-status', { plane: 'core', status: 'disconnected' });
  });

  // Bridge Plane - Hypothesis Testing
  bridgeWS = new WebSocket(WEBSOCKET_URLS.bridge);
  
  bridgeWS.on('open', () => {
    console.log('[GAIA Bridge] Connected');
    mainWindow.webContents.send('ws-status', { plane: 'bridge', status: 'connected' });
  });
  
  bridgeWS.on('message', (data) => {
    const message = JSON.parse(data);
    mainWindow.webContents.send('bridge-message', message);
  });

  bridgeWS.on('error', (error) => {
    console.error('[GAIA Bridge] Error:', error);
  });

  // Overlay Plane - Avatar, Meaning-Making
  overlayWS = new WebSocket(WEBSOCKET_URLS.overlay);
  
  overlayWS.on('open', () => {
    console.log('[GAIA Overlay] Connected');
    mainWindow.webContents.send('ws-status', { plane: 'overlay', status: 'connected' });
  });
  
  overlayWS.on('message', (data) => {
    const message = JSON.parse(data);
    mainWindow.webContents.send('overlay-message', message);
  });

  overlayWS.on('error', (error) => {
    console.error('[GAIA Overlay] Error:', error);
  });
}

function closeWebSockets() {
  if (coreWS) coreWS.close();
  if (bridgeWS) bridgeWS.close();
  if (overlayWS) overlayWS.close();
}

// IPC Handlers - Renderer → Backend communication
ipcMain.handle('send-user-message', async (event, message) => {
  if (overlayWS && overlayWS.readyState === WebSocket.OPEN) {
    overlayWS.send(JSON.stringify({
      type: 'user_input',
      content: message,
      timestamp: new Date().toISOString()
    }));
  }
});

ipcMain.handle('request-zscore', async () => {
  if (coreWS && coreWS.readyState === WebSocket.OPEN) {
    coreWS.send(JSON.stringify({
      type: 'request_zscore',
      timestamp: new Date().toISOString()
    }));
  }
});

ipcMain.handle('trigger-crisis-alert', async (event, data) => {
  if (coreWS && coreWS.readyState === WebSocket.OPEN) {
    coreWS.send(JSON.stringify({
      type: 'crisis_alert',
      data: data,
      timestamp: new Date().toISOString()
    }));
  }
});

ipcMain.handle('get-connection-status', async () => {
  return {
    core: coreWS ? coreWS.readyState : WebSocket.CLOSED,
    bridge: bridgeWS ? bridgeWS.readyState : WebSocket.CLOSED,
    overlay: overlayWS ? overlayWS.readyState : WebSocket.CLOSED
  };
});

// App lifecycle
app.on('ready', () => {
  createWindow();
  setupWebSockets();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
    setupWebSockets();
  }
});

app.on('will-quit', () => {
  closeWebSockets();
});
