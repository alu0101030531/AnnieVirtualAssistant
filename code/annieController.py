from annie import Annie

exitPhrases = ['bye bye', 'exit', 'bye', 'see you']


# This class manages the flow of execution of the Annie methods
class AnnieController:
    def __init__(self):
        self.annie = Annie()

    # Starts the execution loop
    def play(self):
        phrase = self.annie.recordAudio()
        while phrase not in exitPhrases:
            self.annie.assistantResponse(phrase)
            print(phrase)
            print("")
            self.annie.tokenizeAndChunk(phrase)
            phrase = self.annie.recordAudio()

