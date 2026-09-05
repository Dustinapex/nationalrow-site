# -*- coding: utf-8 -*-
"""Shared chassis for National ROW project pages.
Keeps the existing site template (nav, form, footer, compliance) intact and adds
the components a real project page needs: status block, route map, county grid,
acquisition timeline, cited sources.
"""

GA_ID = "G-MX6ZT35QT3"
PHONE1 = "+14694847960"
PHONE1_D = "(469) 484-7960"
PHONE2 = "+19563634144"
PHONE2_D = "(956) 363-4144"

BASE_CSS = r"""
:root{
  --navy:#0d2340;
  --gold:#c9a227;
  --gold-light:#e8bf4a;
  --white:#fff;
  --light:#f5f7fa;
  --text:#1a1a2e;
  --logo:url("/national-row-logo.png");
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Arial','Helvetica Neue',Helvetica,sans-serif;color:var(--text);background:var(--white);line-height:1.6;}
a{color:var(--gold);text-decoration:none;}
img{max-width:100%;}

/* TOP BAR */
.topbar{background:var(--navy);color:rgba(255,255,255,.85);text-align:center;padding:8px 20px;font-size:13px;letter-spacing:.3px;}
.topbar a{color:var(--gold-light);font-weight:600;}
.topbar a:hover{color:#fff;}

/* NAV */
.sitenav{background:var(--white);border-bottom:3px solid var(--gold);padding:0 24px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200;box-shadow:0 2px 10px rgba(0,0,0,.1);height:70px;}
.brand-logo,.footer-brand-logo{display:block;height:46px;aspect-ratio:760/420;background:var(--logo) center/contain no-repeat;background-color:#fff;border-radius:10px;padding:6px 10px;box-sizing:content-box;}
.nav-cta{background:var(--gold);color:var(--navy)!important;font-weight:700;padding:11px 24px;border-radius:4px;font-size:15px;letter-spacing:.3px;transition:background .2s;}
.nav-cta:hover{background:var(--gold-light);}
.nav-links{display:flex;gap:24px;align-items:center;}
.nav-links a{color:var(--navy);font-size:14px;font-weight:600;}
.nav-links a:hover{color:var(--gold);}
@media(max-width:900px){.nav-links{display:none;}}

.alert-banner{background:#b91c1c;color:#fff;text-align:center;padding:13px 20px;font-size:14px;font-weight:600;letter-spacing:.2px;}
.alert-banner a{color:#fff;text-decoration:underline;}

/* HERO */
.hero{background:linear-gradient(135deg,#0a1c33 0%,var(--navy) 55%,#1a3a5c 100%);color:var(--white);padding:72px 24px 56px;text-align:center;}
.hero-badge{display:inline-block;background:var(--gold);color:var(--navy);font-size:11px;font-weight:700;letter-spacing:2px;padding:5px 18px;border-radius:20px;margin-bottom:22px;text-transform:uppercase;}
.hero h1{font-size:clamp(26px,4.5vw,50px);font-weight:900;line-height:1.12;margin-bottom:0;}
.hero h1 .gold{color:var(--gold);}
.hero-accent{width:56px;height:4px;background:var(--gold);margin:18px auto;border-radius:2px;}
.hero-sub{font-size:17px;opacity:.9;max-width:720px;margin:0 auto 32px;line-height:1.7;}
.hero-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
.btn-gold{background:var(--gold);color:var(--navy);font-weight:700;padding:14px 32px;border-radius:4px;font-size:16px;border:none;cursor:pointer;transition:background .2s;display:inline-block;}
.btn-gold:hover{background:var(--gold-light);}
.btn-outline{border:2px solid rgba(255,255,255,.7);color:var(--white);font-weight:700;padding:12px 28px;border-radius:4px;font-size:15px;transition:border-color .2s;}
.btn-outline:hover{border-color:#fff;}
.stats-row{display:flex;justify-content:center;flex-wrap:wrap;margin-top:48px;border-top:1px solid rgba(255,255,255,.15);padding-top:36px;}
.stat{flex:1;min-width:130px;padding:0 18px;border-right:1px solid rgba(255,255,255,.15);text-align:center;}
.stat:last-child{border-right:none;}
.stat-num{font-size:32px;font-weight:900;color:var(--gold);line-height:1;}
.stat-label{font-size:12px;opacity:.75;margin-top:6px;line-height:1.4;}

/* SECTIONS */
section{padding:64px 24px;}
.container{max-width:1080px;margin:0 auto;}
.container-narrow{max-width:820px;margin:0 auto;}
h2{font-size:clamp(22px,3.2vw,34px);font-weight:900;color:var(--navy);margin-bottom:14px;line-height:1.2;}
h3{font-size:19px;font-weight:800;color:var(--navy);margin:30px 0 10px;line-height:1.35;}
.section-sub{font-size:17px;color:#555;margin-bottom:30px;line-height:1.7;}
.section-alt{background:var(--light);}
.prose p{font-size:16px;line-height:1.8;color:#3d4351;margin-bottom:16px;}
.prose ul{margin:0 0 18px 22px;}
.prose li{font-size:16px;line-height:1.75;color:#3d4351;margin-bottom:8px;}
.prose strong{color:var(--navy);}

/* STATUS BLOCK */
.status-block{background:var(--navy);color:var(--white);border-radius:10px;padding:28px 30px;margin:0 0 34px;border-top:5px solid var(--gold);}
.status-head{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:10px;margin-bottom:18px;}
.status-head h3{color:var(--gold);font-size:14px;text-transform:uppercase;letter-spacing:1.6px;margin:0;}
.status-date{font-size:12px;color:rgba(255,255,255,.55);}
.status-pill{display:inline-block;background:#166534;color:#dcfce7;font-size:11px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;padding:5px 13px;border-radius:20px;margin-bottom:16px;}
.status-pill.pending{background:#854d0e;color:#fef3c7;}
.project-table{width:100%;border-collapse:collapse;}
.project-table td{padding:10px 0;border-bottom:1px solid rgba(255,255,255,.09);font-size:15px;vertical-align:top;}
.project-table tr:last-child td{border-bottom:none;}
.project-table td:first-child{color:var(--gold-light);font-weight:700;width:38%;font-size:12px;text-transform:uppercase;letter-spacing:.6px;padding-right:16px;}
.project-table a{color:var(--gold-light);text-decoration:underline;}

/* MAP */
.map-wrap{border:1px solid #d8dee7;border-radius:10px;overflow:hidden;box-shadow:0 3px 18px rgba(0,0,0,.08);background:#fff;}
#routeMap{height:520px;width:100%;background:#eef2f6;}
@media(max-width:640px){#routeMap{height:400px;}}
.map-bar{background:var(--navy);color:#fff;padding:14px 18px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
.map-bar input{flex:1;min-width:220px;border:none;border-radius:5px;padding:11px 14px;font-size:15px;font-family:inherit;}
.map-bar button{background:var(--gold);color:var(--navy);border:none;border-radius:5px;padding:11px 22px;font-weight:800;font-size:15px;cursor:pointer;}
.map-bar button:disabled{opacity:.6;cursor:wait;}
.map-note{font-size:12px;color:#6b7280;padding:12px 18px;background:#f9fafb;line-height:1.6;border-top:1px solid #e5e7eb;}
.map-result{padding:16px 18px;font-size:15px;line-height:1.6;border-top:1px solid #e5e7eb;display:none;}
.map-result.near{background:#fef2f2;color:#7f1d1d;}
.map-result.far{background:#f0fdf4;color:#14532d;}
.map-result.err{background:#fffbeb;color:#78350f;}
.map-result strong{display:block;font-size:17px;margin-bottom:4px;}
.map-legend{display:flex;gap:18px;flex-wrap:wrap;padding:12px 18px;font-size:13px;color:#4b5563;background:#fff;border-top:1px solid #e5e7eb;}
.map-legend span{display:flex;align-items:center;gap:7px;}
.swatch{width:22px;height:4px;border-radius:2px;display:inline-block;}

/* COUNTY GRID */
.county-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin-top:22px;}
.county-chip{background:#fff;border:1px solid #dbe1ea;border-left:4px solid var(--gold);border-radius:5px;padding:12px 14px;font-size:15px;font-weight:700;color:var(--navy);}
.county-chip small{display:block;font-weight:400;color:#6b7280;font-size:12px;margin-top:2px;}

/* TIMELINE */
.timeline{margin-top:26px;border-left:3px solid #e2e8f0;padding-left:0;list-style:none;}
.timeline li{position:relative;padding:0 0 30px 30px;}
.timeline li:last-child{padding-bottom:0;}
.timeline li::before{content:"";position:absolute;left:-9px;top:4px;width:15px;height:15px;border-radius:50%;background:#fff;border:3px solid var(--gold);}
.timeline li.done::before{background:var(--gold);}
.timeline h4{font-size:16px;font-weight:800;color:var(--navy);margin-bottom:6px;}
.timeline .when{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#6b7280;margin-bottom:6px;}
.timeline p{font-size:15px;color:#4b5563;line-height:1.7;}

/* CALLOUTS */
.urgency-box{background:#fffbeb;border-left:5px solid var(--gold);border-radius:4px;padding:18px 24px;margin:26px 0;font-size:15px;line-height:1.75;}
.urgency-box strong{color:#92400e;}
.note-box{background:#f1f5f9;border-left:5px solid #64748b;border-radius:4px;padding:18px 24px;margin:26px 0;font-size:14px;line-height:1.75;color:#475569;}
.note-box strong{color:#334155;}

/* NUMBER TABLE */
.num-table{width:100%;border-collapse:collapse;margin:22px 0;font-size:15px;}
.num-table th{background:var(--navy);color:#fff;text-align:left;padding:12px 14px;font-size:12px;text-transform:uppercase;letter-spacing:.8px;}
.num-table td{padding:12px 14px;border-bottom:1px solid #e5e7eb;}
.num-table tr:nth-child(even) td{background:#f9fafb;}
.num-table td:last-child{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;}
.num-table tfoot td{font-weight:800;color:var(--navy);border-top:2px solid var(--navy);background:#fff!important;}
/* Wide data tables must scroll inside themselves on a phone, never the page. */
@media(max-width:620px){
  .num-table{display:block;width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;font-size:14px;}
  .num-table th,.num-table td{padding:10px 10px;}
  .project-table{display:block;width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;}
  .project-table td:first-child{width:auto;min-width:118px;}
}

/* DAMAGES */
.damages-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:26px;}
.damage-card{background:var(--white);border-radius:8px;border-top:4px solid var(--gold);padding:24px;box-shadow:0 2px 14px rgba(0,0,0,.07);}
.damage-card h4{color:var(--navy);font-size:16px;margin-bottom:10px;font-weight:700;}
.damage-card p{font-size:14px;color:#555;line-height:1.65;}

/* HOW IT WORKS */
.how-section{background:var(--navy);}
.how-section h2{color:var(--white);}
.how-section .section-sub{color:rgba(255,255,255,.75);}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px;margin-top:32px;}
.step{background:rgba(255,255,255,.06);border-radius:8px;padding:28px;border:1px solid rgba(255,255,255,.08);}
.step-num{font-size:42px;font-weight:900;color:var(--gold);opacity:.7;line-height:1;margin-bottom:10px;}
.step h4{color:var(--white);font-size:16px;margin-bottom:8px;font-weight:700;}
.step p{color:rgba(255,255,255,.7);font-size:14px;line-height:1.65;}

/* SEGMENT CARDS (hub) */
.seg-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;margin-top:30px;}
.seg-card{background:#fff;border:1px solid #dbe1ea;border-top:5px solid var(--gold);border-radius:10px;padding:28px;box-shadow:0 3px 16px rgba(0,0,0,.06);display:flex;flex-direction:column;}
.seg-card h3{margin-top:0;font-size:21px;}
.seg-card .docket{font-size:12px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:#6b7280;margin-bottom:10px;}
.seg-card ul{list-style:none;margin:16px 0 20px;}
.seg-card li{font-size:14px;padding:7px 0;border-bottom:1px solid #eef1f5;color:#4b5563;display:flex;justify-content:space-between;gap:12px;}
.seg-card li:last-child{border-bottom:none;}
.seg-card li b{color:var(--navy);text-align:right;}
.seg-card .grow{flex:1;}

/* FAQ */
.faq-item{border-bottom:1px solid #e8edf3;padding:22px 0;}
.faq-item:last-child{border-bottom:none;}
.faq-item h4{font-size:17px;font-weight:700;color:var(--navy);margin-bottom:10px;line-height:1.4;}
.faq-item p{font-size:15px;color:#555;line-height:1.75;}
.faq-item p + p{margin-top:10px;}

/* SOURCES */
.sources{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:24px 28px;}
.sources h3{margin-top:0;font-size:14px;text-transform:uppercase;letter-spacing:1.4px;color:#64748b;}
.sources ol{margin:14px 0 0 20px;}
.sources li{font-size:14px;line-height:1.75;color:#475569;margin-bottom:10px;}
.sources a{color:#1d4ed8;text-decoration:underline;word-break:break-word;}

/* HANDOFF */
.handoff{background:linear-gradient(135deg,#0a1c33,#1a3a5c);color:#fff;padding:56px 24px;text-align:center;}
.handoff h2{color:#fff;}
.handoff p{color:rgba(255,255,255,.85);font-size:17px;max-width:640px;margin:0 auto 26px;line-height:1.7;}

/* PROOF BAND - documented results. Deliberately compact: the numbers are the
   point, everything else is trimmed to the smallest thing that still reads. */
.proofband{background:var(--gold);padding:24px 22px;}
.proofband .inner{max-width:1160px;margin:0 auto;}
.proofband .top{display:flex;align-items:baseline;gap:8px 18px;flex-wrap:wrap;margin-bottom:14px;}
.proofband h2{color:var(--navy);font-size:20px;margin:0;line-height:1.2;}
.proofband .hl{color:rgba(11,31,58,.72);font-size:14px;font-weight:600;line-height:1.4;margin:0;}
.proofband .cols{display:grid;grid-template-columns:repeat(4,1fr);gap:0;}
.proofband .col{padding:0 18px;border-left:1px solid rgba(11,31,58,.22);}
.proofband .col:first-child{padding-left:0;border-left:none;}
.proofband .where{color:rgba(11,31,58,.7);font-size:10.5px;letter-spacing:.6px;text-transform:uppercase;font-weight:700;line-height:1.4;margin-bottom:6px;min-height:30px;}
.proofband .nums{color:var(--navy);font-size:clamp(17px,1.75vw,22px);font-weight:900;letter-spacing:-.5px;line-height:1.25;}
.proofband .nums .ar{margin:0 5px;font-weight:700;}
.proofband .pct{font-size:13.5px;font-weight:800;white-space:nowrap;letter-spacing:0;display:inline-block;}
.proofband .whytxt{color:rgba(11,31,58,.78);font-size:12.5px;line-height:1.45;font-weight:600;margin-top:6px;}
.proofband .act{margin-top:16px;border-top:1px solid rgba(11,31,58,.22);padding-top:13px;
  display:flex;align-items:baseline;gap:4px 14px;flex-wrap:wrap;}
.proofband .act h3{color:var(--navy);font-size:15px;margin:0;}
.proofband .act p{color:rgba(11,31,58,.78);font-size:13.5px;line-height:1.5;margin:0;flex:1 1 220px;}
.proofband .act a{color:var(--navy);font-weight:800;font-size:14px;text-decoration:none;border-bottom:2px solid rgba(11,31,58,.45);padding-bottom:1px;white-space:nowrap;}
.proofband .act a:hover{border-bottom-color:var(--navy);}
.proofband .fine{color:rgba(11,31,58,.62);font-size:11.5px;line-height:1.5;margin:11px 0 0;}
@media(max-width:1150px){
  .proofband .cols{grid-template-columns:1fr 1fr;gap:18px 0;}
  .proofband .col:nth-child(odd){padding-left:0;border-left:none;}
}
@media(max-width:560px){
  .proofband{padding:22px 20px;}
  .proofband .cols{grid-template-columns:1fr;gap:0;}
  .proofband .col{padding:13px 0;border-left:none;border-top:1px solid rgba(11,31,58,.22);}
  .proofband .col:first-child{border-top:none;padding-top:0;}
  .proofband .where{min-height:0;margin-bottom:4px;}
  .proofband .nums{font-size:21px;}
}

/* INLINE CTA BAND */
.cta-band{background:#fbf7ec;border-top:3px solid var(--gold);border-bottom:1px solid #e6dcc2;padding:38px 24px;}
.cta-band .inner{max-width:760px;margin:0 auto;text-align:center;}
.cta-band h3{font-size:clamp(19px,2.4vw,25px);color:var(--navy);margin:0 0 12px;line-height:1.3;}
.cta-band p{font-size:16px;line-height:1.7;color:#3d4a5c;margin:0 auto 22px;max-width:620px;}
.cta-band .btn-gold{font-size:16px;}
.cta-band .alt{margin-top:16px;font-size:15px;color:#5a6674;}
.cta-band .alt a{color:#1d4ed8;font-weight:700;text-decoration:none;}
.cta-band .alt a:hover{text-decoration:underline;}

/* CONTACT + FORM */
.contact-strip{background:var(--navy);color:var(--white);padding:32px 24px;text-align:center;border-bottom:1px solid rgba(255,255,255,.08);}
.contact-strip .phones{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-top:12px;font-size:22px;font-weight:900;}
.contact-strip .phones a{color:var(--gold);}
.form-section{background:var(--navy);padding:64px 24px;}
.form-header{text-align:center;color:var(--white);margin-bottom:32px;}
.form-header h2{color:var(--white);font-size:clamp(22px,3vw,32px);}
.form-header p{color:rgba(255,255,255,.78);margin-top:10px;font-size:16px;}
.form-body{background:var(--white);border-radius:10px;padding:36px;max-width:720px;margin:0 auto;box-shadow:0 8px 40px rgba(0,0,0,.25);}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
@media(max-width:580px){.form-grid{grid-template-columns:1fr;}}
.form-group{display:flex;flex-direction:column;gap:6px;}
.form-group.full{grid-column:1/-1;}
label{font-size:12.5px;font-weight:700;color:var(--navy);text-transform:uppercase;letter-spacing:.6px;}
input,select,textarea{border:1.5px solid #d1d5db;border-radius:5px;padding:13px 14px;font-size:16px;font-family:inherit;width:100%;background:#fff;min-height:46px;box-sizing:border-box;}
textarea{min-height:104px;}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,162,39,.15);}
.tcpa-text{font-size:11px;color:#6b7280;line-height:1.65;margin:18px 0 4px;padding:12px;background:#f9fafb;border-radius:5px;border:1px solid #e5e7eb;}
.form-disclaimer{font-size:12px;color:#8b93a1;margin-top:12px;line-height:1.6;}
.submit-btn{background:var(--gold);color:var(--navy);font-weight:700;font-size:17px;padding:16px 28px;border:none;border-radius:5px;cursor:pointer;width:100%;margin-top:14px;min-height:52px;line-height:1.25;}
.submit-btn:hover{background:var(--gold-light);}
.form-subtext{text-align:center;font-size:13px;color:#6b7280;margin-top:12px;}
.form-success{display:none;text-align:center;padding:40px 20px;}
.form-success h3{color:var(--navy);font-size:24px;margin-bottom:12px;}
.form-success p{color:#555;font-size:16px;line-height:1.7;}
.form-success .phones{margin-top:20px;font-size:18px;font-weight:700;}
.form-success .phones a{color:var(--gold);}

/* FOOTER */
footer{background:#050e1c;color:rgba(255,255,255,.55);padding:48px 24px 32px;text-align:center;}
.footer-brand-logo{margin:0 auto 16px;}
.footer-tagline{font-size:13px;color:rgba(255,255,255,.45);margin-bottom:20px;}
.footer-links{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin:0 0 20px;font-size:13px;}
.footer-links a{color:rgba(255,255,255,.55);}
.footer-links a:hover{color:var(--gold);}
.footer-phones{font-size:14px;margin-bottom:6px;}
.footer-phones a{color:var(--gold-light);font-weight:600;}
.footer-email a{color:rgba(255,255,255,.55);}
.footer-copy{font-size:12px;margin-top:20px;color:rgba(255,255,255,.35);}
.footer-disclaimer{font-size:11px;color:rgba(255,255,255,.3);max-width:760px;margin:14px auto 0;line-height:1.65;}
"""

