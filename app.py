from flask import Flask, request, send_file, make_response, render_template
from Model import do_plot


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['Post'])
def simulate():

    country = request.form.get("country")
    effective_contact_rate = request.form.get("effective_contact_rate")
    recovery_rate = request.form.get("recovery_rate")
    mortality_rate = request.form.get("mortality_rate")
    
    print(country,effective_contact_rate,recovery_rate,mortality_rate)

    fig = do_plot(country, effective_contact_rate, recovery_rate,mortality_rate)

    return send_file(fig,attachment_filename='plot.png', mimetype='image/png')



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    app.run(debug=True)