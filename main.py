from jarvis.core.agent import Assistant
from jarvis.services.tts import Speaker
from jarvis.services.voice import VoiceInput
from jarvis.utils.parser import normalize_text


def choose_mode() -> str:
    print("\n1. Voice")
    print("2. Text")
    print("3. Hybrid")
    choice = input("Select: ").strip()
    return choice if choice in {"1", "2", "3"} else "2"


def get_input(mode: str, voice: VoiceInput) -> str | None:
    if mode == "1":
        return voice.listen()

    if mode == "2":
        return input("You: ").strip()

    while True:
        src = input("\n[t]ext / [v]oice / [q]uit: ").strip().lower()
        if src == "q":
            return "exit"
        if src == "t":
            return input("You: ").strip()
        if src == "v":
            heard = voice.listen()
            if heard:
                print(f"You (voice): {heard}")
                return heard
            print("JARVIS: I could not hear anything.")
        else:
            print("JARVIS: Choose t, v, or q.")


def main():
    assistant = Assistant()
    speaker = Speaker()
    voice = VoiceInput()

    mode = choose_mode()
    speaker.say("Jarvis ready.")

    while True:
        raw = get_input(mode, voice)
        if raw is None:
            continue

        text = normalize_text(raw)
        if not text:
            continue

        result = assistant.run(text)
        speaker.say(result.text)

        if result.exit:
            break


if __name__ == "__main__":
    main()
