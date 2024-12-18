import time
import board
import neopixel

# NeoPixel 설정
pixel_pin = board.D18  # 연결된 핀
num_pixels = 30  # LED 개수
ORDER = neopixel.GRB  # 색상 순서
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

class EmotionLED:
    def __init__(self):
        self.pixels = pixels
        self.clear_lights()

    def set_color(self, r, g, b):
        """모든 LED를 지정된 색으로 설정"""
        for i in range(num_pixels):
            self.pixels[i] = (r, g, b)
        self.pixels.show()

    def update_lights(self, valence_score):
        """
        감정 점수(0.0~1.0)에 따라 색상 업데이트
        - 매우 부정(0.0~0.2): 차가운 진한 남색 (우울함)
        - 부정(0.2~0.4): 차가운 하늘색 (슬픔)
        - 중립(0.4~0.6): 따뜻한 흰색 (평온)
        - 긍정(0.6~0.8): 따뜻한 주황색 (기쁨)
        - 매우 긍정(0.8~1.0): 따뜻한 진한 주황색 (열정)
        """
        if valence_score < 0:
            valence_score = 0
        elif valence_score > 1:
            valence_score = 1

        if valence_score <= 0.2:  # 매우 부정 - 차가운 진한 남색
            intensity = int(255 * (1 - valence_score/0.2))
            self.set_color(0, 0, intensity)
            
        elif valence_score <= 0.4:  # 부정 - 하늘색
            progress = (valence_score - 0.2) / 0.2
            blue = 255
            green = int(200 * progress)
            self.set_color(0, green, blue)
            
        elif valence_score <= 0.6:  # 중립 - 따뜻한 흰색
            progress = (valence_score - 0.4) / 0.2
            base = int(255 * progress)
            self.set_color(base, base, base)
            
        elif valence_score <= 0.8:  # 긍정 - 주황색
            progress = (valence_score - 0.6) / 0.2
            red = 255
            green = int(140 * (1 - progress))
            self.set_color(red, green, 0)
            
        else:  # 매우 긍정 - 진한 주황색
            progress = (valence_score - 0.8) / 0.2
            red = 255
            green = int(70 * (1 - progress))
            self.set_color(red, green, 0)

    def clear_lights(self):
        """LED를 모두 끔"""
        self.set_color(0, 0, 0)
