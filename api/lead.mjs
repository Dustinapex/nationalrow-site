// /api/lead — the one place every lead form on nationalrow.com sends to.
//
// What it does, in order:
//   1. Reads the form (works for normal forms, background "AJAX" forms and JSON).
//   2. Hidden trap fields (_honey / website) filled in?  -> a bot. Pretend success, send nothing.
//   3. Asks Cloudflare whether the Turnstile check passed (server-side, so it can't be faked).
//      Failed or missing?  -> refuse, send nothing.
//   4. Passed  -> hands the lead to FormSubmit, which emails info@nationalrow.com
//      (with the usual cc) exactly like before, with "[Verified]" at the start of the subject.
//
// Needs one Vercel environment variable: TURNSTILE_SECRET_KEY.

const FORMSUBMIT = 'https://formsubmit.co/ajax/info@nationalrow.com';
const SITEVERIFY = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
const SITE = 'https://nationalrow.com';
const PHONE = '(469) 484-7960';
const DEFAULT_THANKS = '/thank-you/';
const ALLOWED_HOSTS = ['nationalrow.com', 'www.nationalrow.com'];

async function readForm(request) {
  const type = (request.headers.get('content-type') || '').toLowerCase();
  const out = [];
  if (type.includes('application/json')) {
    const obj = await request.json();
    for (const [k, v] of Object.entries(obj || {})) {
      if (Array.isArray(v)) v.forEach((x) => out.push([k, String(x)]));
      else if (v !== null && v !== undefined) out.push([k, String(v)]);
    }
  } else {
    const fd = await request.formData();
    for (const [k, v] of fd.entries()) {
      if (typeof v === 'string') out.push([k, v]);
    }
  }
  return out;
}

const first = (pairs, key) => {
  const hit = pairs.find(([k]) => k === key);
  return hit ? hit[1] : '';
};

function wantsJson(request) {
  const accept = (request.headers.get('accept') || '').toLowerCase();
  const type = (request.headers.get('content-type') || '').toLowerCase();
  return accept.includes('application/json') || type.includes('application/json');
}

function safeNext(pairs) {
  const next = first(pairs, '_next');
  try {
    const u = new URL(next, SITE);
    if (ALLOWED_HOSTS.includes(u.hostname)) return u.pathname + u.search;
  } catch (e) {}
  return DEFAULT_THANKS;
}

function reply(request, ok, message, pairs) {
  if (wantsJson(request)) {
    return new Response(JSON.stringify(ok ? { success: 'true' } : { success: 'false', message }), {
      status: ok ? 200 : 400,
      headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
    });
  }
  if (ok) {
    return new Response(null, { status: 303, headers: { location: safeNext(pairs) } });
  }
  const html = `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>We couldn't send that</title>
<body style="font-family:system-ui,sans-serif;max-width:560px;margin:60px auto;padding:0 16px;line-height:1.5">
<h1 style="font-size:22px">We couldn't send your request</h1>
<p>${message}</p>
<p>Please go back and try again, or call or text <a href="tel:+14694847960">${PHONE}</a> and we'll take your details.</p>
<p><a href="javascript:history.back()">&larr; Go back</a></p></body>`;
  return new Response(html, { status: 400, headers: { 'content-type': 'text/html; charset=utf-8' } });
}

async function verifyTurnstile(token, ip) {
  const secret = process.env.TURNSTILE_SECRET_KEY;
  if (!secret) return { ok: false, why: 'missing-secret' };
  if (!token) return { ok: false, why: 'no-token' };
  const body = new URLSearchParams({ secret, response: token });
  if (ip) body.set('remoteip', ip);
  try {
    const r = await fetch(SITEVERIFY, { method: 'POST', body });
    const d = await r.json();
    if (!d.success) return { ok: false, why: (d['error-codes'] || []).join(',') || 'failed' };
    if (d.hostname && !ALLOWED_HOSTS.includes(d.hostname)) return { ok: false, why: 'hostname:' + d.hostname };
    return { ok: true };
  } catch (e) {
    return { ok: false, why: 'siteverify-unreachable' };
  }
}

export async function POST(request) {
  let pairs;
  try {
    pairs = await readForm(request);
  } catch (e) {
    return reply(request, false, 'The form data could not be read.', []);
  }

  // 2. Honeypot: a person never sees these fields.
  const trapped = pairs.some(([k, v]) => (k === '_honey' || k === 'website') && v.trim() !== '');
  if (trapped) {
    console.log('lead blocked: honeypot');
    return reply(request, true, '', pairs); // look successful, send nothing
  }

  // 3. Cloudflare Turnstile, checked on the server.
  const ip = (request.headers.get('x-forwarded-for') || '').split(',')[0].trim();
  const check = await verifyTurnstile(first(pairs, 'cf-turnstile-response'), ip);
  if (!check.ok) {
    console.log('lead blocked: turnstile', check.why);
    return reply(request, false, 'Our automatic check could not confirm the form was sent by a person.', pairs);
  }

  // 4. Forward to FormSubmit -> info@nationalrow.com.
  const DROP = new Set(['cf-turnstile-response', '_honey', 'website', '_next', '_captcha', '_subject']);
  const fwd = new URLSearchParams();
  const subject = first(pairs, '_subject') || 'New case review request — National ROW';
  fwd.set('_subject', '[Verified] ' + subject);
  fwd.set('_captcha', 'false');
  for (const [k, v] of pairs) if (!DROP.has(k)) fwd.append(k, v);
  fwd.append('spam_check', 'Passed Cloudflare check ' + new Date().toISOString());

  try {
    const r = await fetch(FORMSUBMIT, {
      method: 'POST',
      headers: {
        accept: 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        referer: SITE + '/',
        origin: SITE,
      },
      body: fwd,
    });
    const text = await r.text();
    let d = {};
    try { d = JSON.parse(text); } catch (e) {}
    if (r.ok && (d.success === true || d.success === 'true')) {
      console.log('lead sent', first(pairs, 'project_source') || first(pairs, 'source') || '');
      return reply(request, true, '', pairs);
    }
    console.error('formsubmit refused', r.status, text.slice(0, 300));
    return reply(request, false, 'Our email service did not accept the request.', pairs);
  } catch (e) {
    console.error('formsubmit unreachable', String(e));
    return reply(request, false, 'Our email service could not be reached.', pairs);
  }
}

export function GET() {
  return new Response('Method not allowed', { status: 405, headers: { allow: 'POST' } });
}
