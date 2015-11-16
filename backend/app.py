from app import app
import os
app.debug = False
port = int(os.environ.get("PORT", 5001))
app.run(host='0.0.0.0', port=port)