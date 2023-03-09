import pyaudio, audioop, math, pyautogui
while True:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(f'{i}) {p.get_device_info_by_index(i)["name"]}')
    CHANNELS = int(input("Выберите устройство записи: "))
    RECORD_SECONDS = int(input('Введите количество секунд записи: '))
    DECIB_MINIMAL = int(input('Введите порог громкости в Дб (рек. 75-80): '))
    MODE = int(input('Режим (1 = клик, 2 = зажим): '))
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        x, y = pyautogui.position()
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data, 2)
        decibel = 20 * math.log10(rms)
        print(f'Громкость: {decibel} Дб')
        if MODE == 1:
            if decibel > DECIB_MINIMAL:
                pyautogui.click(x=x, y=y)
        elif MODE == 2:
            if decibel > DECIB_MINIMAL:
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp(button='left', x=x, y=y)

    stream.stop_stream()
    stream.close()
    p.terminate()
