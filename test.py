import google.generativeai as genai

print("List of models that support generateContent:\n")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

print("List of models that support embedContent:\n")
for m in genai.list_models():
    if "embedContent" in m.supported_generation_methods:
        print(m.name)