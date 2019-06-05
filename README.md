# rpi-afegedisplay-remote
Raspberry PI replacement for Afege/Charvet/IBLE/Tast LED display IR remote control

Nous avons un (très cher à l'époque) afficheur à LEDs, qui était piloté via un vieux boitier ethernet par un logiciel nommé "WinCom", totalement inscriptable et pas automatisable du tout, en plus d'utiliser un port tcp/ip tout bizarre. En enlevant le boitier, il était possible de piloter directement le panneau par RS232. Mais il n'a pas été possible de pratiquer le reverse-engineering a cause d'un CRC mystérieux. Par contre, il y avait aussi une télécommande infrarouge presque oubliée et sûrement jamais utilisée, et la solution a été d'intercaler un raspberry pi entre le récepteur infrarouge et le panneau, et d'enregistrer les codes de chaque touche...

![Afficheur Afege avec une panne de métro](media/panne-metro.jpg)

Ne pas oublier de convertir les tensions électriques pour faire passer la liaison série par le Raspberry Pi ! À peu près n'importe quelle sorte de circuit en 74HCT alimenté en 5V convient. Depuis le capteur infrarouge (5V) vers le raspberry pi (3.3V), un pont de résistance est présent en aval du 74HCT (4.7kΩ et 10kΩ à la masse).

![Voltage Translator 2000](media/voltage-level-translation.jpg)