TOPBAR_NAV = """
<div class="topbar">
  Nationwide Service &nbsp;·&nbsp; HQ in Texas &nbsp;&nbsp;|&nbsp;&nbsp;
  Call or text &nbsp;<a href="tel:+14694847960">(469) 484-7960</a>
  &nbsp;&nbsp;
  <a href="tel:+19563634144">(956) 363-4144</a>
  &nbsp;&nbsp;
  <a href="mailto:info@nationalrow.com">info@nationalrow.com</a>
</div>

<nav class="sitenav">
  <a href="https://nationalrow.com" aria-label="National ROW home">
    <span class="brand-logo" role="img" aria-label="National ROW — On the owner's side of the right-of-way"></span>
  </a>
  <div class="nav-links">
    <a href="https://nationalrow.com/#how">How it works</a>
    <a href="/services/">What we handle</a>
    <a href="/projects/">Projects</a>
    <a href="https://nationalrow.com/blog/">Blog</a>
    <a href="https://nationalrow.com/about/">About</a>
    <a href="/faq/">FAQ</a>
    <a href="https://nationalrow.com/states/texas/">Texas</a>
  </div>
  <a class="nav-cta" href="#contact">Free Case Review</a>
</nav>
"""


def form_section(project_source, heading="Get Your Free Case Review"):
    return """
<div class="contact-strip" id="contact">
  <p style="font-size:16px;font-weight:700;">Call or text us directly — we answer owners same day.</p>
  <div class="phones">
    <a href="tel:+14694847960">(469) 484-7960</a>
    <a href="tel:+19563634144">(956) 363-4144</a>
  </div>
  <p><a href="mailto:info@nationalrow.com" style="color:rgba(255,255,255,.7)">info@nationalrow.com</a></p>
</div>

<section class="form-section">
  <div class="container">
    <div class="form-header">
      <h2>%s</h2>
      <p>Tell us about your property. A senior consultant reads every one of these and calls you within the hour, 8am&ndash;6pm Central, Monday to Friday. Outside those hours, first thing the next morning.</p>
    </div>
    <div class="form-body">
      <div id="the-form">
        <form id="leadForm" novalidate>
          <input type="hidden" name="_subject" value="New case review — %s">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_cc" value="dustin@apexfreedomfund.com,chris@apexfreedomfund.com">
          <input type="hidden" name="project_source" id="projectSource" value="%s">
          <input type="hidden" name="referrer_url" id="referrerUrl" value="">
          <div class="form-grid">
            <div class="form-group"><label>First Name *</label><input type="text" name="first_name" required placeholder="First name"></div>
            <div class="form-group"><label>Last Name *</label><input type="text" name="last_name" required placeholder="Last name"></div>
            <div class="form-group"><label>Phone *</label><input type="tel" name="phone" required placeholder="(___) ___-____"></div>
            <div class="form-group"><label>Email</label><input type="email" name="email" placeholder="you@email.com"></div>
            <div class="form-group"><label>County &amp; State</label><input type="text" name="county_state" id="countyState" placeholder="e.g. Coke, TX"></div>
            <div class="form-group"><label>Approx. Acreage</label><input type="text" name="acreage" placeholder="e.g. 42"></div>
            <div class="form-group"><label>Property Type</label><select name="property_type"><option value="">Select…</option><option>Agricultural / Ranch</option><option>Residential</option><option>Commercial</option><option>Vacant Land</option><option>Other</option></select></div>
            <div class="form-group"><label>Where are you in the process?</label><select name="stage"><option value="">Select…</option><option>Nothing yet — I just heard about the project</option><option>They asked permission to survey</option><option>An appraiser has been out</option><option>I have a written offer</option><option>I&#39;ve been sued / served with condemnation papers</option></select></div>
            <div class="form-group full"><label>Affected property address</label><input type="text" name="address" id="propAddress" placeholder="Street address, parcel/APN, or legal description"></div>
            <div class="form-group full"><label>What have they sent so far?</label><textarea name="details" rows="4" placeholder="A letter, an offer, an appraisal, an easement document, a survey crew…"></textarea></div>
          </div>
          <div class="tcpa-text">By submitting this form, you agree that National ROW may contact you by phone, text message (SMS), and email at the number and address provided — including by automated means — about your inquiry. Consent is not a condition of any service. Message and data rates may apply. Message frequency may vary. Reply STOP to opt out of texts, HELP for help. See our <a href="https://nationalrow.com/privacy-policy" style="color:var(--gold)">Privacy Policy</a>.</div>
          <button class="submit-btn" type="submit">Free review by a senior consultant →</button>
          <div class="form-subtext">No obligation · Zero out of pocket · Private · We'll never sell your info</div>
          <p class="form-disclaimer">National ROW is a right-of-way consulting firm, not a law firm. No attorney-client relationship is created by submitting this form. Results vary by case. Prior results do not guarantee similar outcomes.</p>
        </form>
      </div>
      <div class="form-success" id="formSuccess">
        <h3>We've got it from here.</h3>
        <p>Your case is in review. A senior consultant reads everything you shared and calls you within the hour, 8am&ndash;6pm Central, Monday to Friday. Outside those hours, first thing the next morning.</p>
        <p style="margin-top:12px;">In the meantime, <strong>don't sign anything</strong> and don't feel pressured to respond to their representatives.</p>
        <div class="phones">Need to talk now? Call or text &nbsp;<a href="tel:+14694847960">(469) 484-7960</a> &nbsp;·&nbsp; <a href="tel:+19563634144">(956) 363-4144</a></div>
      </div>
    </div>
  </div>
</section>
""" % (heading, project_source, project_source)


