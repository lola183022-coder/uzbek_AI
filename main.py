
import json, tempfile
from pathlib import Path
import requests
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

KV = r"""
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

<Nav>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(12); spacing: dp(8)
        canvas.before:
            Color: rgba: .965,.975,.99,1
            Rectangle: pos:self.pos; size:self.size
        BoxLayout:
            size_hint_y: None; height: dp(52)
            Label:
                text: "O‘ZBEK AI 10.0"
                font_size: sp(24); bold: True
            Label:
                text: "ULTIMATE"
                font_size: sp(12)
        ScreenManager:
            id: pages
            MainPage:
            TeacherPage:
            VoicePage:
            QuizPage:
            CorpusPage:
            DictPage:
            NlpPage:
            StatsPage:
            SettingsPage:
        BoxLayout:
            size_hint_y: None; height: dp(54); spacing: dp(5)
            Button: text:"🏠"; on_release: pages.current="main"
            Button: text:"🤖"; on_release: pages.current="teacher"
            Button: text:"🎙"; on_release: pages.current="voice"
            Button: text:"🧠"; on_release: pages.current="quiz"
            Button: text:"📚"; on_release: pages.current="corpus"
            Button: text:"📊"; on_release: pages.current="stats"

<MainPage>:
    name:"main"
    BoxLayout:
        orientation:"vertical"; spacing:dp(10); padding:dp(10)
        Label:
            text:"O‘zbek tilini o‘rganish, tahlil qilish va raqamlashtirish"
            font_size:sp(18); text_size:self.width,None
            size_hint_y:None; height:dp(65)
        GridLayout:
            cols:2; spacing:dp(8)
            Button: text:"AI O‘qituvchi"; on_release: app.go("teacher")
            Button: text:"Ovozli AI"; on_release: app.go("voice")
            Button: text:"Test va mashqlar"; on_release: app.go("quiz")
            Button: text:"Milliy korpus"; on_release: app.go("corpus")
            Button: text:"Raqamli lug‘at"; on_release: app.go("dict")
            Button: text:"NLP tahlil"; on_release: app.go("nlp")
        Label:
            text:"Bugungi progress: " + str(app.correct) + " to‘g‘ri / " + str(app.attempts) + " urinish"
            font_size:sp(16)
        Button:
            text:"⚙ Sozlamalar"; size_hint_y:None; height:dp(48)
            on_release: app.go("settings")

<TeacherPage>:
    name:"teacher"
    BoxLayout:
        orientation:"vertical"; spacing:dp(7); padding:dp(8)
        Label: text:"AI O‘qituvchi"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(40)
        TextInput: id:t; hint_text:"Gap yoki matn kiriting"; multiline:True
        BoxLayout:
            size_hint_y:None; height:dp(46)
            Button: text:"Tahlil"; on_release:root.analyze(t.text)
            Button: text:"Tuzatish"; on_release:root.correct_text(t.text)
        ScrollView:
            Label: text:root.out; text_size:self.width,None; size_hint_y:None; height:self.texture_size[1]
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<VoicePage>:
    name:"voice"
    BoxLayout:
        orientation:"vertical"; spacing:dp(7); padding:dp(8)
        Label: text:"Ovozli AI"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(40)
        Label: text:root.status; size_hint_y:None; height:dp(42)
        TextInput: id:v; hint_text:"Mikrofon yozuvi bo‘lmasa, savolni yozing"; multiline:True
        Button: text:"AI ga yuborish"; size_hint_y:None; height:dp(46); on_release:root.ask(v.text)
        Button: text:"🔊 Javobni ovoz chiqarib o‘qish"; size_hint_y:None; height:dp(46); on_release:root.speak(root.answer)
        ScrollView:
            Label: text:root.answer; text_size:self.width,None; size_hint_y:None; height:self.texture_size[1]
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<QuizPage>:
    name:"quiz"
    BoxLayout:
        orientation:"vertical"; spacing:dp(8); padding:dp(8)
        Label: text:"O‘zbek tili — AI Test"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(42)
        Label: text:root.question; text_size:self.width,None; font_size:sp(17)
        GridLayout:
            cols:1; spacing:dp(6); size_hint_y:None; height:dp(210)
            Button: text:root.a; on_release:root.answer(0)
            Button: text:root.b; on_release:root.answer(1)
            Button: text:root.c; on_release:root.answer(2)
            Button: text:root.d; on_release:root.answer(3)
        Label: text:root.feedback; font_size:sp(16)
        Button: text:"Yangi savol"; size_hint_y:None; height:dp(46); on_release:root.new_question()
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<CorpusPage>:
    name:"corpus"
    BoxLayout:
        orientation:"vertical"; spacing:dp(7); padding:dp(8)
        Label: text:"Milliy til korpusi"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(42)
        TextInput: id:q; hint_text:"So‘z yoki ibora"; size_hint_y:None; height:dp(46)
        Button: text:"Korpus qidiruvi"; size_hint_y:None; height:dp(46); on_release:root.search(q.text)
        ScrollView: Label: text:root.out; text_size:self.width,None; size_hint_y:None; height:self.texture_size[1]
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<DictPage>:
    name:"dict"
    BoxLayout:
        orientation:"vertical"; spacing:dp(7); padding:dp(8)
        Label: text:"Raqamli lug‘at"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(42)
        TextInput: id:w; hint_text:"So‘z"; size_hint_y:None; height:dp(46)
        Button: text:"Izlash"; size_hint_y:None; height:dp(46); on_release:root.lookup(w.text)
        ScrollView: Label: text:root.out; text_size:self.width,None; size_hint_y:None; height:self.texture_size[1]
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<NlpPage>:
    name:"nlp"
    BoxLayout:
        orientation:"vertical"; spacing:dp(7); padding:dp(8)
        Label: text:"NLP laboratoriya"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(42)
        TextInput: id:n; hint_text:"Matn"; multiline:True
        Button: text:"Kompleks NLP tahlil"; size_hint_y:None; height:dp(46); on_release:root.analyze(n.text)
        ScrollView: Label: text:root.out; text_size:self.width,None; size_hint_y:None; height:self.texture_size[1]
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<StatsPage>:
    name:"stats"
    BoxLayout:
        orientation:"vertical"; spacing:dp(10); padding:dp(15)
        Label: text:"Mening natijalarim"; font_size:sp(22); bold:True; size_hint_y:None; height:dp(48)
        Label: text:"Test urinishlari: " + str(app.attempts); font_size:sp(17)
        Label: text:"To‘g‘ri javoblar: " + str(app.correct); font_size:sp(17)
        Label: text:"Tahlil qilingan matnlar: " + str(app.analyzed); font_size:sp(17)
        Label: text:"Lug‘at qidiruvlari: " + str(app.words); font_size:sp(17)
        Label: text:"Aniqlik: " + str(app.accuracy) + "%"; font_size:sp(18); bold:True
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")

<SettingsPage>:
    name:"settings"
    BoxLayout:
        orientation:"vertical"; spacing:dp(8); padding:dp(8)
        Label: text:"Server sozlamalari"; font_size:sp(21); bold:True; size_hint_y:None; height:dp(42)
        TextInput: id:u; text:app.server_url; size_hint_y:None; height:dp(46)
        Button: text:"Saqlash va tekshirish"; size_hint_y:None; height:dp(46); on_release:root.save(u.text)
        Label: text:root.status
        Button: text:"← Bosh sahifa"; size_hint_y:None; height:dp(44); on_release:app.go("main")
"""

