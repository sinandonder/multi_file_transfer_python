class Package:
    def __init__(self, message, file = None):
        self.message = message
        self.file = file
        


if __name__ == "__main__":
    package = Package("mesaj", "askjf")
    print(package.message, package.file)
