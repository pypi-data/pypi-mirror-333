import argparse
import subprocess
import os
import sys
import time
import signal
import psutil  
import platform
import threading


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LISTENER_SCRIPT = os.path.join(BASE_DIR, "osc_listener.py")
PID_FILE = os.path.join(os.path.expanduser("~"), "aimat_listener.pid")
COMPOSE_FILE = os.path.join(os.path.dirname(BASE_DIR), "docker-compose.yml")

def start(run_listener=True, attached=False):
    """Start AIMAT (Docker + Listener) with an optional attached mode."""
    print("[INFO] Starting AIMAT...")

    if not os.path.exists(COMPOSE_FILE):
        print("[ERROR] Missing docker-compose.yml! Reinstall AIMAT or check installation.")
        sys.exit(1)    

    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)
    print("[SUCCESS] AIMAT containers are running!")

    if run_listener:
        print("[INFO] Checking for existing AIMAT listener...")

        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r") as pid_file:
                old_pid = pid_file.read().strip()

            if psutil.pid_exists(int(old_pid)):
                print(f"[WARNING] Found existing listener process (PID {old_pid}). Stopping it first...")
                try:
                    if platform.system() == "Windows":
                        subprocess.run(["taskkill", "/F", "/PID", old_pid], check=True)
                    else:
                        os.kill(int(old_pid), signal.SIGTERM)
                    print("[SUCCESS] Old listener process stopped.")
                except Exception as e:
                    print(f"[ERROR] Failed to stop old listener: {e}")

            os.remove(PID_FILE)

        print(f"[INFO] Starting AIMAT OSC listener in {'attached' if attached else 'background'} mode...")

        try:
            if attached:
                # Run the listener **in foreground (blocking)**
                subprocess.run(["python", LISTENER_SCRIPT], check=True)

            else:
                # Run the listener **in background (non-blocking)**
                listener_process = subprocess.Popen(
                    ["python", LISTENER_SCRIPT],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,  # Line-buffered output to prevent hanging
                    start_new_session=True
                )

                # Function to capture relevant listener output
                def read_listener_output(process):
                    while True:
                        output = process.stdout.readline()
                        if not output and process.poll() is not None:
                            break
                        if "Detected local IP" in output or "Listening for OSC messages on port" in output:
                            print(f"[LISTENER] {output.strip()}")

                # Start a separate thread for capturing output
                output_thread = threading.Thread(target=read_listener_output, args=(listener_process,), daemon=True)
                output_thread.start()

                # Save the listener PID
                with open(PID_FILE, "w") as pid_file:
                    pid_file.write(str(listener_process.pid))

                print(f"[SUCCESS] AIMAT listener started in the background with PID {listener_process.pid}")

        except Exception as e:
            print(f"[ERROR] Exception while starting listener: {e}")

    print("[INFO] Use 'aimat stop' to shut it down.")



def run_listener_func():
    """Run the OSC listener script"""
    if not os.path.exists(LISTENER_SCRIPT):
        print("[ERROR] Listener script not found!")
        sys.exit(1)

    subprocess.run(["python", LISTENER_SCRIPT], check=True)

def stop():
    """Stop AIMAT (Docker + Listener) safely."""
    print("[INFO] Stopping AIMAT...")
    subprocess.run(["docker", "compose", "down"], check=True)

    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as pid_file:
            pid = int(pid_file.read().strip())

        print(f"[INFO] Stopping AIMAT listener (PID: {pid})...")

        try:
            # Verify if process is still running
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                
                # Confirm it's the listener before killing it
                if "python" in process.name():
                    if platform.system() == "Windows":
                        subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
                    else:
                        os.kill(pid, signal.SIGTERM)
                    
                    print("[SUCCESS] Listener stopped.")
                else:
                    print("[WARNING] PID does not match AIMAT listener.")
            else:
                print("[WARNING] Listener process not found (already stopped).")

        except Exception as e:
            print(f"[ERROR] Failed to stop listener: {e}")

        os.remove(PID_FILE)
    else:
        print("[WARNING] No listener process found.")

    print("[SUCCESS] AIMAT has been shut down.")



def restart():
    print("[INFO] Restarting AIMAT...")
    stop()
    start()

def run_listener():
    """Run the OSC listener script"""
    print("[INFO] Starting AIMAT OSC listener...")
    if not os.path.exists(LISTENER_SCRIPT):
        print("[ERROR] Listener script not found!")
        sys.exit(1)
    
    subprocess.run(["python", LISTENER_SCRIPT], check=True)

def main():
    parser = argparse.ArgumentParser(description="AIMAT: AI Music Artist Toolkit")
    parser.add_argument("command", choices=["start", "stop", "restart"], help="Control AIMAT")
    parser.add_argument("--no-listener", action="store_true", help="Disable OSC listener")
    parser.add_argument("--attached", action="store_true", help="Run listener in foreground mode (blocking)")

    args = parser.parse_args()

    if args.command == "start":
        start(run_listener=not args.no_listener, attached=args.attached)
    elif args.command == "stop":
        stop()
    elif args.command == "restart":
        stop()
        start(run_listener=not args.no_listener, attached=args.attached)


if __name__ == "__main__":
    main()
