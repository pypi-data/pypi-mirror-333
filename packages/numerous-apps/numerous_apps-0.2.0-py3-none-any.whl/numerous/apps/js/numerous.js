const USE_SHADOW_DOM = false;  // Set to true to enable Shadow DOM
const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
    NONE: 4
};
let currentLogLevel = LOG_LEVELS.ERROR; // Default log level

// Add this logging utility function
function log(level, ...args) {
    if (level >= currentLogLevel) {
        switch (level) {
            case LOG_LEVELS.DEBUG:
                console.log(...args);
                break;
            case LOG_LEVELS.INFO:
                console.info(...args);
                break;
            case LOG_LEVELS.WARN:
                console.warn(...args);
                break;
            case LOG_LEVELS.ERROR:
                console.error(...args);
                break;
        }
    }
}

// Add MessageType enum at the top of the file
const MessageType = {
    WIDGET_UPDATE: 'widget-update',
    GET_STATE: 'get-state',
    GET_WIDGET_STATES: 'get-widget-states',
    ACTION_REQUEST: 'action-request',
    ACTION_RESPONSE: 'action-response',
    ERROR: 'error',
    INIT_CONFIG: 'init-config',
    SESSION_ERROR: 'session-error'
};

// Create a Model class instead of a single model object
class WidgetModel {
    constructor(widgetId) {
        this.widgetId = widgetId;
        this.data = {};
        this._callbacks = {};
        this._initializing = true; // Flag to indicate initial setup
        this._pendingChanges = new Map(); // Store changes that happen during initialization
        log(LOG_LEVELS.DEBUG, `[WidgetModel] Created for widget ${widgetId}`);
    }
    
    set(key, value, suppressSync = false) {
        log(LOG_LEVELS.DEBUG, `[WidgetModel] Setting ${key}=${value} for widget ${this.widgetId}`);
        const oldValue = this.data[key];
        
        // Only trigger if value actually changed
        const valueChanged = oldValue !== value;
        
        this.data[key] = value;

        if (valueChanged) {
            this.trigger('change:' + key, value);
        }
        
        // Sync with server if not suppressed
        if (!suppressSync && !this._suppressSync) {
            log(LOG_LEVELS.DEBUG, `[WidgetModel] Sending update to server`);
            wsManager.sendUpdate(this.widgetId, key, value);
        } else if (this._initializing && !suppressSync) {
            // If we're initializing and change isn't suppressed, store for later sync
            log(LOG_LEVELS.DEBUG, `[WidgetModel] Queuing change for later: ${key}=${value}`);
            this._pendingChanges.set(key, value);
        }
    }
    
    // Mark initialization complete and send any pending changes
    completeInitialization() {
        if (!this._initializing) return;
        
        log(LOG_LEVELS.DEBUG, `[WidgetModel ${this.widgetId}] Completing initialization, processing ${this._pendingChanges.size} pending changes`);
        this._initializing = false;
        
        // Send any pending changes
        for (const [key, value] of this._pendingChanges.entries()) {
            wsManager.sendUpdate(this.widgetId, key, value);
        }
        
        this._pendingChanges.clear();
    }
    
    get(key) {
        return this.data[key];
    }
    
    save_changes() {
        log(LOG_LEVELS.DEBUG, `[WidgetModel ${this.widgetId}] Saving changes`);
        
        // If we're still initializing, mark initialization as complete
        if (this._initializing) {
            this.completeInitialization();
        } else {
            // Otherwise, send all current values to server
            for (const [key, value] of Object.entries(this.data)) {
                wsManager.sendUpdate(this.widgetId, key, value);
            }
        }
    }

    on(eventName, callback) {
        if (!this._callbacks[eventName]) {
            this._callbacks[eventName] = [];
        }
        this._callbacks[eventName].push(callback);
    }

    off(eventName, callback) {
        if (!eventName) {
            this._callbacks = {};
            return;
        }
        if (this._callbacks[eventName]) {
            if (!callback) {
                delete this._callbacks[eventName];
            } else {
                this._callbacks[eventName] = this._callbacks[eventName].filter(cb => cb !== callback);
            }
        }
    }

