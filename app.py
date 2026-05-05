from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Sales</title>
        <style>
            body {
                margin: 0;
                font-family: Arial;
                background: #0f0f0f;
                color: white;
            }

            .container {
                max-width: 900px;
                margin: 100px auto;
                text-align: center;
            }

            h1 {
                font-size: 48px;
                background: linear-gradient(90deg, #a855f7, #6366f1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            p {
                color: #aaa;
                font-size: 18px;
            }

            .btn {
                margin-top: 30px;
                padding: 15px 30px;
                background: linear-gradient(90deg, #a855f7, #6366f1);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }

            #chat {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 300px;
                height: 400px;
                background: #1a1a1a;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                display: flex;
                flex-direction: column;
            }

            #messages {
                flex: 1;
                padding: 10px;
                overflow-y: auto;
            }

            input {
                border: none;
                padding: 10px;
                width: 100%;
                box-sizing: border-box;
                background: #111;
                color: white;
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Close More Deals</h1>
            <p>AI that talks to your clients and converts them</p>
            <button class="btn">Start Now</button>
        </div>

        <div id="chat">
            <div id="messages">Hi! I can help you buy or book.</div>
            <input placeholder="Type..." />
        </div>

    </body>
    </html>
    """
