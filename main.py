import asyncio
import base64
import json
import io
import os
import sys
import pyaudio
from rich import color, console
from websockets.asyncio.client import connect
from websockets.asyncio.connection import Connection
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

if sys.version_info < (3, 11, 0):
    import taskgroup, exceptiongroup

    asyncio.TaskGroup = taskgroup.TaskGroup
    asyncio.ExceptionGroup = exceptiongroup.ExceptionGroup

F = pyaudio.paInt16
C = 1
SSR = 16000
RSR = 24000
CS = 512

h = "generativelanguage.googleapis.com"
m = "gemini-2.0-flash-exp"

ak = os.getenv("GOOGLE_API_KEY")

u = f"wss://{h}/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={ak}"

class AL:
    def __init__(self):
        self.ws = None
        self.q = asyncio.Queue()
        self.s = 0

    async def srt(self):
        sm = {"setup": {"model": f"models/{m}", "generation_config": {"response_modalities": ["TEXT"]}}}
        await self.ws.send(json.dumps(sm))
        rr = await self.ws.recv(decode=False)
        sr = json.loads(rr.decode("utf-8"))

        im = {"client_content": {"turns": [{"role": "user", "parts": [{"text": "你是一名专业的英语口语指导老师，你需要帮助用户纠正语法发音，用户将会说一句英文，然后你会给出识别出来的英语是什么，并且告诉他发音中有什么问题，语法有什么错误，并且一步一步的纠正他的发音，当一次发音正确后，根据当前语句提出下一个场景的语句,然后一直循环这个过程，直到用户说OK，我要退出。你的回答永远要保持中文。如果明白了请回答OK两个字"}]}], "turn_complete": True}}
        await self.ws.send(json.dumps(im))
        cr = []
        async for rr in self.ws:
            r = json.loads(rr.decode("utf-8"))
            try:
                if "serverContent" in r:
                    p = r["serverContent"].get("modelTurn", {}).get("parts", [])
                    for pt in p:
                        if "text" in pt:
                            cr.append(pt["text"])
            except Exception:
                pass

            try:
                tc = r["serverContent"]["turnComplete"]
            except KeyError:
                pass
            else:
                if tc:
                    if "".join(cr).startswith("OK"):
                        print("初始化完成 ✅")
                        return

    async def la(self):
        pa = pyaudio.PyAudio()
        mi = pa.get_default_input_device_info()
        st = pa.open(format=F, channels=C, rate=SSR, input=True, input_device_index=mi["index"], frames_per_buffer=CS)
        c = Console()
        c.print("🎤 说一句英语吧！比如: What is blockchain?", style="yellow")
        while True:
            d = await asyncio.to_thread(st.read, CS)
            ad = [abs(int.from_bytes(d[i:i + 2], byteorder='little', signed=True)) for i in range(0, len(d), 2)]
            v = sum(ad) / len(ad)
            if v > 200:
                if self.s == 0:
                    c.print("🎤 :", style="yellow", end="")
                    self.s += 1
                c.print("*", style="green", end="")
            self.q.put_nowait(d)

    async def sa(self):
        while True:
            ch = await self.q.get()
            m = {"realtime_input": {"media_chunks": [{"data": base64.b64encode(ch).decode(), "mime_type": "audio/pcm"}]}}
            await self.ws.send(json.dumps(m))

    async def ra(self):
        c = Console()
        cr = []
        async for rr in self.ws:
            if self.s == 1:
                c.print("\n♻️ 处理中：", end="")
                self.s += 1
            r = json.loads(rr.decode("utf-8"))
            try:
                if "serverContent" in r:
                    p = r["serverContent"].get("modelTurn", {}).get("parts", [])
                    for pt in p:
                        if "text" in pt:
                            cr.append(pt["text"])
                            c.print("-", style="blue", end="")
            except Exception:
                pass

            try:
                tc = r["serverContent"]["turnComplete"]
            except KeyError:
                pass
            else:
                if tc:
                    if cr:
                        t = "".join(cr)
                        c.print("\n🤖 =============================================", style="yellow")
                        c.print(Markdown(t))
                        cr = []
                        self.s = 0

    async def r(self):
        async with connect(u, additional_headers={"Content-Type": "application/json"}) as ws:
            self.ws = ws
            c = Console()
            c.print("Gemini 英语口语助手", style="green", highlight=True)
            c.print("Make by twitter: @BoxMrChen", style="blue")
            c.print("============================================", style="yellow")
            await self.srt()
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.la())
                tg.create_task(self.sa())
                tg.create_task(self.ra())

                def ce(t):
                    if t.cancelled():
                        return
                    if t.exception() is None:
                        return
                    e = t.exception()
                    print(f"Error: {e}")
                    sys.exit(1)

                for t in tg._tasks:
                    t.add_done_callback(ce)


if __name__ == "__main__":
    m = AL()
    asyncio.run(m.r())