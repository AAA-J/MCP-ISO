# Discord Developer Documentation

Comprehensive reference guide for Discord API documentation links, organized for building Discord MCP servers.

## Table of Contents

1. [Core API Reference](#core-api-reference)
2. [Interactions](#interactions)
3. [Components](#components)
4. [Activities](#activities)
5. [Discord Social SDK](#discord-social-sdk)
6. [Rich Presence](#rich-presence)
7. [Monetization](#monetization)
8. [Discovery](#discovery)
9. [Events](#events)
10. [Developer Tools](#developer-tools)
11. [Change Log](#change-log)
12. [Resources](#resources)
13. [Topics](#topics)
14. [Tutorials](#tutorials)
15. [Policies](#policies)

---

## Core API Reference

### API Reference
- [API Reference](https://discord.com/developers/docs/reference) - Complete Discord API reference documentation

---

## Interactions

### Overview
- [Interaction Overview](https://discord.com/developers/docs/interactions/overview) - Introduction to Discord interactions

### Receiving and Responding
- [Receiving and Responding](https://discord.com/developers/docs/interactions/receiving-and-responding) - How to receive and respond to interactions

### Application Commands
- [Application Commands](https://discord.com/developers/docs/interactions/application-commands) - Creating and managing application commands (slash commands)

---

## Components

### Overview
- [Components Overview](https://discord.com/developers/docs/components/overview) - Introduction to Discord message components

### Using Components
- [Using Message Components](https://discord.com/developers/docs/components/using-message-components) - Implementing interactive message components
- [Using Modal Components](https://discord.com/developers/docs/components/using-modal-components) - Creating and handling modal dialogs

### Reference
- [Component Reference](https://discord.com/developers/docs/components/reference) - Complete component API reference

---

## Activities

### Overview
- [Activities Overview](https://discord.com/developers/docs/activities/overview) - Introduction to Discord Activities
- [How Activities Work](https://discord.com/developers/docs/activities/how-activities-work) - Understanding the Activities system

### Quick Start
- [Building an Activity](https://discord.com/developers/docs/activities/building-an-activity) - Quick start guide for building activities

### Development Guides
- [Development Guides](https://discord.com/developers/docs/activities/development-guides) - Main development guides index
- [Local Development](https://discord.com/developers/docs/activities/development-guides/local-development#run-your-application-locally) - Running your application locally
- [User Actions](https://discord.com/developers/docs/activities/development-guides/user-actions) - Implementing user actions in activities
- [Mobile Development](https://discord.com/developers/docs/activities/development-guides/mobile) - Mobile-specific development guidance
- [Layout](https://discord.com/developers/docs/activities/development-guides/layout) - Designing activity layouts
- [Networking](https://discord.com/developers/docs/activities/development-guides/networking) - Networking in activities
- [Multiplayer Experience](https://discord.com/developers/docs/activities/development-guides/multiplayer-experience) - Building multiplayer activities
- [Growth and Referrals](https://discord.com/developers/docs/activities/development-guides/growth-and-referrals) - Promoting and growing your activity
- [Assets and Metadata](https://discord.com/developers/docs/activities/development-guides/assets-and-metadata) - Managing activity assets and metadata
- [Production Readiness](https://discord.com/developers/docs/activities/development-guides/production-readiness) - Preparing for production deployment

### Design Patterns
- [Design Patterns](https://discord.com/developers/docs/activities/design-patterns) - Best practices and design patterns for activities

---

## Discord Social SDK

### Overview
- [Social SDK Overview](https://discord.com/developers/docs/discord-social-sdk/overview) - Introduction to the Discord Social SDK

### Core Concepts
- [Core Concepts](https://discord.com/developers/docs/discord-social-sdk/core-concepts) - Fundamental concepts of the Social SDK
- [Core Features](https://discord.com/developers/docs/discord-social-sdk/core-concepts/core-features) - Key features available in the Social SDK
- [Communication Features](https://discord.com/developers/docs/discord-social-sdk/core-concepts/communication-features) - Messaging and communication capabilities
- [Integration Overview](https://discord.com/developers/docs/discord-social-sdk/core-concepts/integration-overview) - How to integrate the Social SDK
- [Platform Compatibility](https://discord.com/developers/docs/discord-social-sdk/core-concepts/platform-compatibility) - Supported platforms and compatibility
- [OAuth2 Scopes](https://discord.com/developers/docs/discord-social-sdk/core-concepts/oauth2-scopes) - Required OAuth2 scopes for Social SDK

### Getting Started
- [Getting Started](https://discord.com/developers/docs/discord-social-sdk/getting-started) - Quick start guide
- [Using C++](https://discord.com/developers/docs/discord-social-sdk/getting-started/using-c++) - Getting started with C++
- [Using Unity](https://discord.com/developers/docs/discord-social-sdk/getting-started/using-unity) - Getting started with Unity
- [Using Unreal Engine](https://discord.com/developers/docs/discord-social-sdk/getting-started/using-unreal-engine) - Getting started with Unreal Engine

### Development Guides
- [Development Guides](https://discord.com/developers/docs/discord-social-sdk/development-guides) - Main development guides index
- [Account Linking with Discord](https://discord.com/developers/docs/discord-social-sdk/development-guides/account-linking-with-discord) - Linking user accounts
- [Account Linking on Consoles](https://discord.com/developers/docs/discord-social-sdk/development-guides/account-linking-on-consoles) - Console-specific account linking
- [Using Provisional Accounts](https://discord.com/developers/docs/discord-social-sdk/development-guides/using-provisional-accounts) - Working with provisional accounts
- [Creating a Unified Friends List](https://discord.com/developers/docs/discord-social-sdk/development-guides/creating-a-unified-friends-list) - Building unified friends lists
- [Managing Relationships](https://discord.com/developers/docs/discord-social-sdk/development-guides/managing-relationships) - Managing user relationships
- [Setting Rich Presence](https://discord.com/developers/docs/discord-social-sdk/development-guides/setting-rich-presence) - Implementing rich presence
- [Managing Game Invites](https://discord.com/developers/docs/discord-social-sdk/development-guides/managing-game-invites) - Handling game invitations
- [Sending Direct Messages](https://discord.com/developers/docs/discord-social-sdk/development-guides/sending-direct-messages) - Sending DMs through the SDK
- [Managing Lobbies](https://discord.com/developers/docs/discord-social-sdk/development-guides/managing-lobbies) - Creating and managing game lobbies
- [Linked Channels](https://discord.com/developers/docs/discord-social-sdk/development-guides/linked-channels) - Working with linked channels
- [Managing Voice Chat](https://discord.com/developers/docs/discord-social-sdk/development-guides/managing-voice-chat) - Voice chat integration

### Design Guidelines
- [Design Guidelines](https://discord.com/developers/docs/discord-social-sdk/design-guidelines) - UI/UX design guidelines
- [Principles](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/principles) - Core design principles
- [Signing In](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/signing-in) - Sign-in flow design
- [Connection Points](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/connection-points) - Where to place connection UI
- [Branding Guidelines](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/branding-guidelines) - Branding requirements
- [Unified Friends List](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/unified-friends-list) - Friends list UI guidelines
- [Direct Messages](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/direct-messages) - DM interface design
- [Chat History](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/chat-history) - Chat history UI patterns
- [Social Settings](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/social-settings) - Settings UI guidelines
- [Provisional Accounts](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/provisional-accounts) - Provisional account UI
- [Status & Rich Presence](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/status-rich-presence) - Status and presence UI
- [Consoles](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/consoles) - Console-specific design guidelines
- [Game Friends](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/game-friends) - In-game friends UI
- [Linked Channels](https://discord.com/developers/docs/discord-social-sdk/design-guidelines/linked-channels) - Linked channels UI design

### How-To Guides
- [How-To Guides](https://discord.com/developers/docs/discord-social-sdk/how-to) - Practical how-to guides
- [Debug & Log](https://discord.com/developers/docs/discord-social-sdk/how-to/debug-log) - Debugging and logging
- [Use with Discord APIs](https://discord.com/developers/docs/discord-social-sdk/how-to/use-with-discord-apis) - Integrating with Discord APIs
- [Integrate Moderation](https://discord.com/developers/docs/discord-social-sdk/how-to/integrate-moderation) - Adding moderation features
- [Market Your Integration](https://discord.com/developers/docs/discord-social-sdk/how-to/market-your-integration) - Marketing your integration
- [Handle Special Characters in Display Names](https://discord.com/developers/docs/discord-social-sdk/how-to/handle-special-characters-display-names) - Display name handling

### Reference
- [Social SDK Reference](https://discord.com/developers/docs/social-sdk/index.html) - Complete Social SDK API reference

---

## Rich Presence

### Overview
- [Rich Presence Overview](https://discord.com/developers/docs/rich-presence/overview) - Introduction to Rich Presence

### Implementation
- [Using with Embedded App SDK](https://discord.com/developers/docs/rich-presence/using-with-the-embedded-app-sdk) - Rich Presence with Embedded App SDK
- [Using with Discord Social SDK](https://discord.com/developers/docs/rich-presence/using-with-the-discord-social-sdk) - Rich Presence with Social SDK

### Best Practices
- [Best Practices](https://discord.com/developers/docs/rich-presence/best-practices) - Rich Presence best practices and guidelines

---

## Monetization

### Overview
- [Monetization Overview](https://discord.com/developers/docs/monetization/overview) - Introduction to Discord monetization

### Setup
- [Enabling Monetization](https://discord.com/developers/docs/monetization/enabling-monetization) - How to enable monetization for your app
- [Managing SKUs](https://discord.com/developers/docs/monetization/managing-skus) - Creating and managing SKUs

### Implementation
- [Implementing App Subscriptions](https://discord.com/developers/docs/monetization/implementing-app-subscriptions) - Adding subscription support
- [Implementing One-Time Purchases](https://discord.com/developers/docs/monetization/implementing-one-time-purchases) - Adding one-time purchase support
- [Implementing IAP for Activities](https://discord.com/developers/docs/monetization/implementing-iap-for-activities) - In-app purchases for Activities

---

## Discovery

### Overview
- [Discovery Overview](https://discord.com/developers/docs/discovery/overview) - Introduction to Discord Discovery

### Setup
- [Enabling Discovery](https://discord.com/developers/docs/discovery/enabling-discovery) - How to enable Discovery for your app

### Best Practices
- [Best Practices](https://discord.com/developers/docs/discovery/best-practices) - Discovery best practices

---

## Events

### Overview
- [Events Overview](https://discord.com/developers/docs/events/overview) - Introduction to Discord events system

### Gateway
- [Using Gateway](https://discord.com/developers/docs/events/gateway) - Discord Gateway documentation
- [Gateway Events](https://discord.com/developers/docs/events/gateway-events) - All Gateway event types

### Webhooks
- [Webhook Events](https://discord.com/developers/docs/events/webhook-events) - Webhook event types

---

## Developer Tools

### SDKs
- [Embedded App SDK](https://discord.com/developers/docs/developer-tools/embedded-app-sdk) - Discord Embedded App SDK documentation

### Resources
- [Community Resources](https://discord.com/developers/docs/developer-tools/community-resources) - Community tools and resources

---

## Change Log

- [Change Log](https://discord.com/developers/docs/change-log) - Discord API change log and version history

---

## Resources

Complete API resource references for Discord objects:

- [Application Role Connection Metadata](https://discord.com/developers/docs/resources/application-role-connection-metadata) - Role connection metadata
- [Application](https://discord.com/developers/docs/resources/application) - Application object reference
- [Audit Log](https://discord.com/developers/docs/resources/audit-log) - Audit log entries
- [Auto Moderation](https://discord.com/developers/docs/resources/auto-moderation) - Auto moderation rules
- [Channel](https://discord.com/developers/docs/resources/channel) - Channel object reference
- [Emoji](https://discord.com/developers/docs/resources/emoji) - Emoji object reference
- [Entitlement](https://discord.com/developers/docs/resources/entitlement) - Entitlement object reference
- [Guild Scheduled Event](https://discord.com/developers/docs/resources/guild-scheduled-event) - Scheduled event reference
- [Guild Template](https://discord.com/developers/docs/resources/guild-template) - Guild template reference
- [Guild](https://discord.com/developers/docs/resources/guild) - Guild (server) object reference
- [Invite](https://discord.com/developers/docs/resources/invite) - Invite object reference
- [Lobby](https://discord.com/developers/docs/resources/lobby) - Lobby object reference
- [Message](https://discord.com/developers/docs/resources/message) - Message object reference
- [Poll](https://discord.com/developers/docs/resources/poll) - Poll object reference
- [SKU](https://discord.com/developers/docs/resources/sku) - SKU object reference
- [Soundboard](https://discord.com/developers/docs/resources/soundboard) - Soundboard sound reference
- [Stage Instance](https://discord.com/developers/docs/resources/stage-instance) - Stage instance reference
- [Sticker](https://discord.com/developers/docs/resources/sticker) - Sticker object reference
- [Subscription](https://discord.com/developers/docs/resources/subscription) - Subscription object reference
- [User](https://discord.com/developers/docs/resources/user) - User object reference
- [Voice](https://discord.com/developers/docs/resources/voice) - Voice state reference
- [Webhook](https://discord.com/developers/docs/resources/webhook) - Webhook object reference

---

## Topics

### Certified Devices
- [Certified Devices](https://discord.com/developers/docs/topics/certified-devices) - Discord certified device requirements

### OAuth2
- [OAuth2](https://discord.com/developers/docs/topics/oauth2) - OAuth2 authentication and authorization

### Opcodes and Status Codes
- [Opcodes and Status Codes](https://discord.com/developers/docs/topics/opcodes-and-status-codes) - Gateway opcodes and HTTP status codes

### Permissions
- [Permissions](https://discord.com/developers/docs/topics/permissions) - Permission system and bitwise flags

### Rate Limits
- [Rate Limits](https://discord.com/developers/docs/topics/rate-limits) - API rate limiting documentation

### RPC
- [RPC](https://discord.com/developers/docs/topics/rpc) - Rich Presence RPC documentation

### Teams
- [Teams](https://discord.com/developers/docs/topics/teams) - Developer team management

### Threads
- [Threads](https://discord.com/developers/docs/topics/threads) - Thread channel documentation

### Voice Connections
- [Voice Connections](https://discord.com/developers/docs/topics/voice-connections) - Voice connection documentation

---

## Tutorials

- [Configuring App Metadata for Linked Roles](https://discord.com/developers/docs/tutorials/configuring-app-metadata-for-linked-roles) - Setting up linked roles
- [Developing a User-Installable App](https://discord.com/developers/docs/tutorials/developing-a-user-installable-app) - Creating installable apps
- [Hosting on Cloudflare Workers](https://discord.com/developers/docs/tutorials/hosting-on-cloudflare-workers) - Deploying to Cloudflare Workers
- [Upgrading to Application Commands](https://discord.com/developers/docs/tutorials/upgrading-to-application-commands) - Migrating to slash commands

---

## Policies

### Developer Policy
- [Developer Policy](https://support-dev.discord.com/hc/articles/8563934450327-Discord-Developer-Policy) - Discord Developer Policy

### Terms of Service
- [Developer Terms of Service](https://support-dev.discord.com/hc/articles/8562894815383-Discord-Developer-Terms-of-Service) - Discord Developer Terms of Service

---

## Notes

This documentation is organized for easy reference when building Discord MCP servers. All links point to the official Discord Developer Documentation.

For the most up-to-date information, always refer to the official Discord Developer Portal: https://discord.com/developers/docs

