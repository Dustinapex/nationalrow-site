/* National ROW — form guard (spam protection for every lead form on the site).
 *
 * Loaded in <head> of every page that has a lead form.
 *  1. NR_LEAD_ENDPOINT is the ONE place the site's AJAX forms send leads.
 *     Change it here and every form on the site follows.
 *  2. Honeypot: hidden fields (_honey / website) that people never see.
 *     If one is filled in, a bot filled it, and the form is not sent.
 *  3. Speed check: nobody types a name, phone and email in under 3 seconds.
 *     A submit that fast is held, with a note asking a person to press again.
 */
(function () {
  'use strict';

  window.NR_LEAD_ENDPOINT = 'https://formsubmit.co/ajax/info@nationalrow.com';

  var LOADED_AT = Date.now();
  var MIN_MS = 3000;
  var PHONE = '(469) 484-7960';

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
      n.setAttribute('role', 'status');
      n.style.cssText = 'margin:10px 0 0;font-size:14px;line-height:1.4;color:#b45309;font-weight:600;';
      var btn = form.querySelector('button[type="submit"], input[type="submit"], .submit-btn, button:not([type])');
      if (btn && btn.parentNode) btn.parentNode.insertBefore(n, btn.nextSibling);
      else form.appendChild(n);
    }
    n.textContent = text;
  }

  // Capture phase on window runs BEFORE each page's own submit handler,
  // so a blocked submit never reaches the code that sends the lead.
  window.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.tagName !== 'FORM') return;

    if (honeypotFilled(form)) {
      e.preventDefault();
      e.stopImmediatePropagation();
      showNote(form, 'We couldn’t send that. Please call or text ' + PHONE + '.');
      return;
    }

    if (Date.now() - LOADED_AT < MIN_MS) {
      e.preventDefault();
      e.stopImmediatePropagation();
      showNote(form, 'One moment — please press the button again.');
      return;
    }
  }, true);
})();
