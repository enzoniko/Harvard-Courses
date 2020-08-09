My project is a web chat application called Flack, there is only one HTML page beside the  'layout', that is the 'index' view.
If it is the first time the user visits Flack then he will need to put tell how he wants to be called (the username), this name will be remembered every time he visits the site again, and also it will remember the last channel that he open.
But what are 'channels'? Channels are chat rooms, where users can interact sending messages, they can create channels and join other chat rooms already created, the messages will appear with the name of the user that sent it and the time it was sent.
My personal touch is the possibility to delete messages.
In application.py there are route decorators that remember the name, creates channels, remember the last channel visited and delete messages. Also, there are two socket functions that send messages and update messages two all users using the site.
In channels.py it was created a Channel class, that contains the channel name and message, besides a newMessage function that adds messages to the channel.
The index HTML contains the name form (that only appears the first use), the channel form(where user can create channels), a list of existing channels where the user can click to enter the channel chat room and the Chat Room field, where users can send and receive messages.
formName.js is the script that sends the name to the '/name' route.
The rest of the script is in the HTML file 'index', and the style properties are in the styles.css and a little bit integrated with the  HTML.

