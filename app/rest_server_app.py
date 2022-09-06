from flask import Flask, make_response, jsonify
import logging

from app.students.students_app import users_blueprint

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger("rest_server_app")

app = Flask(__name__)
app.register_blueprint(users_blueprint)


@app.route('/ping')
def ping():
    logger.info("application pinged...")
    return jsonify({'status': 'Welcome!'})


if __name__ == '__main__':
    app.run()
