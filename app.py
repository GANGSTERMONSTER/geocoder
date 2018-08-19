from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import GoogleV3

nom = GoogleV3()

app = Flask(__name__)

def __init__(self, file_, ):
    self.file_ = file_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods = ["POST"])
def success():
    if request.method == 'POST':
        inputFile = request.files["inputFile"]
        try:
            df = pandas.read_csv(inputFile)
        except:
            return render_template("index.html", text  = "<div class='alert alert-warning'>Please put a CSV file</div>")
        try:
            df['Coordinates'] = df['Address'].apply(nom.geocode)
        except:
            try:
                df['Coordinates'] = df['address'].apply(nom.geocode)
            except:
                return render_template("index.html", text  = "<div class='alert alert-warning'>The column address aren't exsists!</div>")
        df["Latitude"] = df['Coordinates'].apply(lambda x: x.latitude if x != None else None)
        df["Longitude"] = df['Coordinates'].apply(lambda x: x.longitude if x != None else None)
        df = df.drop(df.columns[-3], 1)
        df.to_csv("uploaded.csv")
        return render_template("index.html", btn = "download.html", table = df.to_html(classes = "table"))

@app.route("/download")
def download():
    return send_file("uploaded.csv", attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()