# -------------------- File imports --------------------
from flask_app import app
from flask_app.controllers import recipes_controllers, users_controllers



# -------------------- Conditional statement --------------------

if __name__ == '__main__':
    app.run(debug=True)