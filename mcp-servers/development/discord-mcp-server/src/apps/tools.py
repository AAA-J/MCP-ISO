"""Tools for building Discord apps/bots."""

from mcp.types import Tool, TextContent
import json

apps_tools = [
    Tool(
        name="discord_scaffold_app",
        description="Generate starter code for a Discord bot/application with proper structure, dependencies, and configuration",
        inputSchema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["typescript", "python", "javascript"],
                    "description": "Programming language"
                },
                "framework": {
                    "type": "string",
                    "enum": ["discord.js", "discord.py", "rest"],
                    "description": "Discord library/framework"
                },
                "features": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["slash-commands", "components", "webhooks", "oauth2", "events", "modals"]
                    },
                    "description": "Features to include"
                },
                "appName": {
                    "type": "string",
                    "description": "Name of the application"
                },
                "botToken": {
                    "type": "string",
                    "description": "Bot token (optional, can use env var)"
                }
            },
            "required": ["language", "framework", "features"]
        }
    ),
    Tool(
        name="discord_generate_slash_command",
        description="Generate code for a Discord slash command with proper schema",
        inputSchema={
            "type": "object",
            "properties": {
                "commandName": {
                    "type": "string",
                    "description": "Name of the slash command"
                },
                "description": {
                    "type": "string",
                    "description": "Command description"
                },
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "type": {"type": "number"},
                            "required": {"type": "boolean"}
                        }
                    }
                },
                "language": {
                    "type": "string",
                    "enum": ["typescript", "python"]
                },
                "framework": {
                    "type": "string",
                    "enum": ["discord.js", "discord.py"]
                }
            },
            "required": ["commandName", "description", "language", "framework"]
        }
    ),
    Tool(
        name="discord_generate_component",
        description="Generate code for Discord message components (buttons, select menus, modals)",
        inputSchema={
            "type": "object",
            "properties": {
                "componentType": {
                    "type": "string",
                    "enum": ["button", "select-menu", "modal", "text-input"],
                    "description": "Type of component"
                },
                "language": {
                    "type": "string",
                    "enum": ["typescript", "python"]
                },
                "framework": {
                    "type": "string",
                    "enum": ["discord.js", "discord.py"]
                }
            },
            "required": ["componentType", "language", "framework"]
        }
    ),
    Tool(
        name="discord_validate_interaction",
        description="Validate an interaction payload against Discord API schema",
        inputSchema={
            "type": "object",
            "properties": {
                "payload": {
                    "type": "object",
                    "description": "Interaction payload to validate"
                },
                "interactionType": {
                    "type": "number",
                    "enum": [1, 2, 3, 4, 5],
                    "description": "Interaction type"
                }
            },
            "required": ["payload", "interactionType"]
        }
    ),
    Tool(
        name="discord_check_permissions",
        description="Verify bot permissions are sufficient for required operations",
        inputSchema={
            "type": "object",
            "properties": {
                "operations": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["send-messages", "read-messages", "manage-messages", "manage-channels"]
                    }
                },
                "currentPermissions": {
                    "type": "string",
                    "description": "Current permission integer"
                }
            },
            "required": ["operations"]
        }
    ),
]

