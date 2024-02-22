from flask import Flask, redirect, request

app = Flask(__name__)

@app.before_request
def redirect_to_something():
    if request.full_path.endswith("?"):
        full_path = request.full_path[:-1]
    else:
        full_path = request.full_path
    target_url = "https://streamsnip.com" + full_path
    print(target_url)
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
