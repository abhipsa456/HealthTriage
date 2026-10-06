import onnx_asr

print("Loading Odia speech model...")

model = onnx_asr.load_model(
    "OpenVoiceOS/ai4bharat-indicconformer-or-onnx"
)

print("Model loaded successfully.")
print("Transcribing Odia audio...")

result = model.recognize(
    "odia_test.wav"
)

print("\nOdia transcription:")
print(result)