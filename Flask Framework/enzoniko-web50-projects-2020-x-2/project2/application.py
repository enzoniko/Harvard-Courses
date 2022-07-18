"""Libraries"""
import os
import datetime
from  flask import Flask, render_template, redirect, jsonify, request, url_for, session
from flask_socketio import SocketIO, emit, send
from flask_session import Session
from channels import Channel 

"""Flask and Session config"""
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"

"""SocketIO and Session config"""
socketio = SocketIO(app)
Session(app)

"""Channels list"""
channels = []

"""Route decorators"""
@app.route("/")
def index():

    """Try to render with the Display Name form session, but if there isn't anyone yet just render simpler"""
    try:
        return render_template("index.html", name=session["name"], lastChannel=session["lastChannel"], channels=channels)
    except KeyError:
        try:
            return render_template("index.html", name=session["name"], channels=channels)
        except KeyError:
            return render_template("index.html", channels=channels)

@app.route("/name", methods=["POST"])
def name():

    """Get name from the form"""
    name = request.form.get("name")

    """If Display Name fields not empty, create and remember it in the session"""
    if name is '':
        return jsonify({"success": False})
    session["name"] = name
    return jsonify({"success": True, "name": name})

@app.route("/lastChannel", methods=["POST"])
def lastChannel():

    """Remember the Last Channel visited in Session"""
    channel = request.form.get("lastChannel")
    session["lastChannel"] = channel
    return '', 204

@app.route("/channel", methods=["POST"])
def channel():

    """Get Channel name from the form"""
    channel = request.form.get("channel")

    """If element already exist, do not create another with the same name"""
    for elem in channels:
        if channel in elem.name:
            return jsonify({"success": False})

    """If no channel named the same, then create a new one"""
    newChannel = Channel(channel)
    channels.append(newChannel)

    """Create a dictionary for every object so they can be transformed easily into JSON objects"""
    channelsFeed = [object.__dict__ for object in channels]
    return jsonify({"success": True, "channel": channel, "channels": channelsFeed})

@app.route("/delete", methods = ["POST"])
def delete():

    """Get the channel"""
    channel = request.form.get("channel")

    """Get the message"""
    message = request.form.get("message")

    """Find the channel containing the message that you want to delete"""
    for may_channel in channels:
        if may_channel.name == channel:

            """After finding the channel, find the message of the channel that you want to delete"""
            for may_message in may_channel.messages:
                if may_message["message"] == message:

                    """Delete it"""
                    del(may_channel.messages[may_channel.messages.index(may_message)])
    return '', 204

@socketio.on("sendMessage")
def chat(data):

    """Get the channel and the message that you want to send"""
    channel = data["channel"]
    message = data["message"]

    """Loop through channels seeking for the same name"""
    """If the channel exist then append the new message, else emit a Not success message"""
    for checkChannel in channels:
        if checkChannel.name == channel:

            """Get the time that the message is sended"""
            time = '{:%H:%M:%S}'.format(datetime.datetime.now())

            """Get the name of the user that is sending the message"""
            sender = session["name"]

            """Append the new message to the channel"""
            """Using the 'newMessage' function that requires"""
            """The message, the sender name, the channel and the time"""
            checkChannel.newMessage(message, sender, channel, time)

            """Create a variable containing the last message sended"""
            """Emit this last message"""
            last_message = checkChannel.messages[-1]
            emit("update", last_message, broadcast=True)
            return
    emit("update", "Not success", broadcast=True)

@socketio.on("update")
def conect(data):

    """Get the channel from the last message"""
    channel = data["channel"]

    """Loop through channels seeking for the same name"""
    """If the channel exist then update the old messages of that channel with the last message"""
    for checkChannel in channels:
        if checkChannel.name == channel:

            """Update"""
            oldMessages = checkChannel.messages

            """Get the name"""
            name = session["name"]

            """Emit the update"""
            emit("updateChat", (oldMessages, name), broadcast=True)
            return
    emit("updateChat", 'notFound', broadcast=True)

"""Run the socket app"""
if __name__ == '__main__':
    socketio.run(app)


