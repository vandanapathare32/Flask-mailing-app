from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms import validators,ValidationError
from flask import Flask, render_template, request, flash

class ContactForm(Form):
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