FOOTER = """
<footer>
  <a href="https://nationalrow.com" aria-label="National ROW home">
    <span class="footer-brand-logo" role="img" aria-label="National ROW"></span>
  </a>
  <p class="footer-tagline">Eminent domain and condemnation consulting for property owners — highway, utility, pipeline, and every type of right-of-way.</p>
  <div class="footer-links">
    <a href="https://nationalrow.com">Home</a>
    <a href="https://nationalrow.com/#how">How it works</a>
    <a href="/projects/">Projects</a>
    <a href="https://nationalrow.com/blog/">Blog</a>
    <a href="https://nationalrow.com/about/">About</a>
    <a href="https://nationalrow.com/states/texas/">Texas</a>
    <a href="https://nationalrow.com/privacy-policy">Privacy Policy</a>
  </div>
  <div class="footer-phones">
    Call or text &nbsp;<a href="tel:+14694847960">(469) 484-7960</a> &nbsp;·&nbsp;
    <a href="tel:+19563634144">(956) 363-4144</a>
  </div>
  <div class="footer-email"><a href="mailto:info@nationalrow.com">info@nationalrow.com</a></div>
  <div class="footer-copy">© National ROW. Maximizing compensation for property owners since the 1980s.</div>
  <div class="footer-disclaimer">National ROW is a right-of-way and condemnation consulting firm. We are not a law firm and do not provide legal advice. No attorney-client relationship is formed by visiting this site or submitting a contact form. Information on this page is compiled from public records and is provided for general information only; it is not legal advice and may not reflect the most recent filings. Verify project details with the Public Utility Commission of Texas or the utility before acting. Results vary by case. Prior results do not guarantee similar outcomes.</div>
</footer>
"""