    trigger(eventName, data) {
        log(LOG_LEVELS.DEBUG, `[WidgetModel ${this.widgetId}] Triggering ${eventName} with data:`, data);
        if (this._callbacks[eventName]) {
            log(LOG_LEVELS.DEBUG, `[WidgetModel ${this.widgetId}] Found ${this._callbacks[eventName].length} callbacks for ${eventName}`);
            this._callbacks[eventName].forEach(callback => callback(data));
        } else {
            log(LOG_LEVELS.DEBUG, `[WidgetModel ${this.widgetId}] No callbacks found for ${eventName}`);
        }
    }

    send(content, callbacks, buffers) {
        log(LOG_LEVELS.DEBUG, `[WidgetModel ${this.widgetId}] Sending message:`, content);
        // Implement message sending if needed
    }
}

// Create a function to dynamically load ESM modules
async function loadWidget(moduleSource) {
    try {
        // Check if the source is a URL or a JavaScript string
        if (moduleSource.startsWith('http') || moduleSource.startsWith('./') || moduleSource.startsWith('/')) {
            return await import(moduleSource);
        } else {
            // Create a Blob with the JavaScript code
            const blob = new Blob([moduleSource], { type: 'text/javascript' });
            const blobUrl = URL.createObjectURL(blob);
            
            // Import the blob URL and then clean it up
            const module = await import(blobUrl);
            URL.revokeObjectURL(blobUrl);
            
            return module;
        }
    } catch (error) {
        log(LOG_LEVELS.ERROR, `Failed to load widget from ${moduleSource.substring(0, 100)}...:`, error);
        return null;
    }
}
var wsManager;
// Function to fetch widget configurations and states from the server
async function fetchWidgetConfigs() {
    try {
        console.log("Fetching widget configs and states");

        let sessionId = sessionStorage.getItem('session_id');
        const response = await fetch(`/api/widgets?session_id=${sessionId}`);
        const data = await response.json();

        sessionStorage.setItem('session_id', data.session_id);
        sessionId = data.session_id;

        wsManager = new WebSocketManager(sessionId);
        
        // Set log level if provided in the response
        if (data.logLevel !== undefined) {
            currentLogLevel = LOG_LEVELS[data.logLevel] ?? LOG_LEVELS.INFO;
            log(LOG_LEVELS.INFO, `Log level set to: ${data.logLevel}`);
        }
        
        return data.widgets; 
    } catch (error) {
        log(LOG_LEVELS.ERROR, 'Failed to fetch widget configs:', error);
        return {};
    }
}

// Add these near the top with other state variables
let renderedWidgets = 0;
let totalWidgets = 0;
let statesReceived = false;

// Add this function to handle manual dismissal
function dismissLoadingOverlay() {
    const splashScreen = document.getElementById('splash-screen');
    if (splashScreen) {
        splashScreen.classList.add('hidden');
        // Remove from DOM after transition
        setTimeout(() => {
            splashScreen.remove();
        }, 300);
    }
}

// Modify checkAllWidgetsReady to add a minimum display time
let loadingStartTime = Date.now();
const MIN_LOADING_TIME = 1000; // Minimum time to show loading overlay (1 second)

