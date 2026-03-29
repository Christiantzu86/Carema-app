# Génère des icônes PNG simples pour la PWA
import struct, zlib, base64

def make_png(size, bg=(30,58,138), text_color=(255,255,255)):
    """Crée un PNG simple avec fond bleu et lettre C"""
    width = height = size
    
    def write_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    # Header PNG
    header = b'\x89PNG\r\n\x1a\n'
    
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = write_chunk(b'IHDR', ihdr_data)
    
    # Image data - fond bleu avec cercle blanc simplifié
    raw_rows = []
    cx, cy, r = width//2, height//2, int(width*0.35)
    
    for y in range(height):
        row = b'\x00'  # filter type
        for x in range(width):
            dx, dy = x-cx, y-cy
            dist = (dx*dx + dy*dy)**0.5
            
            # Fond dégradé bleu
            if dist > r + width*0.05:
                # Coin arrondi - fond transparent ou bleu foncé
                corner_r = width * 0.2
                cdx = min(x, width-1-x)
                cdy = min(y, height-1-y)
                if (corner_r-cdx)**2 + (corner_r-cdy)**2 > corner_r**2 and cdx < corner_r and cdy < corner_r:
                    row += bytes(bg)
                else:
                    row += bytes(bg)
            elif dist <= r:
                # Intérieur du cercle blanc
                row += bytes(text_color)
            else:
                row += bytes(bg)
        raw_rows.append(row)
    
    # Fond bleu simple avec "C" blanc
    raw_rows = []
    for y in range(height):
        row = b'\x00'
        for x in range(width):
            dx, dy = x - cx, y - cy
            # Fond bleu
            pixel = bg
            # Anneau blanc pour lettre C
            dist = (dx*dx + dy*dy)**0.5
            inner_r = r * 0.55
            outer_r = r * 0.9
            angle_deg = 0
            import math
            if dx != 0 or dy != 0:
                angle_deg = math.degrees(math.atan2(-dy, dx)) % 360
            
            if inner_r <= dist <= outer_r and not (angle_deg < 45 or angle_deg > 315):
                pixel = text_color
            
            row += bytes(pixel)
        raw_rows.append(row)
    
    import zlib
    compressed = zlib.compress(b''.join(raw_rows))
    idat = write_chunk(b'IDAT', compressed)
    iend = write_chunk(b'IEND', b'')
    
    return header + ihdr + idat + iend

for size in [192, 512]:
    png_data = make_png(size)
    with open(f'/home/claude/carema-pwa/icon-{size}.png', 'wb') as f:
        f.write(png_data)
    print(f"Generated icon-{size}.png ({len(png_data)} bytes)")