async def handle_apps(name: str, arguments: dict) -> list[TextContent]:
    """Handle Discord apps tool calls."""
    if name == "discord_scaffold_app":
        language = arguments.get("language")
        framework = arguments.get("framework")
        features = arguments.get("features", [])
        app_name = arguments.get("appName", "discord-app")
        bot_token = arguments.get("botToken", "")
        
        result = {
            "success": True,
            "language": language,
            "framework": framework,
            "features": features,
            "appName": app_name,
            "files": generate_app_files(language, framework, features, app_name, bot_token)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_generate_slash_command":
        command_name = arguments.get("commandName")
        description = arguments.get("description", "")
        options = arguments.get("options", [])
        language = arguments.get("language")
        framework = arguments.get("framework")
        
        code = generate_slash_command_code(command_name, description, options, language, framework)
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_component":
        component_type = arguments.get("componentType")
        language = arguments.get("language")
        framework = arguments.get("framework")
        
        code = generate_component_code(component_type, language, framework)
        return [TextContent(type="text", text=code)]
    elif name == "discord_validate_interaction":
        payload = arguments.get("payload")
        interaction_type = arguments.get("interactionType")
        
        result = validate_interaction_payload(payload, interaction_type)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_check_permissions":
        operations = arguments.get("operations", [])
        current_permissions = arguments.get("currentPermissions")
        
        result = check_bot_permissions(operations, current_permissions)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown Discord apps tool: {name}")

def generate_app_files(language: str, framework: str, features: list, app_name: str, bot_token: str = "") -> dict:
    """Generate Discord app file structure with complete code."""
    files = {}
    token_ref = bot_token if bot_token else "process.env.DISCORD_TOKEN" if language != "python" else "os.getenv('DISCORD_TOKEN')"
    
    if language == "python" and framework == "discord.py":
        files["src/index.py"] = generate_python_bot_code(app_name, features, token_ref)
        files["requirements.txt"] = generate_python_requirements(features)
        files[".env.example"] = "DISCORD_TOKEN=your_bot_token_here\nDISCORD_CLIENT_ID=your_client_id"
        files["README.md"] = f"# {app_name}\n\nDiscord bot built with discord.py\n\n## Setup\n\n1. Install dependencies: `pip install -r requirements.txt`\n2. Copy `.env.example` to `.env` and add your bot token\n3. Run: `python src/index.py`"
        
        if "slash-commands" in features:
            files["src/commands/__init__.py"] = ""
            files["src/commands/ping.py"] = generate_python_slash_command_example()
        
        if "components" in features:
            files["src/components/__init__.py"] = ""
            files["src/components/buttons.py"] = generate_python_component_example()
            
    elif language in ["typescript", "javascript"] and framework == "discord.js":
        ext = "ts" if language == "typescript" else "js"
        files[f"src/index.{ext}"] = generate_typescript_bot_code(app_name, features, token_ref, language)
        files["package.json"] = generate_typescript_package_json(app_name, features, language)
        files[".env.example"] = "DISCORD_TOKEN=your_bot_token_here\nDISCORD_CLIENT_ID=your_client_id"
        files["README.md"] = f"# {app_name}\n\nDiscord bot built with discord.js\n\n## Setup\n\n1. Install dependencies: `npm install`\n2. Copy `.env.example` to `.env` and add your bot token\n3. Run: `npm start`"
        
        if "slash-commands" in features:
            files[f"src/commands/ping.{ext}"] = generate_typescript_slash_command_example(language)
        
        if "components" in features:
            files[f"src/components/buttons.{ext}"] = generate_typescript_component_example(language)
    
    return files

def generate_python_bot_code(app_name: str, features: list, token_ref: str) -> str:
    """Generate Python discord.py bot code."""
    code = f'''#!/usr/bin/env python3
"""
{app_name} - Discord Bot
Built with discord.py
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
'''
    
    if "slash-commands" in features:
        code += "intents.guild_messages = True\n"
    
    code += f'''
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when bot is ready."""
    print(f'{{bot.user}} has connected to Discord!')
    print(f'Bot is in {{len(bot.guilds)}} guilds')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'Synced {{len(synced)}} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {{e}}')

@bot.event
async def on_guild_join(guild):
    """Called when bot joins a guild."""
    print(f'Joined guild: {{guild.name}} (id: {{guild.id}})')

@bot.event
async def on_guild_remove(guild):
    """Called when bot leaves a guild."""
    print(f'Left guild: {{guild.name}} (id: {{guild.id}})')
'''
    
    if "slash-commands" in features:
        code += '''
# Load slash commands
try:
    from commands import ping
except ImportError:
    pass
'''
    
    if "components" in features:
        code += '''
# Load component handlers
try:
    from components import buttons
except ImportError:
    pass
'''
    
    code += f'''
if __name__ == '__main__':
    token = {token_ref}
    if not token:
        print('Error: DISCORD_TOKEN not found in environment variables')
        exit(1)
    bot.run(token)
'''
    return code

def generate_typescript_bot_code(app_name: str, features: list, token_ref: str, language: str) -> str:
    """Generate TypeScript/JavaScript discord.js bot code."""
    comment = "//" if language == "javascript" else "//"
    code = f'''{comment} {app_name} - Discord Bot
{comment} Built with discord.js

import {{ Client, GatewayIntentBits, Collection }} from 'discord.js';
import {{ config }} from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';

config();

const client = new Client({{
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ],
}});

// Command collection
client.commands = new Collection();

// Load commands
'''
    
    if "slash-commands" in features:
        code += '''
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js') || file.endsWith('.ts'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    if ('data' in command && 'execute' in command) {
        client.commands.set(command.data.name, command);
    }
}
'''
    
    code += '''
client.once('ready', () => {
    console.log(`Ready! Logged in as ${client.user.tag}`);
    console.log(`Bot is in ${client.guilds.cache.size} guilds`);
});

client.on('guildCreate', guild => {
    console.log(`Joined guild: ${guild.name} (id: ${guild.id})`);
});

client.on('guildDelete', guild => {
    console.log(`Left guild: ${guild.name} (id: ${guild.id})`);
});
'''
    
    if "slash-commands" in features:
        code += '''
client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;

    const command = client.commands.get(interaction.commandName);
    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(`Error executing ${interaction.commandName}:`, error);
        await interaction.reply({ 
            content: 'There was an error while executing this command!', 
            ephemeral: true 
        });
    }
});
'''
    
    if "components" in features:
        code += '''
client.on('interactionCreate', async interaction => {
    if (interaction.isButton() || interaction.isStringSelectMenu()) {
        // Handle component interactions
        // See components/buttons.ts for examples
    }
});
'''
    
    code += f'''
const token = {token_ref};
if (!token) {{
    console.error('Error: DISCORD_TOKEN not found in environment variables');
    process.exit(1);
}}

client.login(token);
'''
    return code

def generate_python_requirements(features: list) -> str:
    """Generate Python requirements.txt."""
    deps = ["discord.py>=2.3.0", "python-dotenv>=1.0.0"]
    if "webhooks" in features:
        deps.append("aiohttp>=3.9.0")
    return "\n".join(deps) + "\n"

def generate_typescript_package_json(app_name: str, features: list, language: str) -> str:
    """Generate package.json for TypeScript/JavaScript."""
    deps = {
        "discord.js": "^14.14.1",
        "dotenv": "^16.3.1"
    }
    dev_deps = {}
    if language == "typescript":
        dev_deps = {
            "@types/node": "^20.10.0",
            "typescript": "^5.3.3"
        }
    
    pkg = {
        "name": app_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "description": f"{app_name} Discord Bot",
        "main": f"dist/index.{'js' if language == 'javascript' else 'js'}",
        "scripts": {
            "start": f"node dist/index.js" if language == "typescript" else "node src/index.js",
            "build": "tsc" if language == "typescript" else "echo 'No build step needed'",
            "dev": "ts-node src/index.ts" if language == "typescript" else "node src/index.js"
        },
        "dependencies": deps,
        "devDependencies": dev_deps if dev_deps else {}
    }
    return json.dumps(pkg, indent=2)

def generate_slash_command_code(command_name: str, description: str, options: list, language: str, framework: str) -> str:
    """Generate slash command code."""
    if language == "python" and framework == "discord.py":
        return generate_python_slash_command(command_name, description, options)
    elif language in ["typescript", "javascript"] and framework == "discord.js":
        return generate_typescript_slash_command(command_name, description, options, language)
    else:
        return f"# Slash command: {command_name}\n# Language: {language}, Framework: {framework}"

def generate_python_slash_command(command_name: str, description: str, options: list) -> str:
    """Generate Python slash command."""
    option_types = {
        3: "str", 4: "int", 5: "bool", 6: "discord.Member", 
        7: "discord.abc.GuildChannel", 8: "discord.Role", 10: "float"
    }
    
    code = f'''import discord
from discord import app_commands
from discord.ext import commands

class {command_name.title().replace('_', '')}Command(commands.Cog):
    """{description}"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="{command_name}", description="{description}")
'''
    
    if options:
        params = []
        for opt in options:
            opt_type = option_types.get(opt.get("type", 3), "str")
            required = "" if opt.get("required", False) else " = None"
            params.append(f"        {opt['name']}: {opt_type}{required}")
        
        code += "    async def command(self, interaction: discord.Interaction" + "".join([f",\n{p}" for p in params]) + "):\n"
    else:
        code += "    async def command(self, interaction: discord.Interaction):\n"
    
    code += f'''        """Handle /{command_name} command."""
        await interaction.response.send_message(f'Hello! This is the {command_name} command.')
'''
    
    if options:
        code += "        # Process options:\n"
        for opt in options:
            code += f"        # {opt['name']}: {opt.get('description', '')}\n"
    
    code += '''
async def setup(bot: commands.Bot):
    await bot.add_cog(PingCommand(bot))
'''
    return code

def generate_typescript_slash_command(command_name: str, description: str, options: list, language: str) -> str:
    """Generate TypeScript/JavaScript slash command."""
    option_types = {
        3: "string", 4: "number", 5: "boolean", 6: "User", 
        7: "Channel", 8: "Role", 10: "number"
    }
    
    code = f'''import {{ SlashCommandBuilder, ChatInputCommandInteraction }} from 'discord.js';

export const data = new SlashCommandBuilder()
    .setName('{command_name}')
    .setDescription('{description}')
'''
    
    for opt in options:
        opt_type_num = opt.get("type", 3)
        opt_type = option_types.get(opt_type_num, "string")
        required = opt.get("required", False)
        
        if opt_type_num == 3:  # String
            code += f"    .addStringOption(option =>\n"
            code += f"        option.setName('{opt['name']}')\n"
            code += f"            .setDescription('{opt.get('description', '')}')\n"
            if required:
                code += "            .setRequired(true)\n"
            code += "    )\n"
        elif opt_type_num == 4:  # Integer
            code += f"    .addIntegerOption(option =>\n"
            code += f"        option.setName('{opt['name']}')\n"
            code += f"            .setDescription('{opt.get('description', '')}')\n"
            if required:
                code += "            .setRequired(true)\n"
            code += "    )\n"
        elif opt_type_num == 5:  # Boolean
            code += f"    .addBooleanOption(option =>\n"
            code += f"        option.setName('{opt['name']}')\n"
            code += f"            .setDescription('{opt.get('description', '')}')\n"
            code += "    )\n"
    
    code += f''';

export async function execute(interaction: ChatInputCommandInteraction) {{
    await interaction.reply(`Hello! This is the {command_name} command.`);
'''
    
    if options:
        code += "    // Get options:\n"
        for opt in options:
            opt_type = option_types.get(opt.get("type", 3), "string")
            code += f"    const {opt['name']} = interaction.options.get{opt_type.title() if opt_type != 'string' else 'String'}('{opt['name']}');\n"
    
    code += "}\n"
    return code

def generate_component_code(component_type: str, language: str, framework: str) -> str:
    """Generate component code."""
    if language == "python" and framework == "discord.py":
        return generate_python_component(component_type)
    elif language in ["typescript", "javascript"] and framework == "discord.js":
        return generate_typescript_component(component_type, language)
    else:
        return f"# Component: {component_type}\n# Language: {language}"

def generate_python_component(component_type: str) -> str:
    """Generate Python component code."""
    if component_type == "button":
        return '''import discord
from discord import ui
from discord.ext import commands

class ButtonView(ui.View):
    """Example button component view."""
    
    def __init__(self):
        super().__init__(timeout=180)
    
    @ui.button(label='Click Me!', style=discord.ButtonStyle.primary)
    async def click_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message('Button clicked!', ephemeral=True)
    
    @ui.button(label='Danger', style=discord.ButtonStyle.danger)
    async def danger_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message('Danger button clicked!', ephemeral=True)

# Usage in command:
# view = ButtonView()
# await interaction.response.send_message('Click a button!', view=view)
'''
    elif component_type == "select-menu":
        return '''import discord
from discord import ui
from discord.ext import commands

class SelectMenuView(ui.View):
    """Example select menu component."""
    
    def __init__(self):
        super().__init__(timeout=180)
    
    @ui.select(
        placeholder='Choose an option...',
        options=[
            discord.SelectOption(label='Option 1', value='1', description='First option'),
            discord.SelectOption(label='Option 2', value='2', description='Second option'),
            discord.SelectOption(label='Option 3', value='3', description='Third option'),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: ui.Select):
        await interaction.response.send_message(f'You selected: {select.values[0]}', ephemeral=True)

# Usage:
# view = SelectMenuView()
# await interaction.response.send_message('Choose an option:', view=view)
'''
    elif component_type == "modal":
        return '''import discord
from discord import ui
from discord.ext import commands

class ExampleModal(ui.Modal, title='Example Form'):
    """Example modal dialog."""
    
    name = ui.TextInput(label='Name', placeholder='Enter your name...', required=True)
    age = ui.TextInput(label='Age', placeholder='Enter your age...', required=True, max_length=3)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Thanks {self.name.value}! You are {self.age.value} years old.',
            ephemeral=True
        )
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('Something went wrong!', ephemeral=True)

# Usage:
# modal = ExampleModal()
# await interaction.response.send_modal(modal)
'''
    elif component_type == "text-input":
        return '''import discord
from discord import ui

class TextInputModal(ui.Modal, title='Text Input'):
    """Example text input in modal."""
    
    short_input = ui.TextInput(
        label='Short Input',
        placeholder='Enter text...',
        required=True,
        max_length=100
    )
    
    long_input = ui.TextInput(
        label='Long Input',
        style=discord.TextStyle.paragraph,
        placeholder='Enter longer text...',
        required=False,
        max_length=1000
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Short: {self.short_input.value}\\nLong: {self.long_input.value}',
            ephemeral=True
        )

# Usage:
# modal = TextInputModal()
# await interaction.response.send_modal(modal)
'''
    return f"# Component type: {component_type}"

def generate_typescript_component(component_type: str, language: str) -> str:
    """Generate TypeScript/JavaScript component code."""
    if component_type == "button":
        return '''import { ActionRowBuilder, ButtonBuilder, ButtonStyle, ChatInputCommandInteraction } from 'discord.js';

export async function createButtonView(interaction: ChatInputCommandInteraction) {
    const row = new ActionRowBuilder<ButtonBuilder>()
        .addComponents(
            new ButtonBuilder()
                .setCustomId('primary_button')
                .setLabel('Click Me!')
                .setStyle(ButtonStyle.Primary),
            new ButtonBuilder()
                .setCustomId('danger_button')
                .setLabel('Danger')
                .setStyle(ButtonStyle.Danger)
        );
    
    await interaction.reply({ content: 'Click a button!', components: [row] });
}

// Handle button interaction:
// client.on('interactionCreate', async interaction => {
//     if (!interaction.isButton()) return;
//     if (interaction.customId === 'primary_button') {
//         await interaction.reply({ content: 'Button clicked!', ephemeral: true });
//     }
// });
'''
    elif component_type == "select-menu":
        return '''import { ActionRowBuilder, StringSelectMenuBuilder, ChatInputCommandInteraction } from 'discord.js';

export async function createSelectMenu(interaction: ChatInputCommandInteraction) {
    const row = new ActionRowBuilder<StringSelectMenuBuilder>()
        .addComponents(
            new StringSelectMenuBuilder()
                .setCustomId('example_select')
                .setPlaceholder('Choose an option...')
                .addOptions(
                    { label: 'Option 1', value: '1', description: 'First option' },
                    { label: 'Option 2', value: '2', description: 'Second option' },
                    { label: 'Option 3', value: '3', description: 'Third option' }
                )
        );
    
    await interaction.reply({ content: 'Choose an option:', components: [row] });
}

// Handle select menu:
// client.on('interactionCreate', async interaction => {
//     if (!interaction.isStringSelectMenu()) return;
//     if (interaction.customId === 'example_select') {
//         await interaction.reply({ content: `You selected: ${interaction.values[0]}`, ephemeral: true });
//     }
// });
'''
    elif component_type == "modal":
        return '''import { ModalBuilder, TextInputBuilder, TextInputStyle, ActionRowBuilder, ChatInputCommandInteraction } from 'discord.js';

export async function createModal(interaction: ChatInputCommandInteraction) {
    const modal = new ModalBuilder()
        .setCustomId('example_modal')
        .setTitle('Example Form');
    
    const nameInput = new TextInputBuilder()
        .setCustomId('name_input')
        .setLabel('Name')
        .setStyle(TextInputStyle.Short)
        .setPlaceholder('Enter your name...')
        .setRequired(true)
        .setMaxLength(100);
    
    const ageInput = new TextInputBuilder()
        .setCustomId('age_input')
        .setLabel('Age')
        .setStyle(TextInputStyle.Short)
        .setPlaceholder('Enter your age...')
        .setRequired(true)
        .setMaxLength(3);
    
    const firstActionRow = new ActionRowBuilder<TextInputBuilder>().addComponents(nameInput);
    const secondActionRow = new ActionRowBuilder<TextInputBuilder>().addComponents(ageInput);
    
    modal.addComponents(firstActionRow, secondActionRow);
    
    await interaction.showModal(modal);
}

// Handle modal submit:
// client.on('interactionCreate', async interaction => {
//     if (!interaction.isModalSubmit()) return;
//     if (interaction.customId === 'example_modal') {
//         const name = interaction.fields.getTextInputValue('name_input');
//         const age = interaction.fields.getTextInputValue('age_input');
//         await interaction.reply({ content: `Thanks ${name}! You are ${age} years old.`, ephemeral: true });
//     }
// });
'''
    elif component_type == "text-input":
        return '''import { ModalBuilder, TextInputBuilder, TextInputStyle, ActionRowBuilder, ChatInputCommandInteraction } from 'discord.js';

export async function createTextInputModal(interaction: ChatInputCommandInteraction) {
    const modal = new ModalBuilder()
        .setCustomId('text_input_modal')
        .setTitle('Text Input');
    
    const shortInput = new TextInputBuilder()
        .setCustomId('short_input')
        .setLabel('Short Input')
        .setStyle(TextInputStyle.Short)
        .setPlaceholder('Enter text...')
        .setRequired(true)
        .setMaxLength(100);
    
    const longInput = new TextInputBuilder()
        .setCustomId('long_input')
        .setLabel('Long Input')
        .setStyle(TextInputStyle.Paragraph)
        .setPlaceholder('Enter longer text...')
        .setRequired(false)
        .setMaxLength(1000);
    
    const firstRow = new ActionRowBuilder<TextInputBuilder>().addComponents(shortInput);
    const secondRow = new ActionRowBuilder<TextInputBuilder>().addComponents(longInput);
    
    modal.addComponents(firstRow, secondRow);
    await interaction.showModal(modal);
}
'''
    return f"// Component type: {component_type}"

def generate_python_slash_command_example() -> str:
    """Generate example Python slash command."""
    return '''import discord
from discord import app_commands
from discord.ext import commands

class PingCommand(commands.Cog):
    """Simple ping command example."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Respond with bot latency."""
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latency: {latency}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCommand(bot))
'''

def generate_python_component_example() -> str:
    """Generate example Python component."""
    return '''import discord
from discord import ui
from discord.ext import commands

class ExampleButtonView(ui.View):
    """Example button view."""
    
    def __init__(self):
        super().__init__(timeout=180)
    
    @ui.button(label='Click Me!', style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message('Button was clicked!', ephemeral=True)

# Usage:
# view = ExampleButtonView()
# await interaction.response.send_message('Click the button!', view=view)
'''

def generate_typescript_slash_command_example(language: str) -> str:
    """Generate example TypeScript/JavaScript slash command."""
    return f'''import {{ SlashCommandBuilder, ChatInputCommandInteraction }} from 'discord.js';

export const data = new SlashCommandBuilder()
    .setName('ping')
    .setDescription('Check bot latency');

export async function execute(interaction: ChatInputCommandInteraction) {{
    const latency = Math.round(interaction.client.ws.ping);
    await interaction.reply(`Pong! Latency: ${{latency}}ms`);
}}
'''

def generate_typescript_component_example(language: str) -> str:
    """Generate example TypeScript/JavaScript component."""
    return f'''import {{ ActionRowBuilder, ButtonBuilder, ButtonStyle, ChatInputCommandInteraction }} from 'discord.js';

export async function createExampleButton(interaction: ChatInputCommandInteraction) {{
    const row = new ActionRowBuilder<ButtonBuilder>()
        .addComponents(
            new ButtonBuilder()
                .setCustomId('example_button')
                .setLabel('Click Me!')
                .setStyle(ButtonStyle.Primary)
        );
    
    await interaction.reply({{ content: 'Click the button!', components: [row] }});
}}
'''

def validate_interaction_payload(payload: dict, interaction_type: int) -> dict:
    """Validate interaction payload against Discord API schema."""
    errors = []
    warnings = []
    
    # Interaction type validation
    valid_types = [1, 2, 3, 4, 5]  # PING, APPLICATION_COMMAND, MESSAGE_COMPONENT, APPLICATION_COMMAND_AUTOCOMPLETE, MODAL_SUBMIT
    if interaction_type not in valid_types:
        errors.append(f"Invalid interaction type: {interaction_type}. Must be one of {valid_types}")
    
    # Required fields
    required_fields = ["id", "application_id", "type", "version"]
    for field in required_fields:
        if field not in payload:
            errors.append(f"Missing required field: {field}")
    
    # Type-specific validation
    if interaction_type == 2:  # APPLICATION_COMMAND
        if "data" not in payload:
            errors.append("Missing 'data' field for APPLICATION_COMMAND interaction")
        elif "name" not in payload.get("data", {}):
            errors.append("Missing 'data.name' field for APPLICATION_COMMAND interaction")
    
    elif interaction_type == 3:  # MESSAGE_COMPONENT
        if "data" not in payload:
            errors.append("Missing 'data' field for MESSAGE_COMPONENT interaction")
        elif "custom_id" not in payload.get("data", {}):
            errors.append("Missing 'data.custom_id' field for MESSAGE_COMPONENT interaction")
    
    elif interaction_type == 5:  # MODAL_SUBMIT
        if "data" not in payload:
            errors.append("Missing 'data' field for MODAL_SUBMIT interaction")
        elif "custom_id" not in payload.get("data", {}):
            errors.append("Missing 'data.custom_id' field for MODAL_SUBMIT interaction")
    
    # Version check
    if payload.get("version") != 1:
        warnings.append(f"Interaction version is {payload.get('version')}, expected 1")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def check_bot_permissions(operations: list, current_permissions: str = None) -> dict:
    """Check if bot has required permissions for operations."""
    permission_map = {
        "send-messages": 0x0000000800,  # SEND_MESSAGES
        "read-messages": 0x0000000400,  # VIEW_CHANNEL
        "manage-messages": 0x0000002000,  # MANAGE_MESSAGES
        "manage-channels": 0x0000000010,  # MANAGE_CHANNELS
        "kick-members": 0x0000000002,  # KICK_MEMBERS
        "ban-members": 0x0000000004,  # BAN_MEMBERS
        "administrator": 0x0000000008,  # ADMINISTRATOR
        "manage-roles": 0x1000000000,  # MANAGE_ROLES
        "use-slash-commands": 0x0000000080000000,  # USE_APPLICATION_COMMANDS
    }
    
    required_permissions = 0
    for op in operations:
        if op in permission_map:
            required_permissions |= permission_map[op]
        else:
            return {
                "hasAllPermissions": False,
                "missingPermissions": [op],
                "error": f"Unknown operation: {op}"
            }
    
    missing = []
    if current_permissions:
        try:
            current_perm_int = int(current_permissions)
            for op in operations:
                perm_flag = permission_map.get(op)
                if perm_flag and not (current_perm_int & perm_flag):
                    missing.append(op)
        except ValueError:
            return {
                "hasAllPermissions": False,
                "missingPermissions": operations,
                "error": "Invalid permission integer format"
            }
    else:
        # If no current permissions provided, assume missing
        missing = operations
    
    return {
        "hasAllPermissions": len(missing) == 0,
        "missingPermissions": missing,
        "requiredPermissionInteger": str(required_permissions),
        "suggestedInviteURL": f"https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions={required_permissions}&scope=bot%20applications.commands"
    }

