import asyncio
import json
import math
import random
from datetime import datetime, timezone

import websockets

WS_URL = "ws://localhost:8000/ws/telemetry"


async def stream():
    t = 0.0

    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected to ChronosMamba")

        while True:
            sensor = random.randint(1, 5)

            temperature = 25 + math.sin(t) * 5
            vibration = 1.2 + math.cos(t * 2) * 0.4
            voltage = 220 + math.sin(t / 2) * 10

            if sensor == 2:
                temperature += 15

            elif sensor == 3:
                voltage += random.uniform(-30, 30)

            elif sensor == 4:
                vibration += 2

            elif sensor == 5 and random.random() < 0.15:
                temperature += random.uniform(20, 35)
                vibration += random.uniform(3, 5)

            if random.random() < 0.02:
                temperature += random.uniform(15, 25)
                vibration += random.uniform(2, 5)

            packet = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "sensor_id": f"sensor_{sensor:02d}",
                "metrics": [
                    round(temperature, 2),
                    round(vibration, 2),
                    round(voltage, 2),
                ],
            }

            await ws.send(json.dumps(packet))

            try:
                response = await ws.recv()
                print(response)
            except Exception:
                pass

            t += 0.1
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(stream())