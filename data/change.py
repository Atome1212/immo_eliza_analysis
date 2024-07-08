import json

# Nom du fichier contenant le JSON non formaté
input_file = 'final_dataset.json'

# Nom du fichier où enregistrer le JSON formaté
output_file = 'formatted_json.json'

# Lecture du JSON depuis le fichier
with open(input_file, 'r', encoding='utf-8') as f:
    json_line = f.read()

# Conversion du JSON en dictionnaire
data = json.loads(json_line)

# Conversion du dictionnaire en JSON formaté
formatted_json = json.dumps(data, indent=4, ensure_ascii=False)

# Enregistrement du JSON formaté dans un nouveau fichier
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(formatted_json)

print(f"Le JSON formaté a été enregistré dans le fichier '{output_file}'.")
