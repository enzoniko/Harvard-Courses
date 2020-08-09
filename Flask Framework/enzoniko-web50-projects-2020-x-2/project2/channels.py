"""Create new class called 'Channel' that contains the name and the messages of that channel"""
class Channel:
    def __init__(self, name):
        self.name = name
        self.messages = []
    
    """Define the 'newMessage' function that updates the 'messages' list"""
    def newMessage(self, message, sender, channel, time):

        """Creates a dictionary for the new message with the message, the sender, the channel and the time"""
        new = {"message": message, "sender": sender, "channel": channel, "time": time}

        """Append the new message to the 'messages' list of the channel"""
        self.messages.append(new)

        """If there is more than 100 messages, delete the first ones"""
        while len(self.messages) > 100:
            del(self.messages[0])