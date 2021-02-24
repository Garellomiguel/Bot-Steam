import requests
import bs4
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import secret

username = secret.username
password = secret.password

URL = 'https://store.steampowered.com/app/397540/Borderlands_3/'

def discounts(URL):
    res = requests.get(URL)
    if not res.status_code in range(200,299):
        return 'pagina no encontrada'
    else:
        SteamSoup = bs4.BeautifulSoup(res.text, 'html.parser')
        name = SteamSoup.select('.apphub_AppName')[0].get_text()
        if name == 'Borderlands 3':
            descuentos = []
            precios = []
            div_compra = SteamSoup.select('.game_area_purchase_game_wrapper')
            for i in div_compra:
                try:
                    descuento = int(i.select('.discount_pct')[0].get_text()[1:-1])
                    precio = i.select('.discount_final_price')[0].get_text()
                    descuentos.append(descuento)
                    precios.append(precio.split(' ')[1])
                except IndexError:
                    pass
            return list(zip(precios, descuentos))
        else:
            return "nombre equivocado"

def Gmail(subject = "Hay descuentos al fin",from_email= "garellomiguel94@gmail.com", to_emails=["garellomiguel94@gmail.com"],text = 'x'):
    assert isinstance(to_emails, list)
    
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg["Subject"] = subject
    
    body = text

    txt_part = MIMEText(body, 'plain')
    msg.attach(txt_part)

    msg_str = msg.as_string()
    
    #inicializo el servidor de forma segura
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.ehlo()
    server.starttls()

    try:
        server.login(username, password)
    except:
        return ("usuario o contraseña incorrecta")
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()


if __name__ == "__main__":
    precios_descuentos = discounts(URL)
    max = 50
    try:
        for d in precios_descuentos:
            if d[1]> max:
                 max = d[1]
                 best_price = d[0]
        if max > 50: Gmail(text= f'Altos descuentos perro, el mejor es del {max}% con un precio de {best_price}')
    except IndexError:
        Gmail(text=precios_descuentos)
