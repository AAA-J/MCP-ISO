"""Tools for building Discord Activities."""

from mcp.types import Tool, TextContent
import json

activities_tools = [
    Tool(
        name="discord_generate_activity_starter",
        description="Generate starter code for a Discord Activity",
        inputSchema={
            "type": "object",
            "properties": {
                "activityName": {
                    "type": "string",
                    "description": "Name of the activity"
                },
                "hasMultiplayer": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether the activity supports multiplayer"
                },
                "framework": {
                    "type": "string",
                    "enum": ["react", "vanilla", "phaser"],
                    "default": "react"
                },
                "activityType": {
                    "type": "string",
                    "enum": ["embedded", "iframe"],
                    "default": "embedded"
                }
            },
            "required": ["activityName"]
        }
    ),
    Tool(
        name="discord_generate_activity_layout",
        description="Generate layout code for Discord Activity UI",
        inputSchema={
            "type": "object",
            "properties": {
                "layoutType": {
                    "type": "string",
                    "enum": ["single-player", "multiplayer", "spectator"],
                    "description": "Type of layout"
                },
                "framework": {
                    "type": "string",
                    "enum": ["react", "vanilla"]
                }
            },
            "required": ["layoutType", "framework"]
        }
    ),
    Tool(
        name="discord_generate_networking",
        description="Generate multiplayer networking code for Activities",
        inputSchema={
            "type": "object",
            "properties": {
                "framework": {
                    "type": "string",
                    "enum": ["react", "vanilla", "phaser"]
                },
                "transportType": {
                    "type": "string",
                    "enum": ["websocket", "webrtc", "discord-rpc"],
                    "default": "websocket"
                }
            },
            "required": ["framework"]
        }
    ),
    Tool(
        name="discord_validate_activity_metadata",
        description="Validate activity metadata against Discord requirements",
        inputSchema={
            "type": "object",
            "properties": {
                "metadata": {
                    "type": "object",
                    "description": "Activity metadata object"
                }
            },
            "required": ["metadata"]
        }
    ),
]

