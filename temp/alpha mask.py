# generate_alpha_mask.py
from PIL import Image
import os

# --- CONFIG ---
input_path = r'C:\Users\NOAHDECASTRO\Desktop\673c7db9-bdbf-491f-afc9-38ba6ad1cb2e - Copia.png'
output_path = r'C:\Users\NOAHDECASTRO\Desktop\alpha_mask.png'

# --- PROCESS ---
img = Image.open(input_path).convert("RGBA")
alpha = img.getchannel("A")
alpha.save(output_path)

print(f"✅ Alpha mask saved: {output_path}")
