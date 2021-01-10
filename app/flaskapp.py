from flask import (Flask,
                   make_response,
                   redirect,
                   render_template,
                   abort, url_for, session)

from flask_bootstrap import Bootstrap

from werkzeug.exceptions import HTTPException

from collections import OrderedDict


from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import Form

import csv

from joblib import load

import numpy


app = Flask(__name__, template_folder="templates")
bootstrap = Bootstrap(app)

@app.route('/')
def bonjour():
    return "Votre but si vous l'accepter et de battre mon model de prédiction <a href=\"/ticket\">Essayer de prédir un résultat</a>"

# @app.route('/login/')
# def myfonction():
# 	return render_template("autre_page.html")


app.config["SECRET_KEY"] = "randomstring"


class MyForm(Form):
	id = IntegerField("Id", validators= [NumberRange(min=1, max=39645, message="L'id de l'article n'est pas compris entre 1 et 39645 "), DataRequired()])
	user_prediction = BooleanField("Votre prediction (coché plus de 1400 partage, non coché moins de 1400 partage)")
	submit = SubmitField("Submit")



@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
	form = MyForm()
	contenu_html = "Choisiez un id"
	if form.validate_on_submit():
		id = form.id.data
		form.id.data = ''
		user_prediction = bool(form.user_prediction.data)
		form.id.data = ''
		return redirect(url_for('lottery', id=id, user_prediction=user_prediction))
	return render_template("index.html", var1=session.get("id"), var2=contenu_html, form=form)

@app.route('/lottery/<id>/<user_prediction>', methods=['GET'])
def lottery(id, user_prediction):
	id = int(id)
	user_prediction = user_prediction

	contenu_html = "Vous avez missez sur l'article portant l'id {}".format(id)
	def checklottery(id):
		with open('data/OnlineNewsPopularity.csv', newline='') as csvfile:
			articles = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for i in range(id):
				next(articles)
			article = next(articles)
			shares = int(article[-1])
			return shares > 1400
	def lotteryresult(id, user_prediction):
		return str(checklottery(id)) == user_prediction

	def predictionModel(id):
		model_rf = load('data/model_rf.joblib') 
		data = load("data/data.joblib")
		modelprediction = model_rf.predict(numpy.array(data.iloc[2]).reshape(1, -1) )[0]
		return modelprediction == checklottery(id)


	win = lotteryresult(id, user_prediction)
	modelprediction = predictionModel(id)

	return render_template("lottery.html", win=win, user_prediction=user_prediction, modelprediction=modelprediction)



@app.route('/<path:nompath>')
def error_404(nompath):
	abort(404, "The page {} is not found".format(nompath))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', error_message=e), 404



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80)
