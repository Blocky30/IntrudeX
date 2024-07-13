import functions
import exes

boot_sequence = [
    ("Initializing system...", 0.4),
    ("Loading core modules...", 0.6),
    ("Starting network services...", 0.4),
    ("Establishing secure connection...", 0.7),
    ("Initializing firewall bypass...", 0.6),
    ("Scanning local network...", 1.1),
    ("Loading terminal interface...", 0.4),
    ("Starting background processes...", 0.5),
    ("Retrieving server list...", 0.85),
    ("Loading brute-force algorithms...", 0.9),
    ("Starting SQL injection module...", 0.9),
    ("Activating proxy chains...", 0.6),
    ("Establishing VPN connection...", 0.6),
    ("Initializing SSH tunnels...", 0.85),
    ("Loading password cracking tools...", 0.9),
    ("Starting DNS spoofing service...", 0.7),
    ("Activating keylogger...", 0.5),
    ("Compiling network map...", 0.8),
    ("Initializing system override protocols...", 0.8),
    ("Injecting payloads...", 0.6),
    ("Establishing covert channels...", 0.7),
    ("Connecting to 127.0.0.1...", 0.35),
    ("Boot sequence completed. System ready.", 0.4),
]

standard_data = {
    "dataVersion": 1,
    "username": "",
    "password": "",
    "firstBoot": "true",
}

ascii_intrudex = """
        __               _                               _
       |  |             | |                             | |
       |  |           __| |__                           | |           \\\    //
       |  |          |__   __|                          | |            \\\  //
       |  |   _ ____    | |    _ ___    _    _    ______| |   _____     \\\//
       |  |  | '___ \   | |   | '--_\  | |  | |  / .---.  |  / ___ \  <||//||>
       |  |  | |   | |  | |   | |      | |  | |  | |   |  |  | ____/    //\\\ 
       |  |  | |   | |  | |   | |      | \__/ |  | '---'  |  | |___    //  \\\ 
       |__|  |_|   |_|  |_|   |_|      \______/  \_____/\_|  \_____/  //    \\\ 
      """

color_map = {
    '1': '\033[34m',   # Blue
    '2': '\033[32m',   # Green
    '3': '\033[36m',   # Aqua (Cyan)
    '4': '\033[31m',   # Red
    '5': '\033[35m',   # Purple (Magenta)
    '6': '\033[33m',   # Yellow
    '7': '\033[37m',   # White
    '8': '\033[90m',   # Gray (Light Black)
    '9': '\033[94m',   # Light Blue
    'A': '\033[92m',   # Light Green
    'B': '\033[96m',   # Light Aqua (Light Cyan)
    'C': '\033[91m',   # Light Red
    'D': '\033[95m',   # Light Purple (Light Magenta)
    'E': '\033[93m',   # Light Yellow
    'F': '\033[97m',   # Bright White
}

printed_color_map = "  1 - Blue\n  2 - Green\n  3 - Aqua (Cyan)\n  4 - Red\n  5 - Purple (Magenta)\n  6 - Yellow\n  7 - White\n  8 - Gray (Light Black)\n  9 - Light Blue\n  A - Light Green\n  B - Light Aqua (Light Cyan)\n  C - Light Red\n  D - Light Purple (Light Magenta)\n  E - Light Yellow\n  F - Bright White"

exes = {
    "%TUNES_EXE%": exes.handleTunes,
}