class Email:
    def __init__(self, sender: str, 
                 recipient: str, 
                 theme: str, 
                 filename: str,
                 sent_or_received: str,
                 body: str = "",
                 category: str = None):
        self.sender = sender
        self.recipient = recipient
        self.theme = theme
        self.sent_or_received = sent_or_received
        self.filename = filename
        self.body = body
        self.category = category
    def __str__(self):
        return f"From: {self.sender}\n" \
               f"To: {self.recipient}\n" \
               f"Theme: {self.theme}\n" \
               f"Filename: {self.filename}\n" \
               f"Body: {self.body}\n" \
               f"Category: {self.category}\n" \
               f"Sent or Received: {self.sent_or_received}"
    def get_filename(self):
        return self.filename
    def get_body(self):
        return self.body
    def get_sender(self):
        return self.sender
    def get_recipent(self):
        return self.recipient
    def get_theme(self):
        return self.theme
    def get_category(self):
        return self.category
    def set_category(self, category: str):
        self.category = category
    def get_sent_or_received(self):
        return self.sent_or_received