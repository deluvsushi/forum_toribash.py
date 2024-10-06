class DiscordName {
	constructor() {
		this.api = "https://api-v2.discord.name"
		this.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
			"Content-Type": "application/json"
		}
	}


	async getUserInfo(userId) {
		const response = await fetch(
			`${this.api}/graphql`, {
				method: "POST",
				body: JSON.stringify({
					operationName: "Discord",
					variables: {
						userId: userId
					},
					query: "query Discord($userId: String!) {\n  discord {\n    lookup(userId: $userId) {\n      user {\n        id\n        type\n        username\n        displayName\n        accountAge\n        createdAt\n        creationTimestamp\n        badges {\n          title\n          description\n          url\n          __typename\n        }\n        profileAppearance {\n          accentColor\n          avatar {\n            url\n            __typename\n          }\n          avatarDecoration\n          banner {\n            url\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
				}),
				headers: this.headers
			})
		return JSON.stringify(await response.json())
	}
}

module.exports = {DiscordName}
