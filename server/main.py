import os
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="O‘ZBEK AI 10.0 API")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

MODEL = os.environ.get(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)

TTS_MODEL = os.environ.get(
    "OPENAI_TTS_MODEL",
    "gpt-4o-mini-tts"
)

TRANSCRIBE_MODEL = os.environ.get(
    "OPENAI_TRANSCRIBE_MODEL",
    "gpt-4o-transcribe"
)

VOICE = os.environ.get(
    "OPENAI_TTS_VOICE",
    "coral"
)


class PromptReq(BaseModel):
    prompt: str


class TextReq(BaseModel):
    text: str = ""


class QueryReq(BaseModel):
    query: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "10.0"
    }


@app.post("/ai")
def ai(x: PromptReq):
    try:
        r = client.responses.create(
            model=MODEL,
            instructions=(
                "Siz O‘ZBEK AI platformasining "
                "o‘zbek tili bo‘yicha AI yordamchisisiz. "
                "Javoblarni o‘zbek tilida, aniq va "
                "ta’limiy tarzda bering."
            ),
            input=x.prompt
        )

        return {
            "answer": r.output_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/grammar")
def grammar(x: TextReq):
    try:
        prompt = f"""
O‘zbekcha matnni imlo, grammatika,
punktuatsiya va uslub bo‘yicha tekshiring.

Har bir xatoni quyidagi shaklda yozing:

XATO:
TO‘G‘RI:
SABAB:

Oxirida tahrirlangan to‘liq variantni bering.

Matn:
{x.text}
"""

        r = client.responses.create(
            model=MODEL,
            input=prompt
        )

        return {
            "answer": r.output_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/corpus")
def corpus(x: QueryReq):
    try:
        prompt = f"""
O‘zbek tilidagi “{x.query}” so‘zi yoki
iborasi uchun korpus-uslubida 8 ta
tabiiy misol gap yozing.

Har bir misolda kontekstni ko‘rsating.
So‘z turkumini ham yozing.
"""

        r = client.responses.create(
            model=MODEL,
            input=prompt
        )

        return {
            "answer": r.output_text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        data = await file.read()

        filename = tempfile.mktemp(
            suffix=".wav"
        )

        with open(filename, "wb") as f:
            f.write(data)

        with open(filename, "rb") as audio:

            r = client.audio.transcriptions.create(
                model=TRANSCRIBE_MODEL,
                file=audio,
                language="uz"
            )

        return {
            "text": r.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/tts")
def tts(x: TextReq):
    try:

        r = client.audio.speech.create(
            model=TTS_MODEL,
            voice=VOICE,
            input=x.text,
            instructions=(
                "Speak clearly and naturally "
                "with Uzbek pronunciation."
            )
        )

        return Response(
            content=r.content,
            media_type="audio/mpeg"
        )

    except Exception as e:
        return {
            "error": str(e)
        }