// Modify the initializeWidgets function
async function initializeWidgets() {
    console.log("Initializing widgets");
    loadingStartTime = Date.now();
    const widgetConfigs = await fetchWidgetConfigs();
    
    // Reset tracking variables
    totalWidgets = Object.keys(widgetConfigs).length;
    renderedWidgets = 0;
    statesReceived = false;
    
    // Wait for WebSocket connection to be established before initializing widgets
    await wsManager.connectionReady();
    log(LOG_LEVELS.INFO, "WebSocket connection ready, initializing widgets");
    
    const widgetModels = new Map();
    
    // First phase: Create all models and set default values
    for (const [widgetId, config] of Object.entries(widgetConfigs)) {
        // Create a new model instance for this widget
        const widgetModel = new WidgetModel(widgetId);
        
        // Store in our local map and the WebSocket manager
        widgetModels.set(widgetId, widgetModel);
        wsManager.widgetModels.set(widgetId, widgetModel);
        
        // Initialize default values for this widget
        for (const [key, value] of Object.entries(config.defaults || {})) {
            if (!widgetModel.get(key)) {    
                log(LOG_LEVELS.DEBUG, `[WidgetModel ${widgetId}] Setting default value for ${key}=${value}`);
                widgetModel.set(key, value, true); // Suppress sync during initialization
            }
        }
    }
    
    // Second phase: Render all widgets
    for (const [widgetId, config] of Object.entries(widgetConfigs)) {
        const container = document.getElementById(widgetId);
        if (!container) {
            log(LOG_LEVELS.WARN, `Element with id ${widgetId} not found`);
            renderedWidgets++; // Count failed widgets to maintain accurate tracking
            continue;
        }

        let element;
        const isPlotlyWidget = config.moduleUrl?.toLowerCase().includes('plotly');
        
        if (USE_SHADOW_DOM && !isPlotlyWidget) {
            // Use Shadow DOM for non-Plotly widgets
            const shadowRoot = container.attachShadow({ mode: 'open' });
            
            if (config.css) {
                const styleElement = document.createElement('style');
                styleElement.textContent = config.css;
                shadowRoot.appendChild(styleElement);
            }
            
            element = document.createElement('div');
            element.id = widgetId;
            element.classList.add('widget-wrapper');
            shadowRoot.appendChild(element);
        } else {
            // Use regular DOM for Plotly widgets or when Shadow DOM is disabled
            element = container;
            if (config.css) {
                const styleElement = document.createElement('style');
                styleElement.textContent = config.css;
                document.head.appendChild(styleElement);
            }
        }

        const widgetModel = widgetModels.get(widgetId);
        const widgetModule = await loadWidget(config.moduleUrl);
        
        if (widgetModule && widgetModel) {
            try {
                // Render the widget with its model
                await widgetModule.default.render({
                    model: widgetModel,
                    el: element
                });
                
                log(LOG_LEVELS.DEBUG, `Widget ${widgetId} rendered successfully`);
            } catch (error) {
                log(LOG_LEVELS.ERROR, `Failed to render widget ${widgetId}:`, error);
            }
        }
    }
    
    // Third phase: Complete initialization for all models to send pending changes
    log(LOG_LEVELS.INFO, "All widgets rendered, completing initialization");
    for (const widgetModel of widgetModels.values()) {
        widgetModel.completeInitialization();
    }

    dismissLoadingOverlay();
}

// Initialize widgets when the document is loaded
document.addEventListener('DOMContentLoaded', initializeWidgets); 

// Add WebSocket connection management
class WebSocketManager {
    constructor(sessionId) {
        this.clientId = Math.random().toString(36).substr(2, 9);
        this.sessionId = sessionId;
        this.widgetModels = new Map();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.messageQueue = [];
        
        // Create a promise to track connection state
        this.connectionPromise = new Promise((resolve) => {
            this.resolveConnection = resolve;
        });
        
        log(LOG_LEVELS.INFO, `[WebSocketManager] Created with clientId ${this.clientId} and sessionId ${this.sessionId}`);
        this.connect();
    }

    showErrorModal(message) {
        const modal = document.getElementById('error-modal');
        const messageElement = document.getElementById('error-modal-message');
        messageElement.textContent = message;
        modal.style.display = 'block';
    }

    showSessionLostBanner() {
        const banner = document.getElementById('session-lost-banner');
        log(LOG_LEVELS.DEBUG, `[WebSocketManager] Banner element exists: ${!!banner}`);
        if (banner) {
            banner.classList.remove('hidden');
            log(LOG_LEVELS.DEBUG, `[WebSocketManager] Banner classes after show: ${banner.className}`);
        } else {
            log(LOG_LEVELS.ERROR, `[WebSocketManager] Session lost banner element not found in DOM`);
        }
    }

