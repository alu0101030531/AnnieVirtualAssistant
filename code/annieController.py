from annie import Annie

endPhrases = ['bye bye', 'exit', 'bye', 'see you']


# This class manages the flow of execution of the Annie methods
class AnnieController:
    def __init__(self):
        self.annie = Annie()

    # Start the execution loop
    def play(self):
        phrase = self.annie.recordAudio()
        while phrase not in endPhrases:
            self.annie.assistantResponse(phrase)
            phrase = self.annie.recordAudio()
            print(phrase)
