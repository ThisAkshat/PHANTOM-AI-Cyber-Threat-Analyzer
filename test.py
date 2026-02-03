from utils.predict import predict

text = "Your bank account is locked. Click here to verify."
label, conf = predict(text)

print(label, conf)
