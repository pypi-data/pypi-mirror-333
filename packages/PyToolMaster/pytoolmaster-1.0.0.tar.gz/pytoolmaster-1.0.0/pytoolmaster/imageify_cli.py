from PIL import Image

def image_to_ascii(image_path, output_width=100, style="blocky", use_emoji=False):
    chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    if use_emoji:
        chars = ["🔥", "⭐", "🌑", "🌕", "✨", "⚡", "💥", "🌟", "💫", "🌙"]
    
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(output_width * aspect_ratio * 0.55)
    image = image.resize((output_width, new_height))
    image = image.convert("L")
    
    pixels = image.getdata()
    ascii_str = "".join([chars[pixel // 25] for pixel in pixels])
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:index + output_width] for index in range(0, ascii_str_len, output_width)])
    return ascii_img