#!/usr/bin/env python3.8

#https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
#https://gist.github.com/LeonardoGentile/7a5330e6bc55860feee5d0dd79e7965d
#https://github.com/dodopontocom/diario_itatiba_robo/blob/44594b8a93497f9797781c74959ad1ab75fc3b9a/scripts/functions.sh

from time import sleep
import subprocess
import sys

#validar argumentos
if len(sys.argv) > 3:
    high = float(sys.argv[1])
    telegram_token = str(sys.argv[2])
    telegram_id = str(sys.argv[3])
else:
    print("\n\nok, sayonnara\n\n")
    exit()

#variaveis
too_high = 65.0
critical_high = 78.0
critical_flag = 0
alerts = [1204,1300,1730,1848,2040,2150,2230]
telegram_url = "https://api.telegram.org/bot{}/sendMessage -d chat_id={} -d text=".format(telegram_token, telegram_id)

#enviar mensagem inicial
init_message = "Monitoramento da temperatura do rasp PI foi iniciado!"
subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, init_message))
temp = float(subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"'))
message = "Temperatura neste momento = "
message += str(temp)
subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))

#monitorar
try:

    while True:

        temp = float(subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"'))

        if ( temp >= high and temp < too_high ):
            message = "(Attention) Temperature = "
            message += str(temp)
            subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
            sleep(120)
        elif ( temp >= too_high and temp < critical_high ):
            message = "(Attention) Temperature = "
            message += str(temp)
            subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
            sleep(30)
        elif ( temp >= critical_high and critical_flag < 2 ):
            message = "(Warning:{}) Critical Temperature = ".format(critical_flag)
            message += str(temp)
            subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
            critical_flag += 1
            sleep(30)
        elif ( temp >= critical_high and critical_flag == 2 ):
            message = "(Final Warning) Critical Temperature = "
            message += str(temp)
            subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
            message = "Shutting the System down"
            subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
            subprocess.getoutput('sudo halt -f')

        elif ( temp < high ):
            h = int(subprocess.getoutput('date +%H%M'))
            if (h in alerts):
                message = "Temperature = "
                message += str(temp)
                subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
                sleep(60)

except KeyboardInterrupt:
    print("\n\nok, sayonnara\n\n")