const PYRAMID_PHOTO = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Great%20Pyramid%20(Pyramid%20of%20Cheops%20Khufu)%2C%20Giza%2C%20GG%2C%20EGY%20(47902748131).jpg";

const scenes = [
  {
    duration: 6500,
    kicker: "لغز عمره 4500 عام",
    title: "كيف تبني جبلاً من الحجر… ثم تكتشف داخله فراغاً بجسيمات من الفضاء؟",
    body: "هذه ليست خيالاً علمياً. نحن أمام هرم خوفو؛ بناء ما زال يفرض أسئلته حتى اليوم.",
    fact: "هرم خوفو • الجيزة",
    visual: "hero"
  },
  {
    duration: 6000,
    kicker: "الحجم",
    title: "كان ارتفاعه الأصلي أكثر من 146 متراً.",
    body: "كتلة هندسية هائلة، مؤلفة من ملايين القطع الحجرية، شُيّدت قبل أكثر من أربعة آلاف وخمسمئة سنة.",
    fact: "الارتفاع الأصلي ≈ 146.6 م",
    visual: "scale"
  },
  {
    duration: 5600,
    kicker: "المفاجأة الأولى",
    title: "معظم حجر قلب الهرم لم يأتِ من مكان بعيد.",
    body: "المصريون استخرجوا كميات ضخمة من الحجر الجيري من محاجر قريبة جداً من هضبة الجيزة.",
    fact: "محاجر محلية قرب الجيزة",
    visual: "quarry"
  },
  {
    duration: 6200,
    kicker: "الكسوة البيضاء",
    title: "أما الحجر الجيري الفاخر… فجاء من طرة.",
    body: "كانت الأحجار تنقل عبر النيل والقنوات المائية إلى مشروع البناء في الجيزة.",
    fact: "طرة ← الجيزة",
    visual: "boat"
  },
  {
    duration: 6500,
    kicker: "شاهد من عصر خوفو",
    title: "ثم ظهر اسم رجل: ميرر.",
    body: "سجلات يومية تصف عمل فريقه ورحلات نقل الحجر. بعد 4500 سنة ما زلنا نقرأ تقرير عمل من قلب المشروع.",
    fact: "يوميات ميرر",
    visual: "papyrus"
  },
  {
    duration: 6000,
    kicker: "مدينة البنّائين",
    title: "ورش، مخازن، مخابز، عمال، حرفيون ومديرون.",
    body: "الأدلة قرب الجيزة ترسم صورة مشروع منظم واسع النطاق، لا فوضى عشوائية حول الهرم.",
    fact: "تنظيم • تموين • إدارة",
    visual: "workers"
  },
  {
    duration: 6000,
    kicker: "لكن هنا يبدأ الفراغ",
    title: "نعرف من أين جاءت الأحجار… لكننا لا نملك كتيّب البناء.",
    body: "لا يوجد حتى اليوم وصف مصري كامل يشرح خطوة بخطوة كيف رُفعت الكتل إلى المستويات العليا.",
    fact: "طريقة الرفع الكاملة: غير موثقة",
    visual: "ramp"
  },
  {
    duration: 6800,
    kicker: "2017",
    title: "العلماء استخدموا الميونات للنظر داخل الهرم.",
    body: "جسيمات كونية تعبر الحجر بمعدلات مختلفة؛ ومن خلال قياسها يمكن استنتاج مناطق أقل كثافة داخل البناء.",
    fact: "Muon tomography",
    visual: "muons"
  },
  {
    duration: 6000,
    kicker: "الاكتشاف",
    title: "ظهر فراغ كبير فوق البهو العظيم.",
    body: "ثلاث تقنيات مستقلة أكدت وجود مساحة داخلية كبيرة لم تكن معروفة من قبل.",
    fact: "الطول: لا يقل عن 30 م",
    visual: "void"
  },
  {
    duration: 5600,
    kicker: "السؤال",
    title: "نعرف أنه موجود. لكن لماذا بُني؟",
    body: "وظيفة هذا الفراغ لم تُحسم حتى الآن، وهذا بالضبط ما جعل الاكتشاف أكثر إثارة.",
    fact: "Big Void",
    visual: "voidClose"
  },
  {
    duration: 6200,
    kicker: "2023",
    title: "ثم ظهر ممر آخر خلف الواجهة الشمالية.",
    body: "ممر ظل مخفياً آلاف السنين، بطول يقارب تسعة أمتار ومقطع يقارب مترين في مترين.",
    fact: "ممر ≈ 9 م",
    visual: "corridor"
  },
  {
    duration: 6200,
    kicker: "ما نملكه",
    title: "المحاجر. العمال. القوارب. اليوميات. والفراغات الخفية.",
    body: "كل قطعة دليل تقرّبنا من الصورة، لكنها في الوقت نفسه تفتح سؤالاً جديداً.",
    fact: "الأدلة كثيرة • التعليمات ناقصة",
    visual: "evidence"
  },
  {
    duration: 7000,
    kicker: "السر الحقيقي",
    title: "وجدنا المشروع… لكن كتيّب التعليمات اختفى.",
    body: "وكلما اعتقدنا أننا اقتربنا من النهاية، يفتح هرم خوفو أمامنا باباً جديداً.",
    fact: "النهاية؟ ربما ليست بعد.",
    visual: "ending"
  }
];