def post(url, payload, timeout=30):
    try:
        r=requests.post(url,json=payload,timeout=timeout); r.raise_for_status(); return r.json()
    except Exception as e: return {"error":str(e)}

class Nav(Screen): pass
class MainPage(Screen): pass

class TeacherPage(Screen):
    out=StringProperty("")
    def analyze(self,text):
        if not text.strip(): return
        d=post(App.get_running_app().server_url+"/grammar",{"text":text})
        self.out=d.get("answer",d.get("error",""))
        App.get_running_app().analyzed+=1; App.get_running_app().save()
    def correct_text(self,text):
        d=post(App.get_running_app().server_url+"/ai",{"prompt":f"O‘zbekcha matnni tahrir qiling. Faqat: xato → to‘g‘ri → qisqa izoh. Matn: {text}"})
        self.out=d.get("answer",d.get("error",""))

class VoicePage(Screen):
    status=StringProperty("Savolni yozing. Keyingi bosqichda mikrofon yozuvi avtomatik yuboriladi.")
    answer=StringProperty("")
    def ask(self,text):
        if not text.strip(): return
        d=post(App.get_running_app().server_url+"/ai",{"prompt":text})
        self.answer=d.get("answer",d.get("error","")); self.status="AI javobi tayyor."
    def speak(self,text):
        if not text.strip(): return
        try:
            r=requests.post(App.get_running_app().server_url+"/tts",json={"text":text},timeout=45)
            r.raise_for_status()
            p=Path(tempfile.gettempdir())/"ozbekai_answer.mp3"; p.write_bytes(r.content)
            s=SoundLoader.load(str(p))
            if s: s.play(); self.status="🔊 Audio ijro etilmoqda."
            else: self.status="Audio yaratildi, ijro moduli mavjud emas."
        except Exception as e: self.status="TTS xatosi: "+str(e)

