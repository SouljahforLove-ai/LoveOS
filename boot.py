from kernel.microkernel import Microkernel

kernel = Microkernel()

def main():
    kernel.boot()
    print("LoveOS Booted.")
    print("Type 'breathe', 'feel <text>', or 'exit'.")

    while True:
        cmd = input("> ").strip().lower()

        # Emotion tagging
        if cmd.startswith("feel "):
            text = cmd.replace("feel ", "", 1)
            print(kernel.tag_emotion(text))
            continue

        # Breathing ritual
        if cmd == "breathe":
            print(kernel.breathe())
            continue

        # Exit
        if cmd in ("exit", "quit"):
            print("Shutting down LoveOS.")
            kernel.shutdown()
            break

        # Unknown command
        print("Unknown command.")

if __name__ == "__main__":
    main()
