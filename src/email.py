class Email:
    def __init__(self, sender: str, 
                 recipient: str, 
                 theme: str, 
                 date: str,
                 filename: str,
                 body: str = "",
                 categories: list[str] = []):
        self.sender = sender
        self.recipient = recipient
        self.theme = theme
        self.date = date
        self.filename = filename
        self.body = body
        self.categories = categories if categories is not None else []
    def __str__(self):
        return f"From: {self.sender}\n" \
               f"To: {self.recipient}\n" \
               f"Theme: {self.theme}\n" \
               f"Filename: {self.filename}\n" \
               f"Body: {self.body}\n" \
               f"Categories: {self.categories}\n" \
               f"Date: {self.date}"

