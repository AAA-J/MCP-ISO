"""Tools for Discord webhooks and OAuth2."""

from mcp.types import Tool, TextContent
import json

webhooks_tools = [
    Tool(
        name="discord_generate_webhook",
        description="Generate webhook implementation code for receiving Discord webhook events",
        inputSchema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript", "javascript", "nodejs"],
                    "description": "Programming language"
                },
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi", "flask", "koa", "hono"],
                    "description": "Web framework"
                },
                "webhookType": {
                    "type": "string",
                    "enum": ["incoming", "outgoing", "both"],
                    "default": "incoming",
                    "description": "Type of webhook"
                }
            },
            "required": ["language", "framework"]
        }
    ),
    Tool(
        name="discord_generate_oauth2_flow",
        description="Generate OAuth2 authorization flow implementation",
        inputSchema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript", "javascript"],
                    "description": "Programming language"
                },
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi", "flask"],
                    "description": "Web framework"
                },
                "grantType": {
                    "type": "string",
                    "enum": ["authorization_code", "client_credentials"],
                    "default": "authorization_code",
                    "description": "OAuth2 grant type"
                }
            },
            "required": ["language", "framework"]
        }
    ),
    Tool(
        name="discord_generate_webhook_handler",
        description="Generate webhook event handler code",
        inputSchema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript", "javascript"]
                },
                "events": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["message.create", "message.update", "guild.member.add", "guild.member.remove"]
                    },
                    "description": "Events to handle"
                }
            },
            "required": ["language", "events"]
        }
    ),
]

async def handle_webhooks(name: str, arguments: dict) -> list[TextContent]:
    """Handle webhook and OAuth2 tool calls."""
    if name == "discord_generate_webhook":
        language = arguments.get("language")
        framework = arguments.get("framework")
        webhook_type = arguments.get("webhookType", "incoming")
        
        code = generate_webhook_code(language, framework, webhook_type)
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_oauth2_flow":
        language = arguments.get("language")
        framework = arguments.get("framework")
        grant_type = arguments.get("grantType", "authorization_code")
        
        code = generate_oauth2_code(language, framework, grant_type)
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_webhook_handler":
        language = arguments.get("language")
        events = arguments.get("events", [])
        
        code = generate_webhook_handler_code(language, events)
        return [TextContent(type="text", text=code)]
    else:
        raise ValueError(f"Unknown webhook tool: {name}")

def generate_webhook_code(language: str, framework: str, webhook_type: str) -> str:
    """Generate webhook implementation code."""
    if language == "python":
        if framework == "fastapi":
            return f'''from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import hmac
import hashlib
import json

app = FastAPI()

WEBHOOK_SECRET = "your_webhook_secret_here"

@app.post("/webhook")
async def handle_webhook(
    request: Request,
    x_signature_ed25519: str = Header(None),
    x_signature_timestamp: str = Header(None)
):
    """Handle incoming Discord webhook."""
    body = await request.body()
    
    # Verify webhook signature
    if not verify_signature(body, x_signature_ed25519, x_signature_timestamp):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    data = json.loads(body)
    event_type = request.headers.get("x-discord-event-type")
    
    # Handle different event types
    if event_type == "MESSAGE_CREATE":
        await handle_message_create(data)
    elif event_type == "GUILD_MEMBER_ADD":
        await handle_guild_member_add(data)
    
    return JSONResponse(content={{"status": "ok"}})

def verify_signature(body: bytes, signature: str, timestamp: str) -> bool:
    """Verify Discord webhook signature."""
    if not signature or not timestamp:
        return False
    
    message = timestamp.encode() + body
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

async def handle_message_create(data: dict):
    """Handle message create event."""
    print(f"New message: {{data.get('content')}}")

async def handle_guild_member_add(data: dict):
    """Handle guild member add event."""
    print(f"New member joined: {{data.get('user', {{}}).get('username')}}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        elif framework == "flask":
            return f'''from flask import Flask, request, jsonify
