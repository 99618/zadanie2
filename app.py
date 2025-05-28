from flask import Flask, request, render_template
import datetime
import logging
import requests
import sys
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]

)

logging.info(f"Aplikcja rozpoczela prace {datetime.datetime.now()} UTC "+
", a zostala stworzona przez Mateusz Marczak, aplikacja dziala na porcie 5050.")

wybor = {
    "Polska": {"Warszawa": (52.2298,21.0118),"Lublin":(51.25,22.5667),"Krakow":(50.0614,19.9366)},
    "Anglia": {"Manchester":(53.4809,-2.2374),"London":(51.5085,-0.1257),"Liverpool":(53.4106,-2.9779)},
    "Niemcy": {"Berlin":(52.5244,13.4105),"Hamburg":(53.5507,9.993),"Munich":(48.1374,11.5755)},
    "USA": {"Washington":(38.8951,-77.0364),"Chicago":(41.85,-87.65),"New York":(40.7143,-74.006)}
}

@app.route('/')
def index():
    return render_template('index.html', wybor=wybor)

@app.route('/pogoda', methods=['POST'])
def pogoda():
    panstwo = request.form['panstwo']
    miasto = request.form['miasto']
    szer_geo, dl_geo = wybor[panstwo][miasto]
    pogoda_w_miescie = get_pogoda(szer_geo, dl_geo)
    return render_template('pogoda.html',panstwo=panstwo,miasto=miasto,pogoda_w_miescie=pogoda_w_miescie)

def get_pogoda(szer_geo, dl_geo):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={szer_geo}&longitude={dl_geo}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["current_weather"]
    else:
        return {"error": "Nie udalo sie pobrac obecnej pogody."}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
