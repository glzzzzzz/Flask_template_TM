#from app.config import host
import os 
def reset_message(token):
    return f"""
    <html>
        <body>
            <div style="background-color: #4948FF; text-align: center; display: flex; flex-direction: column; align-items: center; height:auto; width: auto;">
                <div style="text-align: center;"><h1 style="font-weight: bold;color: #FFF; text-align: center; font-family:Arial;">Réinitialisation du mot de passe</h1></div>
                <div style="margin-top: 70px; margin-bottom: 50px; padding: 5px; width: fit-content; height: fit-content; background-color: #e1eaff; border-radius: 20px;"><p style="color: #4948FF; font-family: arial;"> Veuillez <a style="color: #000000; font-family: arial;" href="{os.environ.get('host')}/auth/reset_password/{token}">cliquer ici</a> pour réinitialiser votre mot de passe.</p></div>
            </div>
        </body>
    </html>
    """
