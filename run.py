"""
Easy way to start the app for beginners:

    python run.py

This file lives in the PROJECT ROOT (next to the "app" folder), so Python
can find the "app" package correctly. It simply starts the uvicorn server.

(The professional/standard way is still:  uvicorn app.main:app --reload)
"""

import uvicorn

if __name__ == "__main__":
    # reload=True restarts the server automatically when you edit a file.
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
