const PYRAMID_PHOTO =
  "https://commons.wikimedia.org/wiki/Special:Redirect/file/Great%20Pyramid%20(Pyramid%20of%20Cheops%20Khufu)%2C%20Giza%2C%20GG%2C%20EGY%20(47902748131).jpg";

const scenes = [
  {duration:6200,kicker:"لغز عمره 4500 سنة",title:"كيف تبني جبلاً من الحجر…",subtitle:"ثم تترك داخله سراً لا يُكتشف إلا بجسيمات قادمة من الفضاء؟",visual:"hero"},
  {duration:5400,kicker:"هرم خوفو",title:"أكبر أهرامات مصر.",subtitle:"والوحيد من عجائب الدنيا السبع القديمة الذي ما زال قائماً.",visual:"hero2"},
  {duration:5200,kicker:"الحجم",title:"146 متراً تقريباً.",subtitle:"هذا كان ارتفاعه الأصلي.",visual:"height"},
  {duration:5600,kicker:"المفاجأة الأولى",title:"أغلب حجر قلب الهرم… محلي.",subtitle:"استُخرج من محاجر قريبة من هضبة الجيزة.",visual:"quarry"},
  {duration:5600,kicker:"الكسوة الخارجية",title:"أما الحجر الأبيض الفاخر… فجاء من طرة.",subtitle:"ونُقل بالقوارب إلى مشروع الهرم.",visual:"boat"},
  {duration:5900,kicker:"شاهد من عصر خوفو",title:"ميرر ترك لنا يومياته.",subtitle:"تقرير عمل حقيقي يصف رحلات فريقه ونقل الحجر.",visual:"papyrus"},
  {duration:5600,kicker:"مدينة البنّائين",title:"ورش. مخازن. مطابخ. مخابز.",subtitle:"مشروع منظم واسع النطاق، لا فوضى عشوائية.",visual:"workers"},
  {duration:5700,kicker:"لكن هنا يبدأ اللغز",title:"أين اختفى كتيب التعليمات؟",subtitle:"نعرف العمال والنقل والمحاجر… لكن طريقة الرفع الكاملة غير موثقة.",visual:"ramp"},
  {duration:6300,kicker:"2017",title:"العلماء استخدموا الميونات.",subtitle:"جسيمات كونية تمر عبر الحجر وتكشف ما يختبئ في الداخل.",visual:"muons"},
  {duration:5900,kicker:"ثم ظهرت المفاجأة",title:"فراغ كبير بطول 30 متراً.",subtitle:"مساحة ضخمة فوق البهو العظيم أكدت وجودها ثلاث تقنيات مستقلة.",visual:"void"},
  {duration:5100,kicker:"وحتى الآن",title:"لا نعرف لماذا بُني.",subtitle:"وهذا ما جعل الاكتشاف أكثر غموضاً.",visual:"void2"},
  {duration:5700,kicker:"2023",title:"ممر آخر خلف الواجهة الشمالية.",subtitle:"نحو 9 أمتار ظلت مخفية آلاف السنين.",visual:"corridor"},
  {duration:6500,kicker:"السر الحقيقي",title:"وجدنا المشروع… لكن كتيب التعليمات اختفى.",subtitle:"وكلما اقتربنا من النهاية، يفتح الهرم أمامنا باباً جديداً.",visual:"ending"}
];

const mount = document.getElementById("sceneMount");
const kicker = document.getElementById("kicker");
const title = document.getElementById("title");
const subtitle = document.getElementById("subtitle");
const textLayer = document.getElementById("textLayer");
const flashCut = document.getElementById("flashCut");

let index = 0;
let timer = null;

function dustLayer(count = 18){
  let out = '<div class="dust">';
  for(let i=0;i<count;i++){
    const left = (i * 37) % 100;
    const delay = ((i * 0.73) % 7).toFixed(2);
    const duration = (7 + ((i * 1.17) % 5)).toFixed(2);
    const size = 2 + (i % 4);
    out += `<i style="left:${left}%;bottom:${-20-(i%5)*6}px;width:${size}px;height:${size}px;animation-delay:${delay}s;animation-duration:${duration}s"></i>`;
  }
  return out + "</div>";
}

function visualScene(src,motion="push-in",extra=""){
  return `<section class="scene"><img class="scene-art ${motion}" src="${src}" alt="">${extra}</section>`;
}

const art = {
  hero: () => `<section class="scene"><img class="scene-img push-in" src="${PYRAMID_PHOTO}" alt="هرم خوفو"><div class="sun-haze"></div>${dustLayer(24)}</section>`,
  hero2: () => `<section class="scene"><img class="scene-img pan-left" src="${PYRAMID_PHOTO}" alt="هرم خوفو">${dustLayer(16)}</section>`,
  height: () => `<section class="scene"><img class="scene-img tilt-up" src="${PYRAMID_PHOTO}" alt="هرم خوفو"><div class="big-number">146<span>METERS</span></div></section>`,
  quarry: () => visualScene("assets/quarry.svg","pan-right",dustLayer(26)),
  boat: () => visualScene("assets/boat.svg","pan-left",'<div class="route"></div><div class="boat-wake"></div>'),
  papyrus: () => visualScene("assets/papyrus.svg","drift",'<div class="paper-shadow"></div>'),
  workers: () => visualScene("assets/workers.svg","push-in",dustLayer(16)),
  ramp: () => visualScene("assets/ramp.svg","tilt-up",'<div class="ramp-block"></div>'),
  muons: () => visualScene("assets/muon.svg","push-in",'<div class="scanline"></div><i class="muon m1"></i><i class="muon m2"></i><i class="muon m3"></i><i class="muon m4"></i>'),
  void: () => visualScene("assets/muon.svg","push-in",'<div class="void-glow"></div><div class="scanline"></div><div class="big-number" style="top:25%;left:8%">30+<span>METERS</span></div>'),
  void2: () => visualScene("assets/muon.svg","drift",'<div class="void-glow" style="transform:rotate(-7deg) scale(1.45)"></div>'),
  corridor: () => visualScene("assets/corridor.svg","push-in",'<div class="corridor-light"></div><div class="big-number" style="top:22%;left:8%">9<span>METERS</span></div>'),
  ending: () => `<section class="scene"><img class="scene-img push-in" style="filter:brightness(.38) contrast(1.18) saturate(.42)" src="${PYRAMID_PHOTO}" alt="هرم خوفو"><div class="end-door"></div><div class="end-ray"></div>${dustLayer(14)}</section>`
};

function render(i){
  clearTimeout(timer);
  index = i;

  const s = scenes[index];
  mount.innerHTML = art[s.visual]();

  requestAnimationFrame(() => {
    mount.querySelector(".scene")?.classList.add("active");
  });

  textLayer.classList.remove("animate");
  kicker.textContent = s.kicker;
  title.textContent = s.title;
  subtitle.textContent = s.subtitle;
  void textLayer.offsetWidth;
  textLayer.classList.add("animate");

  flashCut.classList.remove("fire");
  void flashCut.offsetWidth;
  flashCut.classList.add("fire");

  timer = setTimeout(() => {
    if(index < scenes.length - 1){
      render(index + 1);
    }
  }, s.duration);
}

window.addEventListener("load", () => {
  setTimeout(() => render(0), 250);
});
