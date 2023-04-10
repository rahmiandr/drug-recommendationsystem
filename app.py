from flask import Flask, request, make_response, render_template, redirect, url_for
from flask.helpers import url_for
import pandas as pd
# import warnings
# warnings.filterwarnings('ignore')

# Initialize Flask app

app = Flask(__name__)

def recomendation_obat(obat, jumlah):
    data = pd.read_excel("data/data.xlsx")
    cosine_sim = pd.read_excel("data/cosine_sim.xlsx")
    indexprod = int(data.loc[data['Drug Name'] == obat].index.values[0])
    similar_review = list(enumerate(cosine_sim.iloc[indexprod]))
    sorted_similar_review = sorted(similar_review, key=lambda x:x[1], reverse=True)
    aa = []
    for i in range(0,jumlah) :
        aa.append(sorted_similar_review[i][0])
    return data.iloc[aa,:7]

# @app.route("/")
# def home_page():
#     return render_template("Home.html")

@app.route("/")
def home_page():
    return render_template("Home.html")

@app.route("/recommendation", methods=["POST"])
def recommendation():
    if request.method == "POST":
        product_name = str(request.form["product_name"])
        jumlah_obat = int(request.form["jumlah_obat"])+1
        df = recomendation_obat(product_name, jumlah_obat)
        # Add row numbers as a new column called "No"
        df["No"] = range(1, len(df)+1)
        
        # Reorder columns so "No" is first
        cols = list(df.columns)
        cols = [cols[-1]] + cols[:-1]
        df = df[cols]
        headers = list(enumerate(df.columns, 1))
        rows = []

        for _, row in df.iterrows():
            rows.append(list(enumerate(row, 1)))

        return render_template("table.html", headers=headers, rows=rows, product_name=product_name)
    # else:
        # return render_template("Home.html")

if __name__ == '__main__':
    app.run(debug=True)