FORM_SCRIPT = """
<script>
(function(){
  var f = document.getElementById('leadForm');
  if(!f) return;
  var ru = document.getElementById('referrerUrl');
  if(ru) ru.value = location.href;
  f.addEventListener('submit', async function(e){
    e.preventDefault();
    var btn = this.querySelector('.submit-btn');
    btn.disabled = true; btn.textContent = 'Sending…';
    var data = new FormData(this);
    try{
      var res = await fetch('https://formsubmit.co/ajax/info@nationalrow.com', {
        method:'POST', headers:{'Accept':'application/json'}, body:data
      });
      if(res.ok){
        document.getElementById('the-form').style.display='none';
        document.getElementById('formSuccess').style.display='block';
        if(window.gtag) gtag('event','generate_lead',{project: (document.getElementById('projectSource')||{}).value || ''});
      } else { throw new Error('bad status'); }
    }catch(err){
      btn.disabled=false; btn.textContent='Free review by a senior consultant →';
      alert("Couldn't send just now — please call or text (469) 484-7960 or (956) 363-4144 and we'll take your details.");
    }
  });
})();
</script>
"""


def head(title, description, canonical, schema_json, extra_head=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="article">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="https://nationalrow.com/og-image.png">
<meta property="og:url" content="%s">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="https://nationalrow.com/favicon.ico">
<link rel="apple-touch-icon" href="https://nationalrow.com/favicon.png">
<script type="application/ld+json">
%s
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '%s');
</script>
%s
<style>%s</style>
</head>
<body>
""" % (title, description, canonical, title, description, canonical, schema_json, GA_ID, GA_ID, extra_head, BASE_CSS)
