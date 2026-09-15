
# O‘ZBEK AI 10.0 ULTIMATE

Maqsad: o‘zbek tilini o‘rganish, tahlil qilish va raqamlashtirish uchun mobil AI platforma.

## Asosiy modullar
1. AI O‘qituvchi — xatolarni topish, izohlash, tuzatish.
2. Ovozli AI — AI javobini TTS orqali ovozlashtirish; serverda STT endpoint ham mavjud.
3. Test va mashqlar — o‘zbek tili bo‘yicha quiz, ball va aniqlik.
4. Milliy korpus — korpus-uslubidagi kontekstli qidiruv.
5. Raqamli lug‘at — izoh, sinonim, antonim, misollar.
6. NLP laboratoriya — matnning ko‘p parametrli tahlili.
7. Progress — urinish, to‘g‘ri javob, tahlil va lug‘at qidiruvlari.
8. Server sozlamasi — Android ichidan API server URL ni almashtirish.

## Arxitektura
Android ilova → FastAPI server → AI / STT / TTS.

OPENAI_API_KEY faqat serverda saqlanadi. APK ichiga API kalit yozilmaydi.

## Ishga tushirish
Server:
```bash
cd server
pip install -r requirements.txt
export OPENAI_API_KEY="YOUR_KEY"
uvicorn main:app --host 0.0.0.0 --port 8000
```

Windows:
```bat
set OPENAI_API_KEY=YOUR_KEY
uvicorn main:app --host 0.0.0.0 --port 8000
```

Emulator: http://10.0.2.2:8000
Telefon: kompyuterning LAN IP manzili, masalan http://192.168.1.10:8000

## APK
GitHub repositoryga yuklang → Actions → Build O'ZBEK AI 10 APK → Run workflow.
Natijadagi artifact ichidan APK olinadi.

## Keyingi ilmiy darajadagi bosqich
- haqiqiy o‘zbek tili korpusi bazasi (PostgreSQL/Elastic/OpenSearch)
- morfologik analizator va lemmatizator
- o‘zbekcha speech dataset
- foydalanuvchi autentifikatsiyasi
- o‘qituvchi kabineti va guruh reytingi
- maqola/dissertatsiya uchun statistik eksport
