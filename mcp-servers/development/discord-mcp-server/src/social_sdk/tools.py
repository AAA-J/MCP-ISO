"""Tools for building Discord Social SDK integrations."""

from mcp.types import Tool, TextContent
import json

social_sdk_tools = [
    Tool(
        name="discord_generate_sdk_init",
        description="Generate SDK initialization code for Discord Social SDK",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["c++", "unity", "unreal", "csharp"],
                    "description": "Target platform/language"
                },
                "features": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["account-linking", "rich-presence", "friends-list", "lobbies", "voice-chat"]
                    },
                    "description": "SDK features to initialize"
                },
                "clientId": {
                    "type": "string",
                    "description": "Discord application client ID"
                }
            },
            "required": ["platform", "features"]
        }
    ),
    Tool(
        name="discord_create_account_linking",
        description="Generate account linking implementation code",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["c++", "unity", "unreal"]
                },
                "useProvisionalAccounts": {
                    "type": "boolean",
                    "default": False
                }
            },
            "required": ["platform"]
        }
    ),
    Tool(
        name="discord_generate_rich_presence",
        description="Generate rich presence implementation code",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["c++", "unity", "unreal", "csharp"]
                },
                "presenceType": {
                    "type": "string",
                    "enum": ["game", "streaming", "listening", "watching"],
                    "default": "game"
                }
            },
            "required": ["platform"]
        }
    ),
    Tool(
        name="discord_validate_oauth_scopes",
        description="Validate OAuth2 scopes for a specific use case",
        inputSchema={
            "type": "object",
            "properties": {
                "useCase": {
                    "type": "string",
                    "enum": ["social-sdk-basic", "social-sdk-full", "bot-basic"],
                    "description": "Use case type"
                },
                "providedScopes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["useCase"]
        }
    ),
]

