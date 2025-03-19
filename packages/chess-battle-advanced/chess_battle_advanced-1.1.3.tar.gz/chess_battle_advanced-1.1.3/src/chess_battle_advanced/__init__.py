import os as _os, sys as _sys

__stdout = _sys.stdout
with open(_os.devnull, 'w') as _sys.stdout:
    import pygame as _pygame, pygvideo as _pygvideo
_sys.stdout = __stdout

CBA_VIDEO = _os.path.join(_os.path.dirname(__file__), 'chessbattleadvanced.mp4')

def cba():
    # old one:
    #  subprocess.check_call(['ffplay', '-autoexit', '-noborder', '-x', f'{screen_size[0]}', '-y', f'{screen_size[1]}', '-window_title', 'chess battle advanced', f'{CBA_VIDEO}'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open(_os.devnull, 'w') as _sys.stdout:
        _pygame.init()
        info_object = _pygame.display.Info()
        screen_size = (info_object.current_w, info_object.current_h)
        video = _pygvideo.Video(CBA_VIDEO)
        video_length = video.get_duration()
        screen = _pygame.display.set_mode(screen_size, _pygame.NOFRAME)
        _pygame.display.set_caption('chess battle advanced')
        _pygame.display.set_icon(_pygame.image.load(_os.path.join(_os.path.dirname(__file__), 'cba.png')))
        clock = _pygame.time.Clock()
        video.set_size(screen_size)
        video.preplay()

        while True:
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    break
            video.draw_and_update(screen, (0, 0))
            _pygame.display.flip()
            clock.tick(video.get_fps())
            if video.get_pos() >= video_length:
                break
        _pygvideo.quit_all()
        _pygame.quit()