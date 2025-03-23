import fitz  # PyMuPDF
import os

PDF_FILE = "locked.pdf"  # PDF file name
CHECKPOINT_FILE = "checkpoint.txt"  # Last tried password save korbe

def load_checkpoint():
    """Last tried password load korbe."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_checkpoint(number):
    """Last tried password save korbe."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(number))

def try_password(password):
    """PDF unlock korte try korbe."""
    try:
        doc = fitz.open(PDF_FILE)
        if doc.authenticate(password):
            print(f"\n\nSUCCESS! Password found: {password}")
            with open("password.txt", "w") as f:
                f.write(password)
            return True
    except:
        pass
    return False

def brute_force(start):
    """Brute force logic with checkpoint input support."""
    count = start
    while True:
        password = str(count)
        if try_password(password):
            return
        count += 1
        if count % 1000 == 0:  # Checkpoint save korbe
            save_checkpoint(count)
            print(f"Checkpoint saved: {count}")
            
        if count % 5000 == 0:  # Every 5000 attempt por user input nibe
            user_input = input("\nEnter 'c' to continue or any checkpoint number to resume from: ")
            if user_input.lower() == 'c':
                continue
            elif user_input.isdigit():
                count = int(user_input)
                save_checkpoint(count)
                print(f"\nResuming from {count}...\n")

if __name__ == "__main__":
    print("Enter checkpoint password or press Enter to start from last saved point:")
    user_input = input().strip()
    
    if user_input.isdigit():
        start = int(user_input)
    else:
        start = load_checkpoint()
    
    print(f"\nStarting from {start}...\n")
    brute_force(start)
