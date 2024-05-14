import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from gtts import gTTS
import gtts

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add your secret key here for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        if not text:
            flash('Please enter text to convert to speech.', 'error')
            return redirect(url_for('index'))

        language = request.form['language']
        rate = int(request.form['rate'])
        volume = float(request.form['volume'])
        save = bool(request.form.get('save'))

        tts = gTTS(text=text, lang=language, slow=False)
        tts.speed = rate / 100  # gTTS uses speed as a float (0.1 to 2.0)

        if save:
            file_name = 'output.mp3'
            tts.save(file_name)
            return send_file(file_name, as_attachment=True)

        # In case the 'save' checkbox is not checked, return nothing.
        return ""

    languages = list(gtts.lang.tts_langs())  # Get a list of all available language codes

    return render_template('index.html', languages=languages)


if __name__ == '__main__':
    app.run(debug=True)
