import os, sys

old_stdout = sys.stdout
with open(os.devnull, 'w') as sys.stdout:
    import pygame, pygvideo
sys.stdout = old_stdout

CBA_VIDEO = os.path.join(os.path.dirname(__file__), 'chessbattleadvanced.mp4')

def cba():
    # old one:
    #  subprocess.check_call(['ffplay', '-autoexit', '-noborder', '-x', f'{screen_size[0]}', '-y', f'{screen_size[1]}', '-window_title', 'chess battle advanced', f'{CBA_VIDEO}'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open(os.devnull, 'w') as sys.stdout:
        pygame.init()
        info_object = pygame.display.Info()
        screen_size = (info_object.current_w, info_object.current_h)
        video = pygvideo.Video(CBA_VIDEO)
        video_length = video.get_duration()
        screen = pygame.display.set_mode(screen_size, pygame.NOFRAME)
        pygame.display.set_caption('chess battle advanced')
        pygame.display.set_icon(pygame.image.load(os.path.join(os.path.dirname(__file__), 'cba.png')))
        clock = pygame.time.Clock()
        video.set_size(screen_size)
        video.preplay()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            video.draw_and_update(screen, (0, 0))
            pygame.display.flip()
            clock.tick(video.get_fps())
            if video.get_pos() >= video_length:
                break
        pygvideo.quit_all()
        pygame.quit()