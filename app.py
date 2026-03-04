from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Bhai, Project Success Ho Gaya! Website Live Hai. 🔥</h1>"

if __name__ == "__main__":
    # Kubernetes Service port 80 ko target kar raha hai, 
    # isliye hum ise container ke port 80 par chalayenge.
    app.run(host='0.0.0.0', port=80)
