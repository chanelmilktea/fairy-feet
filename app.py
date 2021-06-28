import os
import gsheet
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def size():
    shoe_sizes = [x * 0.5 for x in range(10, 30)]
    return render_template('size.html', sizes=shoe_sizes)

@app.route('/results', methods=['POST'])
def results():
    form_data = request.form
    shoe_size = float(form_data.get('sizes', 0))
    shoe_type = form_data.get('shoe_type', 'Women')
    shoe_width = form_data.get('shoe_width', 'Normal')
    print(form_data)
    df = gsheet.get_recs(shoe_type, shoe_size, shoe_width)
    return render_template('results.html', form=form_data, results_table=df.to_html())

@app.route('/contribute')
def index():
    return render_template('contribute.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
