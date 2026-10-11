/* National ROW — form guard (spam protection for every lead form on the site).
 *
 * Loaded in <head> of every page that has a lead form.
 *  1. NR_LEAD_ENDPOINT: every form sends to /api/lead on this site. That
 *     server code checks Cloudflare and only then emails info@nationalrow.com.
 *  2. Cloudflare Turnstile: an invisible "are you a person" check added to
 *     each form. Most visitors never see it; a suspicious one gets a click box.
 *  3. Honeypot: hidden fields (_honey / website) people never see. Filled in
 *     means a bot, and the form is not sent.
 *  4. Speed check: nobody types a name, phone and email in under 3 seconds.
 */
(function () {
  'use strict';

  window.NR_LEAD_ENDPOINT = '/api/lead';

  var SITEKEY = '0x4AAAAAAFT5z7oFZjIAlZd6';
  var LOADED_AT = Date.now();
  var MIN_MS = 3000;
  var PHONE = '(469) 484-7960';
  var widgets = [];   // {form, id}
  var pending = null; // {form, submitter, timer} waiting for a Turnstile token

  function isLeadForm(f) {
    var a = f.getAttribute('action') || '';
    return !!(f.querySelector('input[name="_honey"]') || /formsubmit\.co|\/api\/lead/.test(a));
  }

  function honeypotFilled(form) {
    var traps = form.querySelectorAll('input[name="_honey"], input[name="website"]');
    for (var i = 0; i < traps.length; i++) {
      if (traps[i].value && traps[i].value.trim() !== '') return true;
    }
    return false;
  }

  function submitButton(form) {
    return form.querySelector('button[type="submit"], input[type="submit"], .submit-btn, button:not([type])');
  }

  function showNote(form, text) {
    var n = form.querySelector('.nr-guard-note');
    if (!n) {
      n = document.createElement('p');
      n.className = 'nr-guard-note';
      n.setAttribute('role', 'status');
      n.style.cssText = 'margin:10px 0 0;font-size:14px;line-height:1.4;color:#b45309;font-weight:600;';
      var btn = submitButton(form);
      if (btn && btn.parentNode) btn.parentNode.insertBefore(n, btn.nextSibling);
      else form.appendChild(n);
    }
    n.textContent = text;
  }

  function clearNote(form) {
    var n = form.querySelector('.nr-guard-note');
    if (n) n.parentNode.removeChild(n);
  }

  function tokenOf(form) {
    var t = form.querySelector('input[name="cf-turnstile-response"]');
    return t ? t.value : '';
  }

  function widgetFor(form) {
    for (var i = 0; i < widgets.length; i++) if (widgets[i].form === form) return widgets[i].id;
    return null;
  }

  function onToken() {
    if (!pending) return;
    var p = pending; pending = null;
    clearTimeout(p.timer);
    clearNote(p.form);
    if (p.form.requestSubmit) p.form.requestSubmit(p.submitter || undefined);
  }

  function renderWidgets() {
    if (!window.turnstile) return;
    var forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) {
      var f = forms[i];
      if (!isLeadForm(f) || widgetFor(f) !== null) continue;
      var box = document.createElement('div');
      box.className = 'nr-turnstile';
      box.style.cssText = 'margin:0;';
      var btn = submitButton(f);
      if (btn && btn.parentNode) btn.parentNode.insertBefore(box, btn);
      else f.appendChild(box);
      try {
        var id = window.turnstile.render(box, {
          sitekey: SITEKEY,
          appearance: 'interaction-only',
          size: 'flexible',
          action: 'lead',
          callback: onToken
        });
        widgets.push({ form: f, id: id });
      } catch (e) {}
    }
  }

  // Point plain (non-JavaScript) forms at /api/lead as well.
  function retargetForms() {
    var forms = document.querySelectorAll('form[action*="formsubmit.co"]');
    for (var i = 0; i < forms.length; i++) forms[i].setAttribute('action', window.NR_LEAD_ENDPOINT);
  }

  window.nrTurnstileReady = renderWidgets;
  var s = document.createElement('script');
  s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=nrTurnstileReady';
  s.async = true; s.defer = true;
  document.head.appendChild(s);

  document.addEventListener('DOMContentLoaded', function () {
    retargetForms();
    renderWidgets();
  });

  // Capture phase on window runs BEFORE each page's own submit handler,
  // so a blocked submit never reaches the code that sends the lead.
  window.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.tagName !== 'FORM' || !isLeadForm(form)) return;

    function hold(msg) {
      e.preventDefault();
      e.stopImmediatePropagation();
      if (msg) showNote(form, msg);
    }

    if (honeypotFilled(form)) {
      return hold('We couldn’t send that. Please call or text ' + PHONE + '.');
    }
    if (Date.now() - LOADED_AT < MIN_MS) {
      return hold('One moment — please press the button again.');
    }
    if (!tokenOf(form)) {
      // Turnstile hasn't finished yet: hold, then send automatically once it has.
      hold('Checking your request…');
      if (pending) clearTimeout(pending.timer);
      pending = {
        form: form,
        submitter: e.submitter,
        timer: setTimeout(function () {
          pending = null;
          showNote(form, 'We couldn’t verify this browser. Please try again, or call or text ' + PHONE + '.');
        }, 15000)
      };
      if (!window.turnstile) renderWidgets();
      return;
    }

    // Allowed through. Each token works once, so get a fresh one ready
    // in case this send fails and the person presses the button again.
    var id = widgetFor(form);
    setTimeout(function () {
      try { if (id !== null && window.turnstile) window.turnstile.reset(id); } catch (err) {}
    }, 1500);
  }, true);
})();
