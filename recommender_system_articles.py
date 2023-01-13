import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

STATIC_FOLDER = 'static/'
MODEL_FOLDER = STATIC_FOLDER + 'models/'
DATA_FOLDER = STATIC_FOLDER + 'data/'

@app.before_first_request
def load__data():
    """
    Load predicted data
    :return: model (global variable)
    """
    print('[INFO] Predicted data Loading ........')
    #global model
    #model = load_model(MODEL_FOLDER + 'bidirectional_lstm_with_return_sequences_on_embedded_heroku')
    #print('[INFO] : Model loaded')
    global data
    data = pd.read_pickle(DATA_FOLDER + 'prediction_content_based.pickle')
    


def predict(user_id, rs_type="content_based"):
    # Prediction:
    result_pred = list(data[data["user_id"]==str(user_id)]["article_id"]) 
    return result_pred

# Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_id = request.form["user_id"]
        print( user_id)
        #rs_type = request.form["rs_type"]
        result_pred = predict(user_id)

        return render_template('index.html', data=data, userId=user_id, result_pred=result_pred, predict=True)
    else:

        return render_template('index.html', data=data, predict=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host="0.0.0.0", port=port, debug=True)
