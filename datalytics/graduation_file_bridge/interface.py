from graduation_file_bridge.models import JsonMessageFile


class JsonFileStorageInterface:
    file_folder = 'json_alerts/'
    messages_dict = None

    def __init__(self):
        self.messages_dict = {}

        self.setup()

    def setup(self):
        """
        Method run when link is set-up
        :return:
        """
        print("Setup has run")

    def breakdown(self):
        """
        Method run when needing to break down this link
        :return:
        """

    def add_message(self, message):
        message_code = message.code
        if message_code not in self.messages_dict.keys():
            self.messages_dict[message_code] = JsonMessageFile(message_code, message_code)

        message_storer = self.messages_dict[message_code]
        message_storer.add(message)
        message_storer.save()

    def update_message(self, message, create_if_nonexistent=False):
        message_code = message.code

        message_storer = self.messages_dict.get(message_code, None)
        try:
            message_storer.update(message)
        except KeyError:
            if create_if_nonexistent:
                return self.add_message(message)

        message_storer.save()



    def get_messages(self):
        pass


interface = JsonFileStorageInterface()