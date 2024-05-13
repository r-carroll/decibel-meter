import ST7735
from PIL import Image, ImageDraw
from enviroplus.noise import Noise
import math

print("""noise-amps-at-freqs.py - Measure amplitude from specific frequency bins

This example retrieves the median amplitude from 3 user-specified frequency ranges and plots them in Blue, Green and Red on the Enviro+ display.

As you play a continuous rising tone on your phone, you should notice peaks that correspond to the frequency entering each range.

Press Ctrl+C to exit!

""")

noise = Noise()

disp = ST7735.ST7735(
    port=0,
    cs=ST7735.BG_SPI_CS_FRONT,
    dc=9,
    backlight=12,
    rotation=90)

disp.begin()

img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
draw = ImageDraw.Draw(img)


while True:
    amps = noise.get_amplitudes_at_frequency_ranges([
    (200, 2000),   # Mid-range frequencies
    (2000, 8000),  # High-range frequencies
    (8000, 20000)  # Very high-range frequencies 
    ])
    amps = [n * 32 for n in amps]
    rms_amplitude = math.sqrt(sum(amp ** 2 for amp in amps) / len(amps))
    img2 = img.copy()
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    img.paste(img2, (1, 0))


    # draw.line((0, 0, 0, amps[0]), fill=(0, 0, 255))
    draw.line((0, 0, 0, amps[0]), fill=(0, 255, 0))
    draw.line((0, 0, 0, amps[1]), fill=(255, 0, 0))
    draw.line((0, 0, 0, amps[2]), fill=(251, 255, 0))

    decibel = 20 * math.log10(rms_amplitude) if rms_amplitude > 0 else -60
    print(f"Computed Decibel Value: {decibel:.2f} dB")

    disp.display(img)