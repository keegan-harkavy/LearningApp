from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pyttsx3

views = Blueprint('views', __name__)

def text_to_speech(text, gender):
    """
    Function to convert text to speech
    :param text: text
    :param gender: gender
    :return: None
    """
    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict[gender]

    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/demo', methods=['GET', 'POST'])
@login_required
def demo():
    #adds text to speech 
    if request.method == 'POST':
        text = "Meet George, George is a 2nd grader struggling with how to pronounce certain words. Help George learn to read by selecting the characters that correspond to each part of the word.  If you can't remember who a certain character represents, ask George; he is sure to know them all."
        text_to_speech(text, 'Male')
        
    else:
        return render_template("demo.html", user=current_user)




@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