class QuizPage(Screen):
    question=StringProperty("Yangi savolni bosing.")
    a=StringProperty(""); b=StringProperty(""); c=StringProperty(""); d=StringProperty("")
    feedback=StringProperty("")
    correct_index=NumericProperty(0)
    bank=[
      ("Qaysi variant imlo jihatdan to‘g‘ri?","mas'ul","ma'sul","masul","ma’sul",3),
      ("Qaysi gap to‘g‘ri?","Men kitob o‘qiyapman.","Men kitob o‘qiyabman.","Men kitob o‘qiyapmanmi.","Men kitob o‘qiyapman.",0),
      ("“Go‘zal” so‘ziga yaqin ma’noli so‘zni toping.","chiroyli","tez","katta","uzoq",0),
      ("Qaysi biri fe’l?","kitob","o‘qimoq","qalam","yashil",1)
    ]
    def on_pre_enter(self,*a): self.new_question()
    def new_question(self):
        import random
        q=random.choice(self.bank)
        self.question=q[0]; self.a=q[1]; self.b=q[2]; self.c=q[3]; self.d=q[4]; self.correct_index=q[5]
        self.feedback="Javobni tanlang."
    def answer(self,i):
        app=App.get_running_app(); app.attempts+=1
        if i==self.correct_index:
            app.correct+=1; self.feedback="✅ To‘g‘ri!"
        else: self.feedback="❌ Noto‘g‘ri. To‘g‘ri javob: "+[self.a,self.b,self.c,self.d][self.correct_index]
        app.save()

class CorpusPage(Screen):
    out=StringProperty("")
    def search(self,q):
        d=post(App.get_running_app().server_url+"/corpus",{"query":q})
        self.out=d.get("answer",d.get("error",""))

class DictPage(Screen):
    out=StringProperty("")
    def lookup(self,w):
        if not w.strip(): return
        d=post(App.get_running_app().server_url+"/ai",{"prompt":f"O‘zbek tilidagi “{w}” so‘ziga lug‘aviy izoh, 3 sinonim, 2 antonim va 2 misol gap bering."})
        self.out=d.get("answer",d.get("error",""))
        App.get_running_app().words+=1; App.get_running_app().save()

class NlpPage(Screen):
    out=StringProperty("")
    def analyze(self,text):
        if not text.strip(): return
        d=post(App.get_running_app().server_url+"/ai",{"prompt":f"""O‘zbekcha matnni NLP laboratoriya hisobotidek tahlil qiling:
1) so‘zlar soni; 2) gaplar soni; 3) asosiy mavzu; 4) kalit so‘zlar;
5) taxminiy so‘z turkumlari; 6) uslub; 7) imlo/uslub muammolari; 8) qisqa xulosa.
Matn: {text}"""})
        self.out=d.get("answer",d.get("error",""))
        App.get_running_app().analyzed+=1; App.get_running_app().save()

class StatsPage(Screen): pass
class SettingsPage(Screen):
    status=StringProperty("")
    def save(self,url):
        app=App.get_running_app(); app.server_url=url.strip().rstrip("/"); app.save()
        try:
            r=requests.get(app.server_url+"/health",timeout=5); self.status="Server: "+r.json().get("status","ok")
        except Exception as e: self.status="Ulanish tekshiruvi: "+str(e)

class OzbekAI(App):
    server_url=StringProperty("http://10.0.2.2:8000")
    attempts=NumericProperty(0); correct=NumericProperty(0); analyzed=NumericProperty(0); words=NumericProperty(0)
    @property
    def accuracy(self):
        return round((self.correct/self.attempts)*100,1) if self.attempts else 0
    def build(self):
        self.path=Path(self.user_data_dir)/"state.json"; self.load()
        Builder.load_string(KV); sm=ScreenManager(); sm.add_widget(Nav(name="root")); return sm
    def go(self,name): self.root.get_screen("root").ids.pages.current=name
    def load(self):
        try:
            d=json.loads(self.path.read_text(encoding="utf-8"))
            for k in ("server_url","attempts","correct","analyzed","words"):
                if k in d: setattr(self,k,d[k])
        except: pass
    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.write_text(json.dumps({"server_url":self.server_url,"attempts":self.attempts,"correct":self.correct,"analyzed":self.analyzed,"words":self.words},ensure_ascii=False),encoding="utf-8")

if __name__=="__main__": OzbekAI().run()