import hmac
import hashlib
import json

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret_here"

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handle incoming Discord webhook."""
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    
    if not verify_signature(request.data, signature, timestamp):
        return jsonify({{"error": "Invalid signature"}}), 401
    
    data = request.get_json()
    event_type = request.headers.get("X-Discord-Event-Type")
    
    # Handle events
    if event_type == "MESSAGE_CREATE":
        handle_message_create(data)
    
    return jsonify({{"status": "ok"}})

def verify_signature(body: bytes, signature: str, timestamp: str) -> bool:
    """Verify Discord webhook signature."""
    if not signature or not timestamp:
        return False
    
    message = timestamp.encode() + body
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

def handle_message_create(data: dict):
    """Handle message create event."""
    print(f"New message: {{data.get('content')}}")

if __name__ == "__main__":
    app.run(port=8000)
'''
    elif language in ["typescript", "javascript", "nodejs"]:
        if framework == "express":
            return f'''import express from 'express';
import crypto from 'crypto';

const app = express();
const WEBHOOK_SECRET = 'your_webhook_secret_here';

app.use(express.raw({{ type: 'application/json' }}));

app.post('/webhook', (req, res) => {{
    const signature = req.headers['x-signature-ed25519'] as string;
    const timestamp = req.headers['x-signature-timestamp'] as string;
    
    if (!verifySignature(req.body, signature, timestamp)) {{
        return res.status(401).json({{ error: 'Invalid signature' }});
    }}
    
    const data = JSON.parse(req.body.toString());
    const eventType = req.headers['x-discord-event-type'] as string;
    
    // Handle events
    if (eventType === 'MESSAGE_CREATE') {{
        handleMessageCreate(data);
    }} else if (eventType === 'GUILD_MEMBER_ADD') {{
        handleGuildMemberAdd(data);
    }}
    
    res.json({{ status: 'ok' }});
}});

function verifySignature(body: Buffer, signature: string, timestamp: string): boolean {{
    if (!signature || !timestamp) return false;
    
    const message = Buffer.concat([Buffer.from(timestamp), body]);
    const expectedSignature = crypto
        .createHmac('sha256', WEBHOOK_SECRET)
        .update(message)
        .digest('hex');
    
    return crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expectedSignature)
    );
}}

function handleMessageCreate(data: any) {{
    console.log(`New message: ${{data.content}}`);
}}

function handleGuildMemberAdd(data: any) {{
    console.log(`New member: ${{data.user?.username}}`);
}}

app.listen(8000, () => {{
    console.log('Webhook server running on port 8000');
}});
'''
        elif framework == "hono":
            return f'''import {{ Hono }} from 'hono';
import crypto from 'crypto';

const app = new Hono();
const WEBHOOK_SECRET = 'your_webhook_secret_here';

app.post('/webhook', async (c) => {{
    const signature = c.req.header('x-signature-ed25519');
    const timestamp = c.req.header('x-signature-timestamp');
    const body = await c.req.arrayBuffer();
    
    if (!verifySignature(Buffer.from(body), signature, timestamp)) {{
        return c.json({{ error: 'Invalid signature' }}, 401);
    }}
    
    const data = JSON.parse(Buffer.from(body).toString());
    const eventType = c.req.header('x-discord-event-type');
    
    if (eventType === 'MESSAGE_CREATE') {{
        handleMessageCreate(data);
    }}
    
    return c.json({{ status: 'ok' }});
}});

function verifySignature(body: Buffer, signature: string, timestamp: string): boolean {{
    if (!signature || !timestamp) return false;
    const message = Buffer.concat([Buffer.from(timestamp), body]);
    const expectedSignature = crypto
        .createHmac('sha256', WEBHOOK_SECRET)
        .update(message)
        .digest('hex');
    return crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expectedSignature)
    );
}}

function handleMessageCreate(data: any) {{
    console.log(`New message: ${{data.content}}`);
}}

export default app;
'''
    
    return f"# Webhook code for {language} with {framework}"

def generate_oauth2_code(language: str, framework: str, grant_type: str) -> str:
    """Generate OAuth2 flow code."""
    if language == "python" and framework == "fastapi":
        return f'''from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import os

app = FastAPI()

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
SCOPE = "identify email"

@app.get("/auth")
async def authorize():
    """Redirect to Discord OAuth2 authorization."""
    auth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={{CLIENT_ID}}"
        f"&redirect_uri={{REDIRECT_URI}}"
        f"&response_type=code"
        f"&scope={{SCOPE}}"
    )
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(code: str):
    """Handle OAuth2 callback."""
    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://discord.com/api/oauth2/token",
            data={{
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            }},
            headers={{"Content-Type": "application/x-www-form-urlencoded"}},
        )
        
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get token")
        
        token_data = token_response.json()
        access_token = token_data["access_token"]
        
        # Get user info
        user_response = await client.get(
            "https://discord.com/api/users/@me",
            headers={{"Authorization": f"Bearer {{access_token}}"}},
        )
        
        user_data = user_response.json()
        return {{
            "access_token": access_token,
            "user": user_data,
        }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    elif language in ["typescript", "javascript"] and framework == "express":
        return f'''import express from 'express';
import axios from 'axios';

const app = express();
const CLIENT_ID = process.env.DISCORD_CLIENT_ID!;
const CLIENT_SECRET = process.env.DISCORD_CLIENT_SECRET!;
const REDIRECT_URI = 'http://localhost:8000/callback';
const SCOPE = 'identify email';

app.get('/auth', (req, res) => {{
    const authUrl = `https://discord.com/api/oauth2/authorize?client_id=${{CLIENT_ID}}&redirect_uri=${{encodeURIComponent(REDIRECT_URI)}}&response_type=code&scope=${{SCOPE}}`;
    res.redirect(authUrl);
}});

app.get('/callback', async (req, res) => {{
    const {{ code }} = req.query;
    
    if (!code) {{
        return res.status(400).json({{ error: 'No code provided' }});
    }}
    
    try {{
        // Exchange code for token
        const tokenResponse = await axios.post(
            'https://discord.com/api/oauth2/token',
            new URLSearchParams({{
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                grant_type: 'authorization_code',
                code: code as string,
                redirect_uri: REDIRECT_URI,
            }}),
            {{
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
            }}
        );
        
        const {{ access_token }} = tokenResponse.data;
        
        // Get user info
        const userResponse = await axios.get('https://discord.com/api/users/@me', {{
            headers: {{
                Authorization: `Bearer ${{access_token}}`,
            }},
        }});
        
        res.json({{
            access_token,
            user: userResponse.data,
        }});
    }} catch (error) {{
        console.error('OAuth2 error:', error);
        res.status(500).json({{ error: 'Failed to authenticate' }});
    }}
}});

app.listen(8000, () => {{
    console.log('OAuth2 server running on port 8000');
}});
'''
    
    return f"# OAuth2 code for {language} with {framework}, grant type: {grant_type}"

def generate_webhook_handler_code(language: str, events: list) -> str:
    """Generate webhook event handler code."""
    handlers = []
    for event in events:
        if event == "message.create":
            handlers.append("handleMessageCreate")
        elif event == "message.update":
            handlers.append("handleMessageUpdate")
        elif event == "guild.member.add":
            handlers.append("handleGuildMemberAdd")
        elif event == "guild.member.remove":
            handlers.append("handleGuildMemberRemove")
    
    if language == "python":
        code = "def handle_webhook_event(event_type: str, data: dict):\n"
        code += "    \"\"\"Route webhook events to appropriate handlers.\"\"\"\n"
        code += "    handlers = {\n"
        for handler in handlers:
            event_name = handler.replace("handle", "").lower()
            code += f'        "{event_name}": {handler},\n'
        code += "    }\n"
        code += "    handler = handlers.get(event_type)\n"
        code += "    if handler:\n"
        code += "        handler(data)\n\n"
        
        for handler in handlers:
            code += f"def {handler}(data: dict):\n"
            code += f'    """Handle {handler.replace("handle", "")} event."""\n'
            code += "    print(f\"Event: {handler}, Data: {data}\")\n\n"
        
        return code
    else:
        code = "function handleWebhookEvent(eventType: string, data: any) {\n"
        code += "    const handlers: Record<string, (data: any) => void> = {\n"
        for handler in handlers:
            event_name = handler.replace("handle", "").toLowerCase()
            code += f'        "{event_name}": {handler},\n'
        code += "    };\n\n"
        code += "    const handler = handlers[eventType];\n"
        code += "    if (handler) handler(data);\n"
        code += "}\n\n"
        
        for handler in handlers:
            code += f"function {handler}(data: any) {{\n"
            code += f'    console.log(`Event: {handler}, Data:`, data);\n'
            code += "}\n\n"
        
        return code

