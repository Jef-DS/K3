from flask import redirect, render_template, request, url_for
from flask.views import View
import logging
from k3.model import get_vloerplan, reserveer_stoel

logger = logging.getLogger(__name__)
class HomeView(View):
    def __init__(self):
        super().__init__()
        self.init_every_request = False

    def dispatch_request(self):
        logger.debug("Genereer index.html")
        return render_template('index.html', active_page='home')
    
class PlanView(View):
    methods=["GET", "POST"]     #zie Method Hints https://flask.palletsprojects.com/en/stable/views/#method-hints
    def dispatch_request(self):
        message = ""
        if request.method=="POST":
            logger.debug("Formdata: %s", repr(request.form))
            voornaam = request.form["voornaam"] if request.form['voornaam'] != "" else 'anoniem'
            vaknr = int(request.form["vaknr"])
            rijnr = int(request.form["rijnr"])
            stoelnr = int(request.form["stoelnr"])
            logger.info("Maak reservatie voor %s op stoel %s in vak %s in rij %s.",voornaam, stoelnr, vaknr, rijnr)
            reservatienr = reserveer_stoel(voornaam, vaknr, rijnr, stoelnr)
            message = f"Uw reservatienr is {reservatienr}"
            return redirect(url_for('reserveer'))
        plan = get_vloerplan()
        return render_template("reservatie.html", plan=plan, message=message, active_page="reserveer")
    
def register_views(app):
    app.add_url_rule('/', view_func=HomeView.as_view('index'))
    app.add_url_rule('/reserveer', view_func=PlanView.as_view('reserveer'))