const art = {
  hero: () => `
    <section class="scene">
      <img class="scene-img kenburns" src="${PYRAMID_PHOTO}" alt="هرم خوفو">
      <div class="overlay-grid"></div>
      <i class="muon m1"></i><i class="muon m2"></i><i class="muon m3"></i>
    </section>`,
  scale: () => `
    <section class="scene">
      <img class="scene-img kenburns" src="${PYRAMID_PHOTO}" alt="هرم خوفو">
      <div class="height-line"></div>
      <div class="visual-stat" style="right:19%;top:25%"><span class="num">146.6</span><span class="unit">METERS</span></div>
    </section>`,
  quarry: () => visualScene("assets/quarry.svg"),
  boat: () => visualScene("assets/boat.svg"),
  papyrus: () => visualScene("assets/papyrus.svg"),
  workers: () => visualScene("assets/workers.svg"),
  ramp: () => visualScene("assets/ramp.svg"),
  muons: () => `
    <section class="scene">
      <img class="scene-art" src="assets/muon.svg" alt="رسم يوضح فحص الهرم بالميونات">
      <div class="overlay-grid"></div><div class="scanline"></div>
      <i class="muon m1"></i><i class="muon m2"></i><i class="muon m3"></i><i class="muon m4"></i>
    </section>`,
  void: () => `
    <section class="scene">
      <img class="scene-art" src="assets/muon.svg" alt="مقطع تخطيطي للهرم">
      <div class="void-glow"></div><div class="scanline"></div>
      <div class="visual-stat" style="left:11%;top:30%"><span class="num">30+</span><span class="unit">METERS</span></div>
    </section>`,
  voidClose: () => `
    <section class="scene">
      <img class="scene-art" style="transform:scale(1.28) translateY(2%)" src="assets/muon.svg" alt="الفراغ الكبير داخل الهرم">
      <div class="void-glow" style="transform:scale(1.5) rotate(-6deg)"></div>
    </section>`,
  corridor: () => visualScene("assets/corridor.svg"),
  evidence: () => `
    <section class="scene">
      <img class="scene-art" src="assets/evidence.svg" alt="لوحة أدلة عن بناء هرم خوفو">
      <div class="card-chip" style="left:10%;top:20%">المحاجر</div>
      <div class="card-chip" style="right:9%;top:31%">ميرر</div>
      <div class="card-chip" style="left:18%;top:47%">العمال</div>
      <div class="card-chip" style="right:12%;top:58%">الميونات</div>
    </section>`,
  ending: () => `
    <section class="scene">
      <img class="scene-img kenburns" style="filter:saturate(.35) brightness(.42) contrast(1.2)" src="${PYRAMID_PHOTO}" alt="هرم خوفو">
      <div class="end-door"></div><div class="end-ray"></div>
    </section>`
};

function visualScene(src){
  return `<section class="scene"><img class="scene-art" src="${src}" alt=""></section>`;
}

const mount = document.getElementById("sceneMount");
const kicker = document.getElementById("kicker");
const title = document.getElementById("title");
const body = document.getElementById("body");
const fact = document.getElementById("fact");
const progressBar = document.getElementById("progressBar");
const dots = document.getElementById("chapterDots");
const sceneIndex = document.getElementById("sceneIndex");
const sceneTotal = document.getElementById("sceneTotal");
const playBtn = document.getElementById("playBtn");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const fullscreenBtn = document.getElementById("fullscreenBtn");
const audioBtn = document.getElementById("audioBtn");
const audioInput = document.getElementById("audioInput");
const voiceover = document.getElementById("voiceover");
const captionZone = document.querySelector(".caption-zone");

let index = 0;
let playing = false;
let timer = null;
let startedAt = 0;
let elapsedBeforePause = 0;
let activeDurations = scenes.map(s => s.duration);

sceneTotal.textContent = String(scenes.length).padStart(2,"0");
dots.innerHTML = scenes.map(() => "<span></span>").join("");

function renderScene(i){
  index = (i + scenes.length) % scenes.length;
  clearTimeout(timer);
  elapsedBeforePause = 0;
  progressBar.style.transition = "none";
  progressBar.style.width = "0%";

  const s = scenes[index];
  mount.innerHTML = art[s.visual]();
  requestAnimationFrame(() => mount.querySelector(".scene")?.classList.add("active"));

  captionZone.classList.remove("animate");
  kicker.textContent = s.kicker;
  title.textContent = s.title;
  body.textContent = s.body;
  fact.textContent = s.fact;
  fact.classList.toggle("show", Boolean(s.fact));
  void captionZone.offsetWidth;
  captionZone.classList.add("animate");

  sceneIndex.textContent = String(index + 1).padStart(2,"0");
  [...dots.children].forEach((dot, n) => {
    dot.className = n < index ? "done" : n === index ? "active" : "";
  });

  if(playing) scheduleCurrent();
}

function scheduleCurrent(){
  clearTimeout(timer);
  const duration = activeDurations[index];
  const remaining = Math.max(50, duration - elapsedBeforePause);
  startedAt = performance.now();

  progressBar.style.transition = "none";
  progressBar.style.width = (elapsedBeforePause / duration * 100) + "%";
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      progressBar.style.transition = `width ${remaining}ms linear`;
      progressBar.style.width = "100%";
    });
  });

  timer = setTimeout(() => {
    elapsedBeforePause = 0;
    if(index === scenes.length - 1){
      if(voiceover.src && !voiceover.paused) voiceover.pause();
      playing = false;
      playBtn.textContent = "↻";
      return;
    }
    renderScene(index + 1);
  }, remaining);
}

function play(){
  if(index === scenes.length - 1 && progressBar.style.width === "100%") renderScene(0);
  playing = true;
  playBtn.textContent = "❚❚";
  if(voiceover.src && voiceover.readyState >= 2 && voiceover.paused){
    const t = timeBeforeScene(index) + elapsedBeforePause / 1000;
    try{ voiceover.currentTime = Math.min(t, voiceover.duration || t); voiceover.play(); }catch(e){}
  }
  scheduleCurrent();
}

function pause(){
  if(!playing) return;
  elapsedBeforePause += performance.now() - startedAt;
  playing = false;
  clearTimeout(timer);
  playBtn.textContent = "▶";
  progressBar.style.transition = "none";
  progressBar.style.width = (elapsedBeforePause / activeDurations[index] * 100) + "%";
  if(!voiceover.paused) voiceover.pause();
}

function timeBeforeScene(i){
  return activeDurations.slice(0,i).reduce((a,b)=>a+b,0)/1000;
}

function jump(delta){
  const was = playing;
  pause();
  renderScene(index + delta);
  if(was) play();
}

function fitToAudio(durationSeconds){
  if(!Number.isFinite(durationSeconds) || durationSeconds < 15) return;
  const base = scenes.reduce((a,s)=>a+s.duration,0);
  const scale = durationSeconds * 1000 / base;
  activeDurations = scenes.map(s => Math.max(2200, Math.round(s.duration * scale)));
}

playBtn.addEventListener("click", () => playing ? pause() : play());
prevBtn.addEventListener("click", () => jump(-1));
nextBtn.addEventListener("click", () => jump(1));
fullscreenBtn.addEventListener("click", async () => {
  const el = document.getElementById("reel");
  if(!document.fullscreenElement) await el.requestFullscreen?.();
  else await document.exitFullscreen?.();
});
audioBtn.addEventListener("click", () => audioInput.click());
audioInput.addEventListener("change", e => {
  const file = e.target.files?.[0];
  if(!file) return;
  voiceover.src = URL.createObjectURL(file);
  voiceover.load();
  audioBtn.textContent = "🎙 " + file.name.slice(0,18);
});
voiceover.addEventListener("loadedmetadata", () => fitToAudio(voiceover.duration));

window.addEventListener("keydown", e => {
  if(e.code === "Space"){ e.preventDefault(); playing ? pause() : play(); }
  if(e.key === "ArrowLeft") jump(1);
  if(e.key === "ArrowRight") jump(-1);
});

["touchstart","mousedown"].forEach(evt => {
  let x=0;
  document.getElementById("reel").addEventListener(evt, e => {
    x = e.touches ? e.touches[0].clientX : e.clientX;
    const end = evt === "touchstart" ? "touchend" : "mouseup";
    const handler = ev => {
      const nx = ev.changedTouches ? ev.changedTouches[0].clientX : ev.clientX;
      if(Math.abs(nx-x)>55) jump(nx < x ? 1 : -1);
      document.removeEventListener(end,handler);
    };
    document.addEventListener(end,handler,{once:true});
  });
});

renderScene(0);
