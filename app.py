from app import create_app
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# Create an instance of the app
app = create_app()

port = os.getenv('FLASK_APP_PORT')

if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
