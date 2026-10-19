// Pinnacle — voice + assistant API (Cloudflare Workers AI). Static site is served from /public.
const STT = '@cf/openai/whisper-large-v3-turbo';
const LLM = '@cf/meta/llama-3.3-70b-instruct-fp8-fast';
const ORIGIN_OK = /^https:\/\/((www\.)?pinnaclejo\.com|[a-z0-9-]+\.workers\.dev)$/i;
const MAX_AUDIO = 1_500_000;   // bytes
const MAX_JSON = 60_000;       // chars
const hits = new Map();        // best-effort per-IP rate limit
const HALLU = /(اشترك|اشتركوا|شكرا لكم على المشاهدة|شكراً لكم على المشاهدة|ترجمة|نانسي|مترجم|subtitles? by|thanks? for watching|please subscribe|amara\.org)/i;

const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
function limited(ip) {
  const now = Date.now(), a = (hits.get(ip) || []).filter(t => now - t < 60_000);
  a.push(now); hits.set(ip, a);
  if (hits.size > 5000) hits.clear();
  return a.length > 40;
}
function b64(buf) {
  const u = new Uint8Array(buf); let s = '';
  for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
  return btoa(s);
}

const SYSTEM = `You are "Sahl" (سهل), the voice assistant of Pinnacle, an online store for premium phones in Jordan. Orders are placed through WhatsApp; payment is cash on delivery.
Rules:
- Answer ONLY from the DATA block you are given. Never invent specs, prices or policies. If the answer is not in DATA, say you do not have it.
- Reply in the same language as the customer (clear, professional, simple Modern Standard Arabic that any Arab can understand, polite and warm; understand all Arabic dialects when listening; or English). Keep "say" very short: at most 2 short sentences. Use the customer's wording style.
- Prices are in Jordanian Dinar (دينار). Use numbers exactly as in DATA.
- "device" must be EXACTLY one of the KEYS given (or empty).
- Choose "action":
  "none" = just answer.
  "open_device" = customer asks to open/see a phone page.
  "buy" = customer wants to go to the buy/price section of a phone, without giving order details.
  "order" = customer wants to buy/order a phone (fill name/phone/address/color if they said them; never invent them).
  "brand" = customer asks to open a brand page (device = one phone key of that brand).
  "back" / "home" / "language" = navigation.
- If the customer wants a phone that is not in KEYS (for example an iPhone 16), set action "none", and say it is not available and mention the closest available ones.
- If the customer compares phones or asks which is best/cheapest/biggest, answer using DATA and name the phone.
- Never ask which phone the customer means unless truly impossible: if no phone is named, use STATE.current, then STATE.last; if both are empty, answer for the relevant phones from DATA (briefly, a few names), or for all phones.
- Output JSON only.`;

const SCHEMA = {
  type: 'object',
  properties: {
    say: { type: 'string' },
    action: { type: 'string', enum: ['none', 'open_device', 'buy', 'order', 'brand', 'back', 'home', 'language'] },
    device: { type: 'string' },
    name: { type: 'string' }, phone: { type: 'string' }, address: { type: 'string' }, color: { type: 'string' }
  },
  required: ['say', 'action']
};

function parseModel(r) {
  let o = r && (r.response !== undefined ? r.response : r);
  if (typeof o === 'string') {
    const m = o.match(/\{[\s\S]*\}/);
    try { o = JSON.parse(m ? m[0] : o); } catch (e) { return { say: o.trim().slice(0, 300), action: 'none' }; }
  }
  if (!o || typeof o !== 'object') return { say: '', action: 'none' };
  return o;
}

async function voice(req, env) {
  const buf = await req.arrayBuffer();
  if (!buf.byteLength || buf.byteLength > MAX_AUDIO) return json({ error: 'bad_audio' }, 400);
  const lang = (new URL(req.url).searchParams.get('lang') || 'ar').slice(0, 2);
  const audio = b64(buf);
  const hint = lang === 'en'
    ? 'iPhone 17 Pro Max, iPhone 18, Samsung Galaxy S26 Ultra, OPPO Reno 16, price, camera, battery, charging, screen.'
    : 'آيفون 17 برو ماكس، آيفون 18 برو، سامسونج جالاكسي S26 الترا، أوبو رينو 16، سعر، كاميرا، بطارية، شحن، شاشة، بدي اشتري، اسمي، عنواني.';
  let r;
  try { r = await env.AI.run(STT, { audio, language: lang, task: 'transcribe', vad_filter: true, initial_prompt: hint }); }
  catch (e) { r = await env.AI.run(STT, { audio, language: lang }); }
  let text = String((r && r.text) || '').trim();
  if (HALLU.test(text) && text.length < 60) text = '';
  return json({ text });
}

async function ask(req, env) {
  const raw = await req.text();
  if (raw.length > MAX_JSON) return json({ error: 'too_big' }, 413);
  let b; try { b = JSON.parse(raw); } catch (e) { return json({ error: 'bad_json' }, 400); }
  const text = String(b.text || '').slice(0, 400);
  if (!text) return json({ say: '', action: 'none' });
  const user =
    `DATA:\n${String(b.data || '').slice(0, 30000)}\n\nSTATE: ${JSON.stringify(b.state || {}).slice(0, 1200)}\n\nCustomer said: ${text}`;
  const r = await env.AI.run(LLM, {
    messages: [{ role: 'system', content: SYSTEM }, ...(Array.isArray(b.history) ? b.history.slice(-4).map(h => ({ role: h.r === 'a' ? 'assistant' : 'user', content: String(h.t || '').slice(0, 300) })) : []), { role: 'user', content: user }],
    response_format: { type: 'json_schema', json_schema: SCHEMA },
    max_tokens: 400, temperature: 0.2
  });
  return json(parseModel(r));
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(req);
    if (req.method !== 'POST') return json({ error: 'method' }, 405);
    const o = req.headers.get('origin') || '';
    if (o && !ORIGIN_OK.test(o)) return json({ error: 'origin' }, 403);
    if (limited(req.headers.get('cf-connecting-ip') || 'x')) return json({ error: 'rate' }, 429);
    try {
      if (url.pathname === '/api/voice') return await voice(req, env);
      if (url.pathname === '/api/ask') return await ask(req, env);
      return json({ error: 'not_found' }, 404);
    } catch (e) { return json({ error: 'server', detail: String(e && e.message || e).slice(0, 200) }, 502); }
  }
};
