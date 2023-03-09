__all__ = []


class File:
    def __init__(self, name, format):
        # Metadata.
        self.name = name
        self.format = format

        # Actual data.
        with open(self.name, "rb") as file:
            self.data = file.read()

        self.size = len(self.data)

        # Stack options.
        self.supports_stack_before_sof = False
        self.supports_stack_after_eof = False

        # Parasite options.
        self.supports_parasite = False
        self.max_parasite_size = 0

    def host_parasite(self, parasite):
        pass
