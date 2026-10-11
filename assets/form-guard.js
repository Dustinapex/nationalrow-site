/* National ROW — form guard (spam protection for every lead form on the site).
 *
 * Loaded in <head> of every page that has a lead form.
 *  1. NR_LEAD_ENDPOINT is the ONE place the site's AJAX forms send leads.
 *     Change it here and every form on the site follows.
 *  2. Honeypot: hidden fields (_honey / website) that people never see.
 *     If one is filled in, a bot filled it, and the form is not sent.
 *  3. Speed check: nobody types a name, phone and email in under 3 seconds.
 *     A submit that fast is held, with a note asking a person to press again.
 *  4. Real-data checks: the phone must be a real-format 10-digit US number,
 *     the email a real-looking address (no throwaway inboxes), names must be
 *     names, and no web links in the short fields. The visitor is told
 *     exactly which box to fix. Only filled-in boxes are checked; which boxes
 *     are required is still decided by each page.
 */
(function () {
  'use strict';

  window.NR_LEAD_ENDPOINT = 'https://formsubmit.co/ajax/info@nationalrow.com';

  var LOADED_AT = Date.now();
  var MIN_MS = 3000;
  var PHONE = '(469) 484-7960';

  var ES = /^es/i.test(document.documentElement.lang || '');
  var MSG = ES ? {
    wait: 'Un momento — por favor presione el botón otra vez.',
    trap: 'No pudimos enviar esto. Llame o envíe un texto al ' + PHONE + '.',
    phone: 'Ingrese un número de teléfono de EE. UU. válido de 10 dígitos.',
    email: 'Ingrese una dirección de correo electrónico válida.',
    tempmail: 'Use su correo electrónico habitual, no uno temporal.',
    name: 'Ingrese su nombre real.',
    link: 'Quite los enlaces web de este campo.',
    links: 'Incluya como máximo un enlace web en su mensaje.'
  } : {
    wait: 'One moment — please press the button again.',
    trap: 'We couldn’t send that. Please call or text ' + PHONE + '.',
    phone: 'Please enter a valid 10-digit US phone number.',
    email: 'Please enter a valid email address.',
    tempmail: 'Please use your regular email address, not a temporary one.',
    name: 'Please enter your real name.',
    link: 'Please remove web links from this box.',
    links: 'Please include no more than one web link in your message.'
  };

  // Throwaway / disposable inbox services and placeholder domains.
  var TEMP_DOMAINS = ('mailinator.com guerrillamail.com guerrillamail.net guerrillamailblock.com sharklasers.com ' +
    'grr.la 10minutemail.com 10minutemail.net tempmail.com temp-mail.org temp-mail.io tempmail.net tempmailo.com ' +
    'tempr.email yopmail.com yopmail.net trashmail.com trashmail.de throwawaymail.com getnada.com nada.email ' +
    'dispostable.com maildrop.cc fakeinbox.com mintemail.com mohmal.com emailondeck.com burnermail.io ' +
    'mailnesia.com mytemp.email spamgourmet.com moakt.com tmail.ws tmpmail.org discard.email mailcatch.com ' +
    'example.com example.org example.net test.com test.org email.com domain.com').split(' ');
  var JUNK_WORDS = ['test', 'testing', 'asdf', 'asdfgh', 'qwerty', 'none', 'na', 'n/a', 'xxx', 'aaa', 'abc', 'fake', 'nobody', 'anonymous'];
  var URL_RX = /(https?:\/\/|www\.|\b[a-z0-9-]+\.(com|net|org|ru|cn|xyz|top|info|biz|io|co)\/)/i;

  function badPhone(v) {
    var d = v.replace(/\D/g, '');
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    if (d.length !== 10) return true;
    if (!/^[2-9]\d{2}[2-9]\d{6}$/.test(d)) return true;   // US area code + exchange rules
    if (/^(\d)\1{9}$/.test(d)) return true;               // 2222222222 etc.
    if (d === '1234567890' || d === '9876543210') return true;
    if (/^\d{3}5550[1][0-9]{2}$/.test(d)) return true;   // 555-0100..0199 reserved fictional
    return false;
  }

  function emailProblem(v) {
    v = v.trim().toLowerCase();
    if (!/^[a-z0-9._%+\-']+@[a-z0-9.\-]+\.[a-z]{2,}$/.test(v) || /\.\./.test(v)) return MSG.email;
    var domain = v.split('@')[1];
    for (var i = 0; i < TEMP_DOMAINS.length; i++) {
      var t = TEMP_DOMAINS[i];
      if (domain === t || domain.slice(-(t.length + 1)) === '.' + t) return MSG.tempmail;
    }
    var local = v.split('@')[0];
    if (JUNK_WORDS.indexOf(local) !== -1 && domain.indexOf('nationalrow.com') === -1) return MSG.email;
    return '';
  }

  function badName(v) {
    v = v.trim();
    if (!/[A-Za-zÀ-ɏ]/.test(v)) return true;    // must contain letters
    if (/\d{2,}/.test(v)) return true;                    // no number strings
    if (URL_RX.test(v) || /[@<>{}\[\]\\\/=]/.test(v)) return true;
    if (v.length > 60) return true;
    if (/(.)\1{3,}/i.test(v)) return true;                // aaaa, xxxx
    if (JUNK_WORDS.indexOf(v.toLowerCase()) !== -1) return true;
    return false;
  }

  var NAME_RX = /^(first_?name|last_?name|firstname|lastname|name)(_es)?$/i;
  var SHORT_RX = /^(location|county_state|county|parcel_?address|parceladdress|address|acreage|project)(_es)?$/i;

  function checkData(form) {
    var els = form.querySelectorAll('input, textarea');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var type = (el.getAttribute('type') || (el.tagName === 'TEXTAREA' ? 'textarea' : 'text')).toLowerCase();
      if (type === 'hidden' || type === 'checkbox' || type === 'radio' || type === 'submit') continue;
      if (el.name === '_honey' || el.name === 'website') continue;
      var v = (el.value || '').trim();
      if (!v) continue;
      var msg = '';
      if (type === 'tel' || /phone/i.test(el.name)) { if (badPhone(v)) msg = MSG.phone; }
      else if (type === 'email' || /email/i.test(el.name)) { msg = emailProblem(v); }
      else if (NAME_RX.test(el.name)) { if (badName(v)) msg = MSG.name; }
      else if (type === 'textarea') { if ((v.match(/https?:\/\/|www\./gi) || []).length > 1) msg = MSG.links; }
      else if (SHORT_RX.test(el.name)) { if (URL_RX.test(v)) msg = MSG.link; }
      if (msg) return { el: el, msg: msg };
    }
    return null;
  }

  function honeypotFilled(form) {
    var traps = form.querySelectorAll('input[name="_honey"], input[name="website"]');
    for (var i = 0; i < traps.length; i++) {
      if (traps[i].value && traps[i].value.trim() !== '') return true;
    }
    return false;
  }

  function showNote(form, text) {
    var n = form.querySelector('.nr-guard-note');
    if (!n) {
      n = document.createElement('p');
      n.className = 'nr-guard-note';
      n.setAttribute('role', 'alert');
      n.style.cssText = 'margin:10px 0 0;font-size:14px;line-height:1.4;color:#b45309;font-weight:600;';
      var btn = form.querySelector('button[type="submit"], input[type="submit"], .submit-btn, button:not([type])');
      if (btn && btn.parentNode) btn.parentNode.insertBefore(n, btn.nextSibling);
      else form.appendChild(n);
    }
    n.textContent = text;
  }

  function flagField(form, el, text) {
    showNote(form, text);
    el.setAttribute('aria-invalid', 'true');
    el.style.outline = '2px solid #b45309';
    el.style.outlineOffset = '1px';
    try { el.focus({ preventScroll: false }); } catch (e) { el.focus(); }
    var clear = function () {
      el.removeAttribute('aria-invalid');
      el.style.outline = '';
      el.style.outlineOffset = '';
      el.removeEventListener('input', clear);
    };
    el.addEventListener('input', clear);
  }

  // Capture phase on window runs BEFORE each page's own submit handler,
  // so a blocked submit never reaches the code that sends the lead.
  window.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.tagName !== 'FORM') return;

    function hold() { e.preventDefault(); e.stopImmediatePropagation(); }

    if (honeypotFilled(form)) { hold(); showNote(form, MSG.trap); return; }
    if (Date.now() - LOADED_AT < MIN_MS) { hold(); showNote(form, MSG.wait); return; }

    var bad = checkData(form);
    if (bad) { hold(); flagField(form, bad.el, bad.msg); return; }

    var old = form.querySelector('.nr-guard-note');
    if (old) old.parentNode.removeChild(old);
  }, true);
})();