    connect() {
        log(LOG_LEVELS.DEBUG, `[WebSocketManager ${this.clientId}] Connecting to WebSocket...`);
        const isSecure = window.location.protocol === 'https:';
        const wsProtocol = isSecure ? 'wss:' : 'ws:';
        this.ws = new WebSocket(`${wsProtocol}//${window.location.host}/ws/${this.clientId}/${this.sessionId}`);
        
        this.ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                log(LOG_LEVELS.DEBUG, `[WebSocketManager ${this.clientId}] Received message:`, message);
                
                // Handle all message types
                switch (message.type) {
                    case MessageType.SESSION_ERROR:
                        log(LOG_LEVELS.INFO, `[WebSocketManager ${this.clientId}] Session error received`);
                        this.showSessionLostBanner();
                        
                        // Don't attempt to reconnect on session errors
                        this.reconnectAttempts = this.maxReconnectAttempts;
                        
                        // Hide the connection status overlay since this is a session error
                        const connectionStatus = document.getElementById('connection-status');
                        if (connectionStatus) {
                            connectionStatus.classList.add('hidden');
                        }
                        break;

                    case 'widget-update':
                        // Handle widget updates from both actions and direct changes
                        const model = this.widgetModels.get(message.widget_id);
                        if (model) {
                            log(LOG_LEVELS.DEBUG, `[WebSocketManager ${this.clientId}] Updating widget ${message.widget_id}: ${message.property} = ${message.value}`);
                            // Update the model without triggering a send back to server
                            model.set(message.property, message.value, true);
                            
                            // Also trigger a general update event that widgets can listen to
                            model.trigger('update', {
                                property: message.property,
                                value: message.value
                            });
                        }
                        break;

                    case 'error':
                        log(LOG_LEVELS.ERROR, `[WebSocketManager ${this.clientId}] Error from backend:`, message);
                        this.showErrorModal(message.error || 'Unknown error occurred');
                        break;

                    default:
                        log(LOG_LEVELS.DEBUG, `[WebSocketManager ${this.clientId}] Unhandled message type: ${message.type}`);
                }
            } catch (error) {
                log(LOG_LEVELS.ERROR, `[WebSocketManager ${this.clientId}] Error processing message:`, error);
            }
        };

        this.ws.onopen = () => {
            log(LOG_LEVELS.INFO, `[WebSocketManager] WebSocket connection established`);
            this.hideConnectionStatus();
            
            // Request all widget states after connection
            this.ws.send(JSON.stringify({
                type: 'get-widget-states',
                client_id: this.clientId
            }));
            
            // Process any queued messages
            this.flushMessageQueue();
            
            // Resolve the connection promise to indicate the connection is ready
            this.resolveConnection();
        };

        this.ws.onclose = (event) => {
            log(LOG_LEVELS.INFO, `[WebSocketManager ${this.clientId}] WebSocket connection closed`);
            
            // Only show connection status if it's not a session error
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.showConnectionStatus();
                this.reconnectAttempts++;
                setTimeout(() => this.connect(), this.reconnectDelay);
                this.reconnectDelay *= 2;
            }
        };

        this.ws.onerror = (error) => {
            log(LOG_LEVELS.ERROR, `[WebSocketManager ${this.clientId}] WebSocket error:`, error);
            // Only show connection status for non-session errors
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.showConnectionStatus();
            }
        };
    }

    // Method to wait for connection to be established
    async connectionReady() {
        return this.connectionPromise;
    }
    
    // Send all queued messages once connection is established
    flushMessageQueue() {
        if (this.messageQueue.length === 0) return;
        
        log(LOG_LEVELS.DEBUG, `[WebSocketManager] Sending ${this.messageQueue.length} queued messages`);
        
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.ws.send(JSON.stringify(message));
        }
    }

    sendUpdate(widgetId, property, value) {
        const message = {
            type: "widget-update",
            widget_id: widgetId,
            property: property,
            value: value
        };
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            log(LOG_LEVELS.DEBUG, `[WebSocketManager] Sending update:`, message);
            this.ws.send(JSON.stringify(message));
        } else {
            log(LOG_LEVELS.DEBUG, `[WebSocketManager] Queuing update message for later:`, message);
            this.messageQueue.push(message);
        }
    }

    showConnectionStatus() {
        const statusOverlay = document.getElementById('connection-status');
        if (statusOverlay) {
            statusOverlay.classList.remove('hidden');
        }
    }

    hideConnectionStatus() {
        const statusOverlay = document.getElementById('connection-status');
        if (statusOverlay) {
            statusOverlay.classList.add('hidden');
        }
    }

    updateConnectionStatus(message) {
        const statusOverlay = document.getElementById('connection-status');
        if (statusOverlay) {
            const messageElement = statusOverlay.querySelector('.loading-content div:last-child');
            if (messageElement) {
                messageElement.textContent = message;
            }
        }
    }
}

