from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '{"message": "AI Ruleset Generator API is working!", "status": "ok"}'

@app.route('/health')
def health():
    return '{"status": "healthy", "version": "1.0.0"}'

# Vercel handler
if __name__ == "__main__":
    app.run()
