# Game Bot Discord

A Discord bot that provides game information and completion times using the HowLongToBeat API. Meet Daoud - a bot with personality that I made for a server I share with my friend. Will get accurate data and has some fun features just for us.

## Tech Stack
- Discord API
- Custom HowLongToBeat API
- discord.py
- aiohttp
- python-dotenv

## Features

- **Game Lookup**: Search for any video game and get detailed information
- **Completion Times**: View main story, completionist, and all play styles timing data
- **Real-time Search**: Fast API integration with HowLongToBeat.com
- **Bot Personality**: Daoud has character and responds with personality
- **Message Monitoring**: Tracks message edits with fun responses
- **Interactive Commands**: Special commands with personal stories and references

### Command Prefix

The bot uses `.d ` as its command prefix. All commands can also be used as slash commands with `/`.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `.d howlongtobeat <game>` | Get completion times for any video game | `.d howlongtobeat Grand Theft Auto V` |
| `.d hello` | Get a friendly greeting from Daoud | `.d hello` |
| `.d iamwatching` | Daoud will reference your previous message | `.d iamwatching` |
| `.d godrick_incident` | Tell the legendary tale of the Godrick Incident | `.d godrick_incident` |
| `.d info` | Display all available commands and their descriptions | `.d info` |

## Example Usage

```
.d howlongtobeat The Witcher 3
```

Or using slash commands:
```
/howlongtobeat The Witcher 3
```

**Returns a rich embed with:**
- Game title and cover image
- Completion times for different play styles
- Developer and publisher information
- Platform availability
- User review score
- Game description

## Setup

### Prerequisites

- Python 3.8+
- Discord Bot Token
- Discord Server with appropriate permissions

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhinavChandra7020/howlongtobeat-discord-bot
   cd howlongtobeat-discord-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv myenv
   
   # Windows
   myenv\Scripts\activate
   
   # macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the root directory:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   GUILD_ID=your_primary_guild_id
   GUILD_ID2=your_secondary_guild_id (optional)
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Configuration

### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy the bot token to your `.env` file
4. Invite the bot to your server with these permissions:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History
   - Add Reactions
OR
   - Administrator
### Bot Permissions

The bot requires the following intents:
- `message_content` - To read message content
- `members` - To access member information
- Default intents for basic functionality