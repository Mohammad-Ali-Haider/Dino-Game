with open("options.txt", "r") as f:
            options = f.readlines()
            volume = float(options[0].split(' ')[1].replace('\n', ''))
            for sound in SOUNDS:
                pygame.mixer.Sound.set_volume(sound, volume/100)