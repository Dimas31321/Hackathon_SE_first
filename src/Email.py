class Email:
    def __init__(self, sender: str, 
                 recipient: str, 
                 theme: str, 
                 data: str,
                 filename: str,
                 body: str = "",
                 category: str = None):
        self.sender = sender
        self.recipient = recipient
        self.theme = theme
        self.data = data
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
               f"Data: {self.data}"