from bs4 import BeautifulSoup
import requests
import smtplib
import lxml
import locale

### SETTINGS
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
AcceptLanguage = "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6,ru;q=0.5,tr;q=0.4,fr;q=0.3,pl;q=0.2,de;q=0.1,it;q=0.1"
headers = {
    "User-Agent": UserAgent,
    "Accept-Language": AcceptLanguage
}

### OPEN FILE WITH LINKS

with open("links.txt", "r") as l:
    links = l.readlines()
    l.seek(0)
    filedata = l.read()



### CHECK CURRENT PRICE

for l in links:
    thing = l.split("###")[0]
    last_price = float(l.split("###")[1])
    URL = l.split("###")[2]

    response = requests.get(url=URL, headers=headers)
    content = response.text

    soup = BeautifulSoup(content, "lxml")
    text_price = soup.find(class_="a-price aok-align-center")
    price = float(text_price.getText().split("R$")[1].replace(",", "."))


    if price < last_price:

        ### SEND EMAIL TO NOTIFY

        my_email = "email"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password="senha")
            connection.sendmail(
                from_addr=my_email,
                to_addrs="email",
                msg=f"ABAIXOU O PREÇO, COMPRE"
            )

        ### REPLACING OLD PRICE IN FILE
        filedata = filedata.replace(f"{thing}###{last_price}###{URL}", f"{thing}###{price}###{URL}")
        with open("links.txt", "w") as file:
            file.write(filedata)


