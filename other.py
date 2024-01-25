from flask import Flask, redirect, request

app = Flask(__name__)

@app.before_request
def redirect_to_something():
    target_url = "https://streamsnip.com" + request.full_path
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
