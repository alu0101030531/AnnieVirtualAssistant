import annie as Annie


annie = Annie.Annie();
text = annie.recordAudio()
for transcription in text:
    if (transcription["transcript"] == 'hey Annie'):
        annie.assistantResponse(transcription["transcript"])
