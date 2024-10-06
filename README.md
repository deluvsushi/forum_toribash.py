# discord_name.js
Web-API for [discord.name](https://discord.name/) website which is used to get discord user account info by id

## Example
```JavaScript
async function main() {
	const { DiscordName } = require("./discord_name.js")
	const discordName = new DiscordName()
	const userInfo = await discordName.getUserInfo("userId")
	console.log(userInfo)
}

main()
```