async def handle_social_sdk(name: str, arguments: dict) -> list[TextContent]:
    """Handle Discord Social SDK tool calls."""
    if name == "discord_generate_sdk_init":
        platform = arguments.get("platform")
        features = arguments.get("features", [])
        client_id = arguments.get("clientId", "YOUR_CLIENT_ID")
        
        result = {
            "success": True,
            "platform": platform,
            "features": features,
            "clientId": client_id,
            "code": generate_sdk_init_code(platform, features, client_id),
            "files": generate_sdk_files(platform, features, client_id)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_create_account_linking":
        platform = arguments.get("platform")
        use_provisional = arguments.get("useProvisionalAccounts", False)
        code = generate_account_linking_code(platform, use_provisional)
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_rich_presence":
        platform = arguments.get("platform")
        presence_type = arguments.get("presenceType", "game")
        code = generate_rich_presence_code(platform, presence_type)
        return [TextContent(type="text", text=code)]
    elif name == "discord_validate_oauth_scopes":
        use_case = arguments.get("useCase")
        provided_scopes = arguments.get("providedScopes", [])
        result = validate_oauth_scopes(use_case, provided_scopes)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown Discord Social SDK tool: {name}")

def generate_sdk_init_code(platform: str, features: list, client_id: str) -> str:
    """Generate SDK initialization code."""
    if platform == "unity":
        return generate_unity_sdk_init(features, client_id)
    elif platform == "c++":
        return generate_cpp_sdk_init(features, client_id)
    elif platform == "unreal":
        return generate_unreal_sdk_init(features, client_id)
    elif platform == "csharp":
        return generate_csharp_sdk_init(features, client_id)
    else:
        return f"# {platform} SDK initialization code"

def generate_sdk_files(platform: str, features: list, client_id: str) -> dict:
    """Generate SDK file structure."""
    files = {}
    
    if platform == "unity":
        files["DiscordManager.cs"] = generate_unity_sdk_init(features, client_id)
        if "account-linking" in features:
            files["AccountLinking.cs"] = generate_account_linking_code("unity", False)
        if "rich-presence" in features:
            files["RichPresence.cs"] = generate_rich_presence_code("unity", "game")
        if "friends-list" in features:
            files["FriendsManager.cs"] = generate_friends_list_code("unity")
        if "lobbies" in features:
            files["LobbyManager.cs"] = generate_lobby_code("unity")
    
    elif platform == "c++":
        files["discord_sdk.cpp"] = generate_cpp_sdk_init(features, client_id)
        files["discord_sdk.h"] = generate_cpp_header()
        if "rich-presence" in features:
            files["rich_presence.cpp"] = generate_rich_presence_code("c++", "game")
    
    elif platform == "unreal":
        files["DiscordManager.h"] = generate_unreal_header()
        files["DiscordManager.cpp"] = generate_unreal_sdk_init(features, client_id)
    
    return files

def generate_unity_sdk_init(features: list, client_id: str) -> str:
    """Generate Unity SDK initialization."""
    code = f'''using Discord;
using UnityEngine;

public class DiscordManager : MonoBehaviour
{{
    public Discord.Discord discord;
    private const long CLIENT_ID = {client_id}L;
'''
    
    if "rich-presence" in features:
        code += "    private ActivityManager activityManager;\n"
    if "friends-list" in features:
        code += "    private RelationshipManager relationshipManager;\n"
    if "lobbies" in features:
        code += "    private LobbyManager lobbyManager;\n"
    if "voice-chat" in features:
        code += "    private VoiceManager voiceManager;\n"
    
    code += '''
    void Start()
    {
        try
        {
            discord = new Discord.Discord(CLIENT_ID, (System.UInt64)CreateFlags.Default);
'''
    
    if "rich-presence" in features:
        code += "            activityManager = discord.GetActivityManager();\n"
    if "friends-list" in features:
        code += "            relationshipManager = discord.GetRelationshipManager();\n"
    if "lobbies" in features:
        code += "            lobbyManager = discord.GetLobbyManager();\n"
    if "voice-chat" in features:
        code += "            voiceManager = discord.GetVoiceManager();\n"
    
    code += '''        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to initialize Discord SDK: {e.Message}");
        }
    }

    void Update()
    {
        try
        {
            discord?.RunCallbacks();
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Discord SDK callback error: {e.Message}");
        }
    }

    void OnDestroy()
    {
        discord?.Dispose();
    }
}
'''
    return code

def generate_cpp_sdk_init(features: list, client_id: str) -> str:
    """Generate C++ SDK initialization."""
    code = f'''#include "discord_sdk.h"
#include <iostream>

DiscordManager::DiscordManager() {{
    discord::Core* core{{}};
    auto result = discord::Core::Create({client_id}L, DiscordCreateFlags_Default, &core);
    
    if (result != discord::Result::Ok) {{
        std::cerr << "Failed to create Discord core: " << static_cast<int>(result) << std::endl;
        return;
    }}
    
    core_ = std::unique_ptr<discord::Core>{{{{core}}}};
'''
    
    if "rich-presence" in features:
        code += "    activity_manager_ = core_->ActivityManager();\n"
    if "friends-list" in features:
        code += "    relationship_manager_ = core_->RelationshipManager();\n"
    if "lobbies" in features:
        code += "    lobby_manager_ = core_->LobbyManager();\n"
    if "voice-chat" in features:
        code += "    voice_manager_ = core_->VoiceManager();\n"
    
    code += '''}

void DiscordManager::Update() {
    if (core_) {
        core_->RunCallbacks();
    }
}

DiscordManager::~DiscordManager() {
    core_.reset();
}
'''
    return code

def generate_cpp_header() -> str:
    """Generate C++ header file."""
    return '''#ifndef DISCORD_SDK_H
#define DISCORD_SDK_H

#include <discord.h>
#include <memory>

class DiscordManager {
public:
    DiscordManager();
    ~DiscordManager();
    void Update();
    
    discord::ActivityManager* GetActivityManager() { return activity_manager_; }
    discord::RelationshipManager* GetRelationshipManager() { return relationship_manager_; }
    discord::LobbyManager* GetLobbyManager() { return lobby_manager_; }
    discord::VoiceManager* GetVoiceManager() { return voice_manager_; }

private:
    std::unique_ptr<discord::Core> core_;
    discord::ActivityManager* activity_manager_ = nullptr;
    discord::RelationshipManager* relationship_manager_ = nullptr;
    discord::LobbyManager* lobby_manager_ = nullptr;
    discord::VoiceManager* voice_manager_ = nullptr;
};

#endif // DISCORD_SDK_H
'''

def generate_unreal_sdk_init(features: list, client_id: str) -> str:
    """Generate Unreal Engine SDK initialization."""
    return f'''#include "DiscordManager.h"
#include "Discord.h"

void ADiscordManager::BeginPlay()
{{
    Super::BeginPlay();
    
    discord::Core* core{{}};
    auto result = discord::Core::Create({client_id}L, DiscordCreateFlags_Default, &core);
    
    if (result != discord::Result::Ok) {{
        UE_LOG(LogTemp, Error, TEXT("Failed to create Discord core"));
        return;
    }}
    
    Core = MakeUnique<discord::Core>(core);
    
    if (Core.IsValid()) {{
        ActivityManager = Core->ActivityManager();
        RelationshipManager = Core->RelationshipManager();
    }}
}}

void ADiscordManager::Tick(float DeltaTime)
{{
    Super::Tick(DeltaTime);
    
    if (Core.IsValid()) {{
        Core->RunCallbacks();
    }}
}}
'''

def generate_unreal_header() -> str:
    """Generate Unreal Engine header."""
    return '''#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Discord.h"
#include "DiscordManager.generated.h"

UCLASS()
class YOURGAME_API ADiscordManager : public AActor
{
    GENERATED_BODY()

public:
    ADiscordManager();
    
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

    discord::ActivityManager* GetActivityManager() const { return ActivityManager; }
    discord::RelationshipManager* GetRelationshipManager() const { return RelationshipManager; }

private:
    TUniquePtr<discord::Core> Core;
    discord::ActivityManager* ActivityManager = nullptr;
    discord::RelationshipManager* RelationshipManager = nullptr;
};
'''

def generate_csharp_sdk_init(features: list, client_id: str) -> str:
    """Generate C# SDK initialization."""
    code = f'''using Discord;

public class DiscordSDKManager
{{
    private Discord.Discord discord;
    private const long CLIENT_ID = {client_id}L;
'''
    
    if "rich-presence" in features:
        code += "    private ActivityManager activityManager;\n"
    if "friends-list" in features:
        code += "    private RelationshipManager relationshipManager;\n"
    
    code += f'''
    public void Initialize()
    {{
        try
        {{
            discord = new Discord.Discord(CLIENT_ID, (ulong)CreateFlags.Default);
'''
    
    if "rich-presence" in features:
        code += "            activityManager = discord.GetActivityManager();\n"
    if "friends-list" in features:
        code += "            relationshipManager = discord.GetRelationshipManager();\n"
    
    code += '''        }
        catch (Exception e)
        {
            Console.WriteLine($"Failed to initialize Discord SDK: {e.Message}");
        }
    }

    public void Update()
    {
        try
        {
            discord?.RunCallbacks();
        }
        catch (Exception e)
        {
            Console.WriteLine($"Discord SDK callback error: {e.Message}");
        }
    }

    public void Dispose()
    {
        discord?.Dispose();
    }
}
'''
    return code

def generate_account_linking_code(platform: str, use_provisional: bool) -> str:
    """Generate account linking code."""
    if platform == "unity":
        return f'''using Discord;
using UnityEngine;

public class AccountLinking : MonoBehaviour
{{
    private DiscordManager discordManager;
    
    void Start()
    {{
        discordManager = FindObjectOfType<DiscordManager>();
    }}
    
    public void LinkAccount()
    {{
        var oauth2 = discordManager.discord.GetOAuth2Manager();
        
        oauth2.GetAccessToken((result, accessToken) =>
        {{
            if (result == Result.Ok)
            {{
                // Store access token securely
                PlayerPrefs.SetString("discord_access_token", accessToken);
                Debug.Log("Account linked successfully!");
            }}
            else
            {{
                Debug.LogError($"Failed to link account: {{result}}");
            }}
        }});
    }}
    
    {"// Provisional account support enabled" if use_provisional else "// Standard account linking"}
}}
'''
    elif platform == "c++":
        return f'''#include "account_linking.h"
#include <iostream>

void AccountLinking::LinkAccount() {{
    auto oauth2 = core_->OAuth2Manager();
    
    oauth2->GetAccessToken([](discord::Result result, discord::OAuth2Token token) {{
        if (result == discord::Result::Ok) {{
            // Store access token securely
            std::cout << "Account linked successfully!" << std::endl;
        }} else {{
            std::cerr << "Failed to link account: " << static_cast<int>(result) << std::endl;
        }}
    }});
}}
'''
    else:
        return f"# Account linking code for {platform}\n# Provisional accounts: {use_provisional}"

def generate_rich_presence_code(platform: str, presence_type: str) -> str:
    """Generate rich presence code."""
    if platform == "unity":
        return f'''using Discord;
using UnityEngine;

public class RichPresence : MonoBehaviour
{{
    private ActivityManager activityManager;
    
    public void SetRichPresence(string details, string state)
    {{
        var activity = new Activity
        {{
            Details = details,
            State = state,
            Assets = {{
                LargeImage = "game_logo",
                LargeText = "Playing Game"
            }},
            Timestamps = {{
                Start = System.DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            }}
        }};
        
        activityManager.UpdateActivity(activity, (result) =>
        {{
            if (result == Result.Ok)
            {{
                Debug.Log("Rich presence updated!");
            }}
        }});
    }}
    
    // Presence type: {presence_type}
}}
'''
    elif platform == "c++":
        return f'''#include "rich_presence.h"

void RichPresence::UpdatePresence(const std::string& details, const std::string& state) {{
    discord::Activity activity{{}};
    activity.SetDetails(details.c_str());
    activity.SetState(state.c_str());
    
    discord::ActivityAssets assets{{}};
    assets.SetLargeImage("game_logo");
    assets.SetLargeText("Playing Game");
    activity.SetAssets(assets);
    
    activity.GetTimestamps().SetStart(std::time(nullptr));
    
    activity_manager_->UpdateActivity(activity, [](discord::Result result) {{
        if (result == discord::Result::Ok) {{
            std::cout << "Rich presence updated!" << std::endl;
        }}
    }});
}}
'''
    else:
        return f"# Rich presence code for {platform}\n# Type: {presence_type}"

def generate_friends_list_code(platform: str) -> str:
    """Generate friends list code."""
    if platform == "unity":
        return '''using Discord;
using System.Collections.Generic;

public class FriendsManager
{
    private RelationshipManager relationshipManager;
    private List<Relationship> friends = new List<Relationship>();
    
    public void RefreshFriends()
    {
        relationshipManager.OnRefresh += () =>
        {
            relationshipManager.Filter((relationship) =>
            {
                return relationship.Type == RelationshipType.Friend;
            });
            
            relationshipManager.OnRelationshipUpdate += (relationship) =>
            {
                if (relationship.Type == RelationshipType.Friend)
                {
                    friends.Add(relationship);
                }
            };
        };
        
        relationshipManager.Refresh();
    }
    
    public List<Relationship> GetFriends()
    {
        return friends;
    }
}
'''
    else:
        return f"# Friends list code for {platform}"

def generate_lobby_code(platform: str) -> str:
    """Generate lobby code."""
    if platform == "unity":
        return '''using Discord;

public class LobbyManager
{
    private LobbyManager lobbyManager;
    
    public void CreateLobby(int capacity, LobbyType type)
    {
        var transaction = lobbyManager.GetLobbyCreateTransaction();
        transaction.SetCapacity((uint)capacity);
        transaction.SetType(type);
        
        lobbyManager.CreateLobby(transaction, (result, lobby) =>
        {
            if (result == Result.Ok)
            {
                Debug.Log($"Lobby created: {lobby.Id}");
            }
        });
    }
    
    public void JoinLobby(long lobbyId, string secret)
    {
        lobbyManager.ConnectLobby(lobbyId, secret, (result, lobby) =>
        {
            if (result == Result.Ok)
            {
                Debug.Log($"Joined lobby: {lobby.Id}");
            }
        });
    }
}
'''
    else:
        return f"# Lobby code for {platform}"

def validate_oauth_scopes(use_case: str, provided_scopes: list) -> dict:
    """Validate OAuth2 scopes."""
    scope_requirements = {
        "social-sdk-basic": ["identify", "rpc"],
        "social-sdk-full": ["identify", "rpc", "rpc.activities.write", "rpc.voice.write", "rpc.notifications.read"],
        "bot-basic": ["bot", "applications.commands"],
        "bot-full": ["bot", "applications.commands", "guilds", "guilds.members.read"],
        "account-linking": ["identify", "email"],
        "rich-presence": ["rpc", "rpc.activities.write"]
    }
    
    required_scopes = scope_requirements.get(use_case, [])
    missing_scopes = [scope for scope in required_scopes if scope not in provided_scopes]
    
    return {
        "valid": len(missing_scopes) == 0,
        "useCase": use_case,
        "requiredScopes": required_scopes,
        "providedScopes": provided_scopes,
        "missingScopes": missing_scopes,
        "oauthUrl": f"https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope={'%20'.join(required_scopes)}&response_type=code&redirect_uri=YOUR_REDIRECT_URI"
    }

