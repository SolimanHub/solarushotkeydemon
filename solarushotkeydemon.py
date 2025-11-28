#!/usr/bin/env python3

import evdev
import asyncio
from subprocess import check_output

arkos_joypad = evdev.InputDevice("/dev/input/event2")

class Joypad:
    start = 705
    select = 704
    
def runcmd(cmd, *args, **kw):
    print(f">>> {cmd}")
    check_output(cmd, *args, **kw)

async def handle_event(device):
    async for event in device.async_read_loop():
        if device.name == "GO-Super Gamepad" or device.name == "OpenSimHardware OSH PB Controller":
            keys = arkos_joypad.active_keys()
            
            if Joypad.select in keys and event.code == Joypad.start and event.value == 1:
                print("Hotkey detected: FN+Start - Killing Solarus")
                runcmd("pkill solarus-run", shell=True)
                break

def run():
    asyncio.ensure_future(handle_event(arkos_joypad))
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    run()
