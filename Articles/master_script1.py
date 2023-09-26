import subprocess
import sys

def main():
    # Step 1: Initial rewriting of the article
    process = subprocess.Popen(['python', 'writer.py'])

    while True:
        # Check if writer.py is still running
        ret_code = process.poll()
        
        # If ret_code is None, the process is still running.
        # If ret_code is not None, the process has terminated.
        if ret_code is not None:
            if ret_code != 0:
                print("writer.py was terminated manually. Exiting the main program.")
                sys.exit(1)  # Terminates the program
            
            # If ret_code is 0, writer.py terminated successfully.
            break
    
    with open('variables.txt', 'r') as f:
        keyword, density, length = f.read().splitlines()

    # Loop to perform critiquing and revising three times
    for i in range(3):
        # Step 2: Critiquing
        subprocess.run(['python', 'critique.py'])

        # Step 3: Revising
        subprocess.run(['python', 'revision.py', keyword, density, length])

        print(f"Iteration {i + 1} completed.")

if __name__ == "__main__":
    main()
