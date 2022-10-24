import requests
from hashlib import md5
from html_to_json import convert

class ForumToribash:
	def __init__(self):
		self.api = "https://forum.toribash.com"
		self.recaptcha_api = "https://www.google.com/recaptcha/api2"
		self.user_id = None
		self.tb5_password = None
		self.tb5_session_hash = None
		self.headers = {
			"accept": "application/json",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
			"cookie": f"tb5sessionhash={self.tb5_session_hash}; tb5userid={self.user_id}; tb5password={self.tb5_password}"
		}
	
	def md5hash(self, string: str):
		return md5(string.encode()).hexdigest()

	def generate_captcha(
			self,
			hl: str = "en",
			vh: int = 1080739656,
			cb: str = "yqzvhrcuefd",
			chr: str = "[97,54,75]",
			v: str = "PRMRaAwB3KlylGQR57Dyk-pF",
			key: str = "6LfTeLkUAAAAAFXarNTDL29B5TJoMmvtADlvilA7",
			co: str = "aHR0cHM6Ly9mb3J1bS50b3JpYmFzaC5jb206NDQz",
			bg: str = "!vbugu74KAAQVHCQMbQEHDwJliyi_1YCin_bisYSgvOK-_oSWYd-CVRtB_IoKv1xL4XhGFCUVFbA8AdYR8zp8H0o87SEuvBRoEZqbHG51z2qcDbRQtJz-gSWU0FqJC7PbYnMaPu7V3guQWSx7MnutKGkcR6AGPE6-oNh5e448w67CDud6EnmyeeCxfK-4sLDl8kXBgnZQefz-RsnicYe3gaD8gGmhq7rFPHiw78zA1Qkl9_H4i1tLgzapnluB_grL8yzpGMLXx3Wh37E0OmjWivHZlmQIxnKm9sRU-IYhQbFkwyi0jDBsX9Etn_YKb0mnrHQSg770XyEyIpSW7RCjWR-p1AjA-g_iL5QI7QeMuL4WmNyYhrN4BsQR5hLD5kPUyno3J5dvfYjxOiEiESNF81oyK8gWZZJ1kEcc2zJ0UtjBR4F0jmbauD5ZII2Z1UbNVooGTe4ydmUNHfUCbqmJ1HRirPuqCXDU868gi9deYB83grzG1c_S9KbUt74zilNn6See0MQs2qXIDGZzZQUwkLE5Xg617COHODV14GNc22eg_Ctj1jlE9SbOcUhdVVKy1-AbH-gpCD9BzsbmLibCQl6uaMYthuqkqLCDDjvmjpo-iIcPNauq29djP6muvQoPqQ1HNBMdV0Y5P64TrfGLenU8zirLIM2k0XnbfoY_iTDyVw763qDhKGy-I3O-k8-VPGTXKWyS5wah9brnPQ9nKPjufsBvxIyDjzUYsK1I0dZfiUoVYTconHc-OH7yXQxjlWseGkrnYjLqjFZIInwVbj0dWozXVhE8-1kLyFDpMdDDY4da1oSAGq2oJKbFDSrqzLJPf98DQJwAT9jTM0rdk9i9ZrIaLP2Eihx2CNJw8SUVe8yHp0mb13Kel3-oLqtMYay2iO2P8XYQplvH1165et2NBgGkRUCTpMd7l-9979U8w93TjUGoxok*",
			parameters: str = "v={v}&reason=q&c=<token>&k={key}&co={co}&hl={hl}&size=invisible&chr={chr}&vh={vh}&bg={bg}"):
		anchor = requests.get(
				f"{self.recaptcha_api}/anchor?ar=1&k={key}&co={co}&hl={hl}&v={v}&size=invisible&cb={cb}",
				headers=self.headers).text
		recaptcha_token = anchor.split(
				'recaptcha-token" value="')[1].split('">')[0]
		data = parameters.replace("<token>", recaptcha_token)
		self.headers["content-type"] = "application/x-www-form-urlencoded"
		response = requests.post(
			f"{self.recaptcha_api}/reload?k={key}",
			data=data,
			headers=self.headers).text
		return response.split(
				'"rresp","'
			)[1].split('"')[0] if "rresp" in response else response

	def register(
			self,
			email: str,
			username: str,
			password: str,
			tos: str = "on"):
		data = {
			"email": email,
			"username": username,
			"password": password,
			"c_password": password,
			"tos": tos,
			"action": "register",
			"g-recaptcha-response": self.generate_captcha()
		}
		return convert(
			requests.post(
				f"{self.api}/tori_register.php",
				data=data,
				headers=self.headers).text)

	def login(self, username: str, password: str):
		data = {
			"vb_login_username": username,
			"vb_login_password": password,
			"vb_login_md5password": self.md5hash(password),
			"vb_login_md5password_utf": self.md5hash(password),
			"cookieuser": 1,
			"do": "login",
			"securitytoken": "guest",
			"format": "json"
		}
		response = requests.post(
			f"{self.api}/login.php?do=login",
			data=data,
			headers=self.headers)
		cookies = response.cookies
		text = convert(response.text)
		if "tb5userid" in cookies:
			self.user_id = cookies["tb5userid"]
			self.tb5_password = cookies["tb5password"]
			self.tb5_session_hash = cookies["tb5sessionhash"]
			self.headers["cookie"] = f"tb5sessionhash={self.tb5_session_hash}; tb5userid={self.user_id}; tb5password={self.tb5_password}"
		return text

	def get_user_info(self, user_id: int):
		return convert(
			requests.get(
				f"{self.api}/member.php?u={user_id}",
				headers=self.headers).text)

	def get_ranking(self):
		return convert(
			requests.get(
				f"{self.api}/tori_ranking.php",
				headers=self.headers).text)

	def get_clans(self):
		return convert(
			requests.get(
				f"{self.api}/clans.php",
				headers=self.headers).text)

	def get_market(self):
		return convert(
			requests.get(
				f"{self.api}/marketplace.php",
				headers=self.headers).text)

	def get_market_item(self, item_id: int):
		return convert(
			requests.get(
				f"{self.api}/marketplace.php?itemid={item_id}",
				headers=self.headers).text)

	def get_all_items(self):
		return convert(
			requests.get(
				f"{self.api}/tori_shop.php",
				headers=self.headers).text)

	def get_user_inventory(self, user_id: int):
		return convert(
			requests.get(
				f"{self.api}/tori_inventory.php?u={user_id}",
				headers=self.headers).text)

	def get_toribash_staff(self):
		return convert(
			requests.get(
				f"{self.api}/showgroups.php",
				headers=self.headers).text)	
