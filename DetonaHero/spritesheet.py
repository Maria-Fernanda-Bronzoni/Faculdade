import pygame

class Spritesheet:
    def __init__(self, filename):
        """Carrega o arquivo da spritesheet com transparência."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Não foi possível carregar o spritesheet: {filename}")
            raise SystemExit(e)

    def get_image(self, x, y, width, height):
        """Recorta e retorna uma imagem da spritesheet na posição (x,y) com tamanho (width, height)."""
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

    def get_animation_frames(self, frame_width, frame_height, num_frames):
        """Retorna uma lista de frames consecutivos na linha superior da spritesheet para animação."""
        frames = []
        for i in range(num_frames):
            x = i * frame_width
            y = 0
            frames.append(self.get_image(x, y, frame_width, frame_height))
        return frames
