# src/main.py
from src.core.pipeline import AssistantPipeline

def main():
    assistant = AssistantPipeline()
    print("Smart Assistant Ready!")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            cmd = input("Press Enter to record, or type 'quit' to exit: ").strip()
            if cmd.lower() in {"q", "quit", "exit"}:
                break
            assistant.run_one_turn()
            print("---\n")
    except KeyboardInterrupt:
        print("\nExiting assistant.")

if __name__ == "__main__":
    main()