async def handle_activities(name: str, arguments: dict) -> list[TextContent]:
    """Handle Discord Activities tool calls."""
    if name == "discord_generate_activity_starter":
        activity_name = arguments.get("activityName")
        has_multiplayer = arguments.get("hasMultiplayer", False)
        framework = arguments.get("framework", "react")
        activity_type = arguments.get("activityType", "embedded")
        
        result = {
            "success": True,
            "activityName": activity_name,
            "multiplayer": has_multiplayer,
            "framework": framework,
            "activityType": activity_type,
            "files": generate_activity_files(activity_name, has_multiplayer, framework, activity_type)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_generate_activity_layout":
        layout_type = arguments.get("layoutType")
        framework = arguments.get("framework")
        code = generate_activity_layout_code(layout_type, framework)
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_networking":
        framework = arguments.get("framework")
        transport = arguments.get("transportType", "websocket")
        code = generate_networking_code(framework, transport)
        return [TextContent(type="text", text=code)]
    elif name == "discord_validate_activity_metadata":
        metadata = arguments.get("metadata")
        result = validate_activity_metadata(metadata)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown Discord Activities tool: {name}")

def generate_activity_files(activity_name: str, has_multiplayer: bool, framework: str, activity_type: str) -> dict:
    """Generate Activity file structure with complete code."""
    files = {}
    
    if framework == "react":
        files["src/App.tsx"] = generate_react_activity_app(activity_name, has_multiplayer, activity_type)
        files["src/index.tsx"] = generate_react_index()
        files["package.json"] = generate_react_package_json(activity_name, has_multiplayer)
        files["tsconfig.json"] = generate_tsconfig()
        files["public/index.html"] = generate_activity_html(activity_name)
        files["README.md"] = generate_activity_readme(activity_name, framework, has_multiplayer)
        
        if has_multiplayer:
            files["src/hooks/useMultiplayer.ts"] = generate_multiplayer_hook()
            files["src/components/PlayerList.tsx"] = generate_player_list_component()
    
    elif framework == "vanilla":
        files["src/index.html"] = generate_vanilla_html(activity_name, has_multiplayer)
        files["src/index.js"] = generate_vanilla_js(activity_name, has_multiplayer, activity_type)
        files["src/styles.css"] = generate_vanilla_css()
        files["package.json"] = generate_vanilla_package_json(activity_name)
        files["README.md"] = generate_activity_readme(activity_name, framework, has_multiplayer)
    
    elif framework == "phaser":
        files["src/index.js"] = generate_phaser_game(activity_name, has_multiplayer)
        files["src/scenes/GameScene.js"] = generate_phaser_scene(has_multiplayer)
        files["index.html"] = generate_phaser_html(activity_name)
        files["package.json"] = generate_phaser_package_json(activity_name)
        files["README.md"] = generate_activity_readme(activity_name, framework, has_multiplayer)
    
    # Activity manifest
    files["activity.json"] = generate_activity_manifest(activity_name, activity_type, has_multiplayer)
    
    return files

def generate_react_activity_app(activity_name: str, has_multiplayer: bool, activity_type: str) -> str:
    """Generate React Activity app component."""
    code = f'''import React, {{ useState, useEffect }} from 'react';
import {{ DiscordSDK }} from '@discord/embedded-app-sdk';
import './App.css';

const discordSdk = new DiscordSDK(import.meta.env.VITE_DISCORD_CLIENT_ID);

function App() {{
    const [ready, setReady] = useState(false);
    const [user, setUser] = useState(null);
'''
    
    if has_multiplayer:
        code += '''    const [players, setPlayers] = useState([]);
    
    useEffect(() => {
        // Initialize multiplayer
        const initMultiplayer = async () => {
            try {
                await discordSdk.ready();
                // Set up multiplayer listeners
                // See hooks/useMultiplayer.ts for implementation
            } catch (error) {
                console.error('Failed to initialize multiplayer:', error);
            }
        };
        initMultiplayer();
    }, []);
'''
    
    code += '''
    useEffect(() => {
        const initDiscord = async () => {
            try {
                await discordSdk.ready();
                const { user } = await discordSdk.commands.authenticate();
                setUser(user);
                setReady(true);
            } catch (error) {
                console.error('Failed to authenticate:', error);
            }
        };
        initDiscord();
    }, []);

    if (!ready) {
        return <div className="loading">Loading {activity_name}...</div>;
    }

    return (
        <div className="App">
            <header className="App-header">
                <h1>{activity_name}</h1>
                {user && <p>Welcome, {user.username}!</p>}
'''
    
    if has_multiplayer:
        code += '''                <div className="player-list">
                    <h2>Players</h2>
                    {/* Player list component */}
                </div>
'''
    
    code += '''            </header>
            <main className="App-main">
                {/* Your activity content here */}
                <div className="activity-content">
                    <p>Activity content goes here!</p>
                </div>
            </main>
        </div>
    );
}

export default App;
'''
    return code

def generate_react_index() -> str:
    """Generate React index file."""
    return '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
'''

def generate_react_package_json(activity_name: str, has_multiplayer: bool) -> str:
    """Generate React package.json."""
    deps = {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "@discord/embedded-app-sdk": "^1.0.0"
    }
    
    if has_multiplayer:
        deps["socket.io-client"] = "^4.5.4"
    
    pkg = {
        "name": activity_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "dependencies": deps,
        "devDependencies": {
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "@vitejs/plugin-react": "^4.2.0",
            "typescript": "^5.3.3",
            "vite": "^5.0.0"
        }
    }
    return json.dumps(pkg, indent=2)

def generate_tsconfig() -> str:
    """Generate TypeScript config."""
    return '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''

def generate_activity_html(activity_name: str) -> str:
    """Generate HTML file for activity."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{activity_name}</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/index.tsx"></script>
</body>
</html>
'''

def generate_multiplayer_hook() -> str:
    """Generate React hook for multiplayer."""
    return '''import { useState, useEffect } from 'react';
import { DiscordSDK } from '@discord/embedded-app-sdk';

export function useMultiplayer(discordSdk: DiscordSDK) {
    const [players, setPlayers] = useState([]);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        // Initialize multiplayer connection
        const initConnection = async () => {
            try {
                // Set up WebSocket or RPC connection for multiplayer
                // This is a placeholder - implement based on your networking choice
                setIsConnected(true);
            } catch (error) {
                console.error('Multiplayer connection failed:', error);
            }
        };

        initConnection();

        return () => {
            // Cleanup
            setIsConnected(false);
        };
    }, [discordSdk]);

    return { players, isConnected };
}
'''

def generate_player_list_component() -> str:
    """Generate player list component."""
    return '''import React from 'react';

interface Player {
    id: string;
    username: string;
    avatar?: string;
}

interface PlayerListProps {
    players: Player[];
}

export function PlayerList({ players }: PlayerListProps) {
    return (
        <div className="player-list">
            <h3>Players ({players.length})</h3>
            <ul>
                {players.map(player => (
                    <li key={player.id}>
                        {player.avatar && <img src={player.avatar} alt={player.username} />}
                        <span>{player.username}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}
'''

def generate_vanilla_html(activity_name: str, has_multiplayer: bool) -> str:
    """Generate vanilla HTML."""
    code = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{activity_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app">
        <header>
            <h1>{activity_name}</h1>
            <div id="user-info"></div>
'''
    
    if has_multiplayer:
        code += '''            <div id="player-list">
                <h2>Players</h2>
                <ul id="players"></ul>
            </div>
'''
    
    code += '''        </header>
        <main id="activity-content">
            <!-- Activity content here -->
        </main>
    </div>
    <script type="module" src="index.js"></script>
</body>
</html>
'''
    return code

def generate_vanilla_js(activity_name: str, has_multiplayer: bool, activity_type: str) -> str:
    """Generate vanilla JavaScript."""
    code = f'''import {{ DiscordSDK }} from '@discord/embedded-app-sdk';

const discordSdk = new DiscordSDK(import.meta.env.VITE_DISCORD_CLIENT_ID);

async function init() {{
    try {{
        await discordSdk.ready();
        const {{ user }} = await discordSdk.commands.authenticate();
        
        // Display user info
        const userInfo = document.getElementById('user-info');
        if (userInfo) {{
            userInfo.textContent = `Welcome, ${{user.username}}!`;
        }}
        
        // Initialize activity
        initActivity();
'''
    
    if has_multiplayer:
        code += '''
        // Initialize multiplayer
        initMultiplayer();
'''
    
    code += '''    }} catch (error) {{
        console.error('Failed to initialize:', error);
    }}
}}

function initActivity() {{
    // Your activity logic here
    const content = document.getElementById('activity-content');
    if (content) {{
        content.innerHTML = '<p>Activity content goes here!</p>';
    }}
}
'''
    
    if has_multiplayer:
        code += '''
function initMultiplayer() {
    // Multiplayer initialization
    // Set up WebSocket or RPC connection
}
'''
    
    code += '''
init();
'''
    return code

def generate_vanilla_css() -> str:
    """Generate vanilla CSS."""
    return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: #232428;
    color: #ffffff;
    height: 100vh;
    overflow: hidden;
}

#app {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

header {
    padding: 1rem;
    background: #1e1f22;
    border-bottom: 1px solid #2b2d31;
}

h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

#activity-content {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
}
'''

def generate_vanilla_package_json(activity_name: str) -> str:
    """Generate vanilla package.json."""
    pkg = {
        "name": activity_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build"
        },
        "dependencies": {
            "@discord/embedded-app-sdk": "^1.0.0"
        },
        "devDependencies": {
            "vite": "^5.0.0"
        }
    }
    return json.dumps(pkg, indent=2)

def generate_phaser_game(activity_name: str, has_multiplayer: bool) -> str:
    """Generate Phaser game code."""
    return f'''import Phaser from 'phaser';
import {{ DiscordSDK }} from '@discord/embedded-app-sdk';
import GameScene from './scenes/GameScene';

const discordSdk = new DiscordSDK(import.meta.env.VITE_DISCORD_CLIENT_ID);

const config = {{
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game-container',
    physics: {{
        default: 'arcade',
        arcade: {{
            gravity: {{ y: 300 }},
            debug: false
        }}
    }},
    scene: [GameScene]
}};

async function init() {{
    try {{
        await discordSdk.ready();
        const {{ user }} = await discordSdk.commands.authenticate();
        console.log('Authenticated as:', user.username);
        
        // Initialize Phaser game
        const game = new Phaser.Game(config);
'''
    
    if has_multiplayer:
        code += '''
        // Set up multiplayer networking
        // See scenes/GameScene.js for multiplayer implementation
'''
    
    code += '''    }} catch (error) {{
        console.error('Failed to initialize:', error);
    }}
}}

init();
'''

def generate_phaser_scene(has_multiplayer: bool) -> str:
    """Generate Phaser scene."""
    code = '''export default class GameScene extends Phaser.Scene {
    constructor() {
        super({ key: 'GameScene' });
    }

    create() {
        // Create game objects
        this.add.text(400, 300, 'Hello Phaser!', {
            fontSize: '32px',
            fill: '#fff'
        }).setOrigin(0.5);
'''
    
    if has_multiplayer:
        code += '''
        // Initialize multiplayer sync
        this.initMultiplayer();
'''
    
    code += '''    }

    update() {
        // Game loop
    }
'''
    
    if has_multiplayer:
        code += '''
    initMultiplayer() {
        // Multiplayer synchronization logic
    }
'''
    
    code += "}\n"
    return code

def generate_phaser_html(activity_name: str) -> str:
    """Generate Phaser HTML."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{activity_name}</title>
</head>
<body>
    <div id="game-container"></div>
    <script type="module" src="src/index.js"></script>
</body>
</html>
'''

def generate_phaser_package_json(activity_name: str) -> str:
    """Generate Phaser package.json."""
    pkg = {
        "name": activity_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build"
        },
        "dependencies": {
            "@discord/embedded-app-sdk": "^1.0.0",
            "phaser": "^3.70.0"
        },
        "devDependencies": {
            "vite": "^5.0.0"
        }
    }
    return json.dumps(pkg, indent=2)

def generate_activity_manifest(activity_name: str, activity_type: str, has_multiplayer: bool) -> str:
    """Generate activity manifest."""
    manifest = {
        "name": activity_name,
        "type": activity_type,
        "supported_platforms": ["desktop", "mobile"],
        "max_players": 16 if has_multiplayer else 1,
        "description": f"{activity_name} Discord Activity"
    }
    return json.dumps(manifest, indent=2)

def generate_activity_readme(activity_name: str, framework: str, has_multiplayer: bool) -> str:
    """Generate activity README."""
    return f'''# {activity_name}

Discord Activity built with {framework}.

## Features

- Discord integration via Embedded App SDK
{f"- Multiplayer support for up to 16 players" if has_multiplayer else "- Single player experience"}

## Development

1. Install dependencies: `npm install`
2. Set up environment variables:
   - Create `.env` file with `VITE_DISCORD_CLIENT_ID=your_client_id`
3. Run development server: `npm run dev`
4. Build for production: `npm run build`

## Deployment

See Discord Developer Portal for Activity deployment instructions.
'''

def generate_activity_layout_code(layout_type: str, framework: str) -> str:
    """Generate activity layout code."""
    if framework == "react":
        if layout_type == "single-player":
            return '''import React from 'react';

export function SinglePlayerLayout({ children }) {
    return (
        <div className="single-player-layout">
            <div className="game-area">
                {children}
            </div>
            <div className="ui-overlay">
                {/* UI elements */}
            </div>
        </div>
    );
}
'''
        elif layout_type == "multiplayer":
            return '''import React from 'react';
import { PlayerList } from './PlayerList';

export function MultiplayerLayout({ children, players }) {
    return (
        <div className="multiplayer-layout">
            <aside className="sidebar">
                <PlayerList players={players} />
            </aside>
            <main className="game-area">
                {children}
            </main>
        </div>
    );
}
'''
        elif layout_type == "spectator":
            return '''import React from 'react';

export function SpectatorLayout({ gameState }) {
    return (
        <div className="spectator-layout">
            <div className="spectator-view">
                <h2>Spectating</h2>
                {/* Display game state */}
            </div>
        </div>
    );
}
'''
    else:
        return f"// {layout_type} layout for {framework}"

def generate_networking_code(framework: str, transport_type: str) -> str:
    """Generate networking code."""
    if transport_type == "websocket":
        return f'''// WebSocket networking for {framework}
import io from 'socket.io-client';

const socket = io('wss://your-game-server.com');

socket.on('connect', () => {{
    console.log('Connected to game server');
}});

socket.on('game-state', (state) => {{
    // Update game state
}});

export function sendGameAction(action) {{
    socket.emit('game-action', action);
}}
'''
    elif transport_type == "webrtc":
        return f'''// WebRTC networking for {framework}
// Initialize WebRTC peer connection
const pc = new RTCPeerConnection();

// Set up data channel for game state sync
const dataChannel = pc.createDataChannel('game-data');

dataChannel.onmessage = (event) => {{
    const gameState = JSON.parse(event.data);
    // Update game state
}};

export function sendGameState(state) {{
    if (dataChannel.readyState === 'open') {{
        dataChannel.send(JSON.stringify(state));
    }}
}}
'''
    elif transport_type == "discord-rpc":
        return f'''// Discord RPC networking for {framework}
import {{ DiscordSDK }} from '@discord/embedded-app-sdk';

const discordSdk = new DiscordSDK(import.meta.env.VITE_DISCORD_CLIENT_ID);

export async function sendActivityUpdate(activityData) {{
    await discordSdk.commands.setActivity({{
        activity: activityData
    }});
}}

export async function subscribeToActivityUpdates(callback) {{
    // Subscribe to activity updates via Discord RPC
    // Implementation depends on Discord SDK version
}}
'''
    return f"// Networking code for {framework} using {transport_type}"

def validate_activity_metadata(metadata: dict) -> dict:
    """Validate activity metadata."""
    errors = []
    warnings = []
    
    required_fields = ["name", "type"]
    for field in required_fields:
        if field not in metadata:
            errors.append(f"Missing required field: {field}")
    
    # Validate type
    if "type" in metadata and metadata["type"] not in ["embedded", "iframe"]:
        errors.append(f"Invalid type: {metadata['type']}. Must be 'embedded' or 'iframe'")
    
    # Validate max_players
    if "max_players" in metadata:
        max_players = metadata["max_players"]
        if not isinstance(max_players, int) or max_players < 1 or max_players > 16:
            errors.append("max_players must be an integer between 1 and 16")
    
    # Check for recommended fields
    recommended_fields = ["description", "supported_platforms", "assets"]
    for field in recommended_fields:
        if field not in metadata:
            warnings.append(f"Missing recommended field: {field}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

