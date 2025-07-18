import time
import threading
import math
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import requests


COINGECKO_IDS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'DOGE': 'dogecoin',
    'LTC': 'litecoin',
    'XRP': 'ripple',
    # add more as you like...
}

COIN_COLORS = {
    'BTC': (247, 147, 26),    # Bitcoin orange (#f7931a)
    'ETH': (98, 126, 234),    # Ethereum blue (#627eea)
    'DOGE': (194, 166, 51),   # Dogecoin gold (#c2a633)
    'LTC': (184, 184, 184),   # Litecoin silver (#b8b8b8)
    'XRP': (52, 106, 169),    # XRP navy (#346aa9)
}

class MatrixController:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 16
        options.cols = 32
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        options.pixel_mapper_config = "Rotate:180"
        self.matrix = RGBMatrix(options=options)
        self.stop_event = threading.Event()
        self.worker = None

    def _run_in_thread(self, target, *args):
        if self.worker and self.worker.is_alive():
            self.stop_event.set()
            self.worker.join()
        self.stop_event.clear()
        self.worker = threading.Thread(target=target, args=args, daemon=True)
        self.worker.start()

    def clear(self):
        if self.worker and self.worker.is_alive():
            self.stop_event.set()
            self.worker.join()
        self.matrix.Clear()

    def show_text(self, text,
                  color=(255,255,255),
                  font_path="fonts/7x13.bdf",
                  scroll_speed=0.05):
        def runner():
            font = graphics.Font()
            font.LoadFont(font_path)
            text_color = graphics.Color(*color)
            pos = self.matrix.width
            y = font.height
            while not self.stop_event.is_set():
                self.matrix.Clear()
                length = graphics.DrawText(self.matrix, font, pos, y, text_color, text)
                pos -= 1
                if pos + length < 0:
                    pos = self.matrix.width
                time.sleep(scroll_speed)
        self._run_in_thread(runner)

    def show_clock(self,
                   color=(0,255,255),
                   font_path="fonts/5x7.bdf"):
        def runner():
            font = graphics.Font()
            font.LoadFont(font_path)
            text_color = graphics.Color(*color)
            while not self.stop_event.is_set():
                now = datetime.now().strftime("%H:%M")
                # measure text width
                text_width = graphics.DrawText(self.matrix, font, 0, 0, text_color, now)
                x = (self.matrix.width - text_width) // 2
                y = (self.matrix.height + font.height) // 2
                self.matrix.Clear()
                graphics.DrawText(self.matrix, font, x, y, text_color, now)
                # sleep until the next minute (or break earlier)
                for _ in range(60):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
        self._run_in_thread(runner)

    def run_program(self, name):
        if name == 'rotating_square':
            self._run_in_thread(self._rotating_square)
        elif name == 'rainbow':
            self._run_in_thread(self._rainbow)
        elif name == 'clock':
            self.show_clock()
        else:
            self.clear()

    def _rotating_square(self):
        size = 10
        cx, cy = self.matrix.width // 2, self.matrix.height // 2
        angle = 0.0
        while not self.stop_event.is_set():
            self.matrix.Clear()
            x0 = int(cx + (size/2) * math.cos(angle))
            y0 = int(cy + (size/2) * math.sin(angle))
            x1 = int(cx - (size/2) * math.cos(angle))
            y1 = int(cy - (size/2) * math.sin(angle))
            for x in range(min(x0, x1), max(x0, x1)+1):
                for y in range(min(y0, y1), max(y0, y1)+1):
                    self.matrix.SetPixel(x, y, 0, 255, 0)
            angle += 0.1
            time.sleep(0.1)

    def _rainbow(self):
        import colorsys
        step = 0
        while not self.stop_event.is_set():
            for x in range(self.matrix.width):
                for y in range(self.matrix.height):
                    hue = (x + step) / float(self.matrix.width)
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
                    self.matrix.SetPixel(x, y, r, g, b)
            step = (step + 1) % self.matrix.width
            time.sleep(0.05)

    def set_pixel(self, x, y, color):
        if self.worker and self.worker.is_alive():
            self.stop_event.set()
            self.worker.join()
        self.matrix.SetPixel(x, y, *color)

    def show_crypto_ticker(self, tickers,
                           price_color=(255,255,0),
                           vs_currency='usd',
                           font_path="fonts/5x7.bdf",
                           update_interval=60):
        """Display first valid ticker statically:
           * Line 1: symbol in coin-specific color
           * Line 2: integer price in user-defined price_color
        """
        def runner():
            font       = graphics.Font()
            font.LoadFont(font_path)

            # pick first valid symbol + ID
            symbol = None
            cid    = None
            for sym in tickers:
                key = sym.upper()
                if key in COINGECKO_IDS:
                    symbol = key
                    cid    = COINGECKO_IDS[key]
                    break
            if not symbol:
                return

            # coin color from map (fallback to yellow)
            coin_color = COIN_COLORS.get(symbol, (255,255,0))
            sym_color  = graphics.Color(*coin_color)
            price_col  = graphics.Color(*price_color)

            while not self.stop_event.is_set():
                # fetch price
                try:
                    data = requests.get(
                        'https://api.coingecko.com/api/v3/simple/price',
                        params={'ids': cid, 'vs_currencies': vs_currency},
                        timeout=10
                    ).json()
                    price = data.get(cid, {}).get(vs_currency)
                except Exception:
                    price = None

                if price is not None:
                    price_int = int(price)
                    line1 = symbol
                    line2 = str(price_int)

                    self.matrix.Clear()
                    # draw symbol (line1) at top
                    w1 = graphics.DrawText(self.matrix, font, 0, 0, sym_color, line1)
                    x1 = (self.matrix.width  - w1) // 2
                    y1 = font.height
                    graphics.DrawText(self.matrix, font, x1, y1, sym_color, line1)

                    # draw price (line2) at bottom
                    w2 = graphics.DrawText(self.matrix, font, 0, 0, price_col, line2)
                    x2 = (self.matrix.width  - w2) // 2
                    y2 = self.matrix.height - 1
                    graphics.DrawText(self.matrix, font, x2, y2, price_col, line2)

                # wait up to update_interval seconds
                for _ in range(update_interval):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
        
        self._run_in_thread(runner)