#!/usr/bin/env python3
"""
Ashfaq Tailor — page generator (OPTIONAL, for developers).

The finished website is plain HTML in the main folder, so you do NOT need this
to run or deploy the site. Use it only if you want to regenerate all pages after
changing wording / sections in bulk:   python3 tools/generate.py

Contact details (phone, WhatsApp, hours, map, social, banner, reviews, analytics)
live in js/site-config.js — not here.
"""
import glob, html, json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://YOUR-DOMAIN.com"          # replaced by tools/set_domain.py
LASTMOD = "2026-10-24"

# ------------------------------------------------------------------ icons
WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-.9 1.1-.3.2-.6.1c-.3-.1-1.2-.4-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5s-.7-1.6-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.5 1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 3 1.3 3 .9 3.6.8.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-2.9-.4-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.200z"/></svg>'
def _s(inner): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
PHONE = _s('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>')
PIN = _s('<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>')
CLOCK = _s('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>')
ICONS = {
    "shirt": '<path d="M8 3 3 6l2 4 3-1v12h8V9l3 1 2-4-5-3c-1 2-2.500 3-4 3S9 5 8 3z"/>',
    "pant": '<path d="M7 3h10l1 18h-4l-2-10-2 10H6z"/>',
    "vest": '<path d="M8 3l4 5 4-5 3 3v14l-4-1-3 2-3-2-4 1V6z"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.100 15.900M14.500 14.500 20 20M8.100 8.100 12 12"/>',
    "tape": '<rect x="2" y="8" width="20" height="8" rx="1"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/>',
    "needle": '<path d="M20 4 6 18"/><path d="M6 18c-2 0-3 2-2 3 1 1 3 0 3-2"/><circle cx="18" cy="6" r="1"/>',
    "spark": '<path d="M12 3l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/>',
    "hanger": '<path d="M12 6a2 2 0 1 0-2-2M12 6v2L3 15a1 1 0 0 0 .6 1.800h16.800A1 1 0 0 0 21 15l-9-7"/>',
}
def icon(name): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

# ------------------------------------------------------------------ data
SERVICES = [
    dict(id="shalwar-kameez", name="Shalwar Kameez Stitching", icon="shirt",
         short="Clean collars, plackets and cuffs, stitched to your measurements.",
         long="Everyday and occasion shalwar kameez, stitched to your measurements with neat finishing.",
         points=["Choose your collar, placket and cuff style", "Fitting and length discussed before stitching", "Send a photo of the design you like on WhatsApp"],
         img="portfolio/ashfaq-tailor-shalwar-kameez-cream-gold-placket-faisalabad", alt="Cream shalwar kameez with a gold contrast placket and cuff"),
    dict(id="kurta", name="Kurta Stitching", icon="hanger",
         short="Kurtas in the neckline, placket and cuff style you choose.",
         long="Kurtas made in the neckline, placket and cuff style you prefer, finished neatly.",
         points=["Band-collar and other neckline styles", "Detail work such as contrast piping and stitching", "Regular, slim or relaxed fit"],
         img="portfolio/ashfaq-tailor-kurta-cream-cross-stitch-collar-faisalabad", alt="Cream kurta collar with small cross-stitch patterns"),
    dict(id="shirt", name="Shirt Stitching", icon="shirt",
         short="Formal and casual shirts with the collar and cuff you prefer.",
         long="Formal and casual shirts with the collar, placket and cuff style you prefer.",
         points=["Collar, placket and cuff options", "Contrast trims and detail stitching", "Fit discussed with you before we start"],
         img="portfolio/ashfaq-tailor-shirt-navy-contrast-stitch-faisalabad", alt="Navy shirt with red and white contrast stitch trim"),
    dict(id="pant", name="Pant / Trouser Stitching", icon="pant",
         short="Trousers cut for your waist, length and preferred fit.",
         long="Comfortable trousers cut for your waist, length and preferred fit.",
         points=["Measured for waist, length and fit", "Regular, slim or relaxed cut", "Ask us about pockets and finishing"],
         img=None, alt=""),
    dict(id="waistcoat", name="Waistcoat Stitching / Fitting", icon="vest",
         short="Waistcoats made or fitted to sit properly.",
         long="Waistcoats made, or fitted to sit properly, for weddings and special occasions.",
         points=["New waistcoat stitching", "Fitting adjustments", "Plan ahead for special occasions"],
         img=None, alt=""),
    dict(id="alterations", name="Alterations", icon="scissors",
         short="Adjust length and fit on clothes you already own.",
         long="Length, width and fitting adjustments so the clothes you already own fit properly.",
         points=["Length and width adjustments", "Fitting improvements", "Bring the garment to the shop or message us first"],
         img=None, alt=""),
    dict(id="custom-fitting", name="Custom Fitting", icon="tape",
         short="Regular, slim or relaxed — stitched to how you like to wear it.",
         long="Tell us your preferred fit — regular, slim or relaxed — and we stitch to it.",
         points=["Measurements taken for you", "Fit preference discussed", "Use Choose Your Style on the home page"],
         img=None, alt=""),
    dict(id="other", name="Other Tailoring Services", icon="needle",
         short="Something not listed? Ask us on WhatsApp.",
         long="Need something that is not listed? Ask us on WhatsApp and we will tell you if we can help.",
         points=["Send a photo or describe what you need", "We will reply with what is possible"],
         img=None, alt=""),
]

CATS = {"shalwar-kameez": "Shalwar Kameez", "kurta": "Kurta", "shirts": "Shirts"}
P = "portfolio/ashfaq-tailor-"
WORK = [
    ("kameez-cream", "shalwar-kameez", "Cream kameez with gold contrast placket", P + "shalwar-kameez-cream-gold-placket-faisalabad", "Cream shalwar kameez with a mustard-gold contrast placket and cuff, shown close up"),
    ("shirt-navy", "shirts", "Navy shirt with contrast stitch trim", P + "shirt-navy-contrast-stitch-faisalabad", "Folded navy shirt with red and white stitched trim on the collar, placket, pocket and cuff"),
    ("kurta-white", "kurta", "White kurta with blue inner detail", P + "kurta-white-blue-inner-detail-faisalabad", "Folded white band-collar kurta with a chest pocket and blue inner detail on a blue checked cloth"),
    ("kameez-black", "shalwar-kameez", "Black kameez with mustard piping", P + "shalwar-kameez-black-mustard-piping-faisalabad", "Folded black kameez with mustard piping and white contrast stitching on the collar and placket"),
    ("shirt-brown", "shirts", "Brown shirt with black collar contrast", P + "shirt-brown-black-collar-faisalabad", "Folded brown shirt with black and white contrast on the collar, placket and cuff"),
    ("kurta-cream", "kurta", "Cream kurta with cross-stitch collar", P + "kurta-cream-cross-stitch-collar-faisalabad", "Hand holding the collar of a cream kurta with small cross-stitch patterns and two button studs"),
    ("kameez-grey", "shalwar-kameez", "Grey kameez with blue and white trim", P + "shalwar-kameez-grey-stripe-trim-faisalabad", "Folded grey kameez with a blue and white striped trim down the placket and collar"),
    ("shirt-blue", "shirts", "Light blue shirt with striped placket", P + "shirt-blue-stripe-placket-faisalabad", "Light blue shirt with a striped placket, cross-stitch collar details and a patterned inner collar"),
    ("shirt-grey", "shirts", "Grey shirt with round collar", P + "shirt-grey-round-collar-faisalabad", "Grey shirt with a rounded collar, hidden placket and two-button cuffs"),
]
HOME_WORK = ["kameez-cream", "shirt-navy", "kurta-cream", "kameez-black", "shirt-brown", "shirt-blue"]

INSIDE = [
    ("shop/ashfaq-tailor-shop-interior-workspace-faisalabad", "Inside Ashfaq Tailor: sewing machines, a cutting table and men's fashion posters on the wall"),
    ("shop/ashfaq-tailor-shop-interior-thread-wall-faisalabad", "Wall of thread boxes on red shelves with warm lighting"),
    ("shop/ashfaq-tailor-shop-interior-overlock-corner-faisalabad", "Corner of the shop with thread racks, trims and an overlock machine on a blue-edged table"),
    ("shop/ashfaq-tailor-shop-interior-sewing-corner-faisalabad", "Sewing corner with an overlock machine, thread shelves and a green chair"),
]

FAQS = [
    ("How can I place a stitching order?",
     "Message us on WhatsApp or call to tell us what you need. Then visit the shop to confirm your measurements and style, and we will prepare your clothes."),
    ("Do I need to visit the shop for measurements?",
     "Measurements are normally taken at the shop so the fit is right. If visiting is difficult for you, message us on WhatsApp and ask."),
    ("Do you provide alterations?",
     "Yes, alterations are one of our services. Message us or bring the garment to the shop and we will tell you what can be done."),
    ("Can I send a design picture on WhatsApp?",
     "Yes. Send us a photo of the style you like on WhatsApp and we will discuss it with you."),
    ("Where is Ashfaq Tailor located?",
     "We are at Street No. 1, Iqbal Town, GM Abad, Faisalabad, Pakistan. Use the Get Directions button to open the route in Google Maps."),
    ("How can I contact Ashfaq Tailor?",
     "Message us on WhatsApp, call us, or visit the shop. All contact details are on our Contact page."),
    ("What types of clothes do you stitch?",
     "Shalwar kameez, kurta, shirts and pants, plus waistcoat stitching and fitting, alterations and custom fitting. For anything else, just ask."),
    ("How long does stitching take?",
     "It depends on the garment and how busy we are. Message us on WhatsApp and we will confirm the time for your order."),
]

WHY = [
    ("Attention to Measurements", "We take time over measurements so the fit feels right."),
    ("Professional Stitching", "Careful stitching on every garment, from kameez to trousers."),
    ("Clean Finishing", "Neat seams, collars and plackets."),
    ("Personalized Fitting", "Regular, slim or relaxed — tell us how you like to wear it."),
    ("Custom Stitching", "Bring a design idea and we will discuss how to make it."),
    ("Friendly Service", "Talk to the owner directly, on WhatsApp or at the shop."),
    ("Convenient Local Location", "Easy to find in Iqbal Town, GM Abad, Faisalabad."),
    ("Customer Satisfaction Focus", "We want you to feel comfortable and confident in what you wear."),
]

NAV = [("Home", "index.html"), ("Services", "services.html"), ("Our Work", "our-work.html"), ("Shop", "shop.html"), ("Blog", "blog.html"), ("How to Use", "how-to-use.html"), ("About", "about.html"), ("Visit Us / Contact", "contact.html")]

# ------------------------------------------------------------------ helpers
def e(s): return html.escape(s, quote=True)

def img(prefix, alt, sizes, cls="", eager=False, extra=""):
    files = glob.glob(os.path.join(ROOT, "images", prefix + "-*.webp"))
    items = sorted(((int(re.search(r"-(\d+)\.webp$", f).group(1)), os.path.relpath(f, ROOT).replace(os.sep, "/"), f) for f in files))
    assert items, "missing image " + prefix
    w, src, f = items[-1]
    h = Image.open(f).height
    srcset = ", ".join(f"{p} {ww}w" for ww, p, _ in items)
    load = "" if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}"{load} decoding="async" {extra}>'

def biggest(prefix):
    files = glob.glob(os.path.join(ROOT, "images", prefix + "-*.webp"))
    return max(files, key=lambda f: int(re.search(r"-(\d+)\.webp$", f).group(1)))

def full(prefix): return os.path.relpath(biggest(prefix), ROOT).replace(os.sep, "/")

def wa_btn(label="WhatsApp Now", cls="btn btn--wa", msg=None, track=None):
    m = f' data-msg="{e(msg)}"' if msg else ""
    t = f' data-track="{track}"' if track else ""
    return f'<a class="{cls}" data-wa{m}{t} href="contact.html">{WA}{label}</a>'

def call_btn(label="Call Now", cls="btn btn--ghost"):
    return f'<a class="{cls}" data-call href="contact.html">{PHONE}{label}</a>'

def dir_btn(label="Get Directions", cls="btn btn--ghost"):
    return f'<a class="{cls}" data-directions href="contact.html">{PIN}{label}</a>'

def sec_head(eyebrow, title, intro="", center=False, tag="h2"):
    c = " center" if center else ""
    p = f"<p class=\"muted\">{intro}</p>" if intro else ""
    return f'<div class="sec-head{c} reveal"><span class="eyebrow">{eyebrow}</span><{tag}>{title}</{tag}>{p}</div>'

# ------------------------------------------------------------------ shared parts
def business_ld():
    d = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": DOMAIN + "/#business",
        "name": "Ashfaq Tailor",
        "description": "Local tailoring shop in Iqbal Town, GM Abad, Faisalabad for shalwar kameez, kurta, shirt and pant stitching, alterations and custom fitting.",
        "url": DOMAIN + "/",
        "image": [DOMAIN + "/" + full("shop/ashfaq-tailor-shop-exterior-faisalabad"), DOMAIN + "/" + full("owner/faizan-ali-ashfaq-tailor-owner")],
        "logo": DOMAIN + "/" + full("brand/ashfaq-tailor-logo"),
        "address": {"@type": "PostalAddress", "streetAddress": "Street No. 1, Iqbal Town, GM Abad", "addressLocality": "Faisalabad", "addressRegion": "Punjab", "addressCountry": "PK"},
        "areaServed": {"@type": "City", "name": "Faisalabad"},
        "employee": {"@type": "Person", "name": "Faizan Ali", "jobTitle": "Owner"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Tailoring services",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"]}} for s in SERVICES]},
    }
    return json.dumps(d, ensure_ascii=False)

def faq_ld():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}, ensure_ascii=False)


POSTS = [
 {"file": "blog-shalwar-kameez-measurements-guide.html", "date": "2026-10-24",
  "title": "Shalwar Kameez Measurements: What Your Tailor Needs to Know",
  "desc": "A simple guide to the measurements a tailor takes for a shalwar kameez, and how to describe the fit you like so the stitching comes out right.",
  "img": "portfolio/ashfaq-tailor-shalwar-kameez-cream-gold-placket-faisalabad", "alt": "Cream shalwar kameez with a gold placket stitched by Ashfaq Tailor",
  "body": """<p>A shalwar kameez that fits well starts with good measurements. Most tailors take the same core set, and knowing what they are helps you feel confident when you visit the shop.</p>
<h2>The measurements for a kameez</h2>
<ul><li><strong>Length:</strong> from the shoulder down to where you want the kameez to end.</li>
<li><strong>Chest:</strong> measured around the fullest part of the chest.</li>
<li><strong>Waist and hip:</strong> so the kameez falls neatly and you can move comfortably.</li>
<li><strong>Shoulder:</strong> from one shoulder point to the other.</li>
<li><strong>Sleeve length:</strong> from the shoulder to the wrist, or shorter if you prefer.</li>
<li><strong>Neck or collar:</strong> important if you want a collar or a band collar.</li></ul>
<h2>The measurements for a shalwar</h2>
<ul><li><strong>Length:</strong> from the waist to the ankle.</li>
<li><strong>Waist:</strong> where the shalwar will sit.</li>
<li><strong>Hip and thigh:</strong> for comfortable room when you sit.</li>
<li><strong>Bottom opening (pancha):</strong> narrow or wide, depending on your taste.</li></ul>
<h2>Tell your tailor how you like it to fit</h2>
<p>Numbers are only half the story. Say whether you like a slim, regular or loose fit, and whether you want the kameez on the shorter or longer side. If you own a shalwar kameez that fits you perfectly, bring it along so the tailor can compare.</p>
<div class="tip"><strong>Tip:</strong> wear normal clothes when you are measured, and stand naturally. Measurements taken in person, with a proper fitting, are the best way to get a result you are happy with.</div>
<p>At Ashfaq Tailor we take measurements at the shop in Iqbal Town, GM Abad, Faisalabad, and talk through the style with you before stitching starts.</p>"""},
 {"file": "blog-choosing-fabric-for-faisalabad-weather.html", "date": "2026-10-24",
  "title": "Choosing Fabric for Shalwar Kameez in Faisalabad’s Weather",
  "desc": "How to pick the right fabric for summer and winter in Faisalabad, from light cotton and lawn to warmer cloth, plus a few tips to keep your stitched clothes looking good.",
  "img": "portfolio/ashfaq-tailor-kurta-cream-cross-stitch-collar-faisalabad", "alt": "Cream kurta with cross stitch collar stitched by Ashfaq Tailor",
  "body": """<p>Faisalabad has long hot summers and cooler winters, so the fabric you choose changes how comfortable your clothes feel. Here are some simple things to think about before you buy cloth.</p>
<h2>For hot weather</h2>
<p>Light, breathable fabrics such as cotton and lawn are usually the most comfortable when it is hot. They let air pass through and feel lighter on the skin. Very thick or tightly woven cloth can feel heavy in the heat.</p>
<h2>For cooler weather</h2>
<p>In winter, many people prefer thicker cloth that holds some warmth. A heavier fabric also tends to hang differently, so tell your tailor what you chose so the cutting and stitching suit it.</p>
<h2>Think about care</h2>
<ul><li>Ask whether the fabric may shrink when washed, and plan for it.</li>
<li>Some fabrics crease easily. If you do not like ironing often, pick one that stays smooth.</li>
<li>Dark and bright colours can fade, so wash them gently.</li></ul>
<h2>Bring the fabric to your tailor early</h2>
<p>Showing the cloth before stitching lets the tailor tell you how much is needed, and which collar, placket and cuff styles will look best on it.</p>
<div class="tip"><strong>Tip:</strong> if the fabric might shrink, ask your tailor whether it should be washed once before stitching.</div>
<p>You are welcome to visit Ashfaq Tailor in Iqbal Town, GM Abad, and talk about fabric and style face to face.</p>"""},
 {"file": "blog-first-visit-to-a-tailor.html", "date": "2026-10-24",
  "title": "Your First Visit to a Tailor: What to Bring and What to Ask",
  "desc": "Going to a tailor for the first time? Here is what to bring, which questions to ask, and how to explain the style you want so you get the result you imagined.",
  "img": "shop/ashfaq-tailor-shop-interior-workspace-faisalabad", "alt": "Inside the Ashfaq Tailor shop workspace in Faisalabad",
  "body": """<p>Visiting a tailor for the first time is easier when you know what to expect. A little preparation helps you explain exactly what you want.</p>
<h2>What to bring</h2>
<ul><li><strong>Your fabric,</strong> if you already have it.</li>
<li><strong>A photo or sample</strong> of the style you like: collar, placket, cuffs, pockets.</li>
<li><strong>A garment that fits you well,</strong> so the tailor can see the fit you prefer.</li></ul>
<h2>Questions worth asking</h2>
<ul><li>How long will stitching take?</li>
<li>Will there be a fitting before the garment is finished?</li>
<li>What can be adjusted afterwards if something is not quite right?</li>
<li>Is there anything about my fabric the tailor should know?</li></ul>
<h2>Explain the style clearly</h2>
<p>Pictures say more than words. If you are unsure about collars or cuffs, ask the tailor to show you options and talk through what suits the garment and your taste.</p>
<div class="tip"><strong>Tip:</strong> you can start the conversation on WhatsApp first, then come to the shop to be measured.</div>
<p>At Ashfaq Tailor, Street No. 1, Iqbal Town, GM Abad, Faisalabad, we are happy to talk through your style and fitting before you decide.</p>"""},
]

EXTRA_NAMES = {"how-to-use.html": "How to Use", "privacy-policy.html": "Privacy Policy", "blog.html": "Blog"}

def breadcrumb_ld(path):
    if path in ("index.html", "404.html"): return ""
    items = [("Home", "/")]
    post = next((x for x in POSTS if x["file"] == path), None)
    if post: items += [("Blog", "/blog.html"), (post["title"], "/" + path)]
    else: items.append((EXTRA_NAMES.get(path) or dict((h, n) for n, h in NAV).get(path, path), "/" + path))
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, "item": DOMAIN + u} for k, (n, u) in enumerate(items)]}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>\n'

def website_ld():
    data = {"@context": "https://schema.org", "@type": "WebSite", "name": "Ashfaq Tailor", "url": DOMAIN + "/", "inLanguage": "en-PK"}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>\n'

def head(title, desc, path, extra_ld=""):
    url = DOMAIN + "/" + ("" if path == "index.html" else path)
    og = DOMAIN + "/images/brand/og-ashfaq-tailor.jpg"
    robots = "" if path == "404.html" else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">\n'
    extra_ld = extra_ld + breadcrumb_ld(path) + (website_ld() if path == "index.html" else "")
    return f'''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-PK" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="geo.region" content="PK-PB">
<meta name="geo.placename" content="Iqbal Town, GM Abad, Faisalabad">
<meta name="theme-color" content="#14110d">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ashfaq Tailor">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:alt" content="Ashfaq Tailor shop front in Iqbal Town, GM Abad, Faisalabad">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_PK">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="icon" type="image/png" sizes="32x32" href="images/brand/favicon-32.png">
<link rel="apple-touch-icon" href="images/brand/favicon-180.png">
<link rel="stylesheet" href="css/style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json" id="ld-business">{business_ld()}</script>
{extra_ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{n}</a>' for n, h in NAV)
    mlinks = "".join(f'<a href="{h}">{n}</a>' for n, h in NAV)
    return f'''<header class="site-header">
 <div class="container">
  <a class="brand" href="index.html" aria-label="Ashfaq Tailor — home">{img("brand/ashfaq-tailor-logo", "Ashfaq Tailor logo", "44px", eager=True)}<span><b>Ashfaq Tailor</b><small>Faisalabad</small></span></a>
  <nav class="nav" aria-label="Main">{links}</nav>
  {wa_btn("WhatsApp Us", "btn btn--wa btn--sm header-cta")}
  <button class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menu"><span></span></button>
 </div>
 <div class="container mobile-nav" id="mobile-nav"><nav aria-label="Mobile">{mlinks}</nav>{wa_btn("WhatsApp Us")}</div>
</header>
<main id="main">
'''

def footer():
    nav = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV) + '<li><a href="privacy-policy.html">Privacy Policy</a></li>'
    svc = "".join(f'<li><a href="services.html#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES[:6])
    return f'''</main>
<footer class="site-footer">
 <div class="container">
  <div class="foot-grid">
   <div>
    <div class="foot-brand">{img("brand/ashfaq-tailor-logo", "Ashfaq Tailor logo", "56px")}<b>Ashfaq Tailor</b></div>
    <p>Professional stitching, careful fitting and personal service in Iqbal Town, GM Abad, Faisalabad. Owner: <span data-f="owner">Faizan Ali</span>.</p>
    <ul class="social" data-social-wrap hidden>
     <li><a data-social="facebook" href="#">Facebook</a></li><li><a data-social="instagram" href="#">Instagram</a></li><li><a data-social="tiktok" href="#">TikTok</a></li>
    </ul>
   </div>
   <div><h3>Services</h3><ul>{svc}</ul></div>
   <div><h3>Pages</h3><ul>{nav}</ul></div>
   <div data-loc="footer">
    <h3>Visit &amp; Contact</h3>
    <ul>
     <li>Street No. 1, Iqbal Town, GM Abad, Faisalabad, Pakistan</li>
     <li>Phone: <a data-call href="contact.html"><span data-f="phone">0311-4614341</span></a></li>
     <li>WhatsApp: <a data-wa href="contact.html"><span data-f="whatsapp">0327-7938569</span></a></li>
     <li data-hours></li>
     <li><a data-directions href="contact.html">Get Directions</a></li>
    </ul>
   </div>
  </div>
  <p class="copy">© Ashfaq Tailor. All Rights Reserved. · <a href="privacy-policy.html">Privacy Policy</a></p>
 </div>
</footer>
<div class="mobile-bar" data-loc="mobile-bar" role="navigation" aria-label="Quick contact">
 <a class="wa" data-wa href="contact.html">{WA}WhatsApp</a>
 <a data-call href="contact.html">{PHONE}Call</a>
 <a data-directions href="contact.html">{PIN}Directions</a>
</div>
<a class="wa-float" data-wa data-loc="floating-button" href="contact.html" aria-label="Chat on WhatsApp">{WA}<span>WhatsApp</span></a>
<script src="js/site-config.js"></script>
<script src="js/main.js" defer></script>
</body>
</html>
'''

def cta_band(text="Ready to get your clothes stitched?"):
    return f'''<section class="section section--dark on-dark" data-loc="cta-band"><div class="container" style="text-align:center">
 <div class="reveal"><h2>{text}</h2><p class="muted" style="max-width:34rem;margin:0 auto 1.4rem">Message us on WhatsApp, call, or visit the shop in Iqbal Town. We will help you with style, fitting and measurements.</p>
 <div class="btn-row" style="justify-content:center">{wa_btn()}{call_btn()}{dir_btn()}</div></div></div></section>'''

def page_hero(h1, intro, eyebrow):
    return f'<section class="page-hero"><div class="container"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{intro}</p></div></section>'

# ------------------------------------------------------------------ sections
def services_cards():
    out = []
    for s in SERVICES:
        msg = f"Assalam-o-Alaikum Ashfaq Tailor, I would like to ask about {s['name']}."
        out.append(f'''<article class="card reveal" id="s-{s["id"]}"><span class="icon">{icon(s["icon"])}</span><h3>{s["name"]}</h3><p>{s["short"]}</p>{wa_btn("Ask on WhatsApp", "btn btn--wa btn--sm", msg)}</article>''')
    return "".join(out)

def work_item(w):
    wid, cat, title, prefix, alt = w
    msg = f"Assalam-o-Alaikum Ashfaq Tailor, I like this style: {title}. I would like to discuss it."
    return f'''<figure class="work-item reveal" data-cat="{cat}">
<button class="thumb" type="button" data-lb data-lb-wa data-full="{full(prefix)}" data-alt="{e(alt)}" data-title="{e(title)}" aria-label="View larger: {e(title)}">{img(prefix, alt, "(min-width:760px) 33vw, 50vw")}</button>
<figcaption class="cap"><small>{CATS[cat]}</small><b>{title}</b><span class="ask">Like This Style?</span>{wa_btn("Discuss It on WhatsApp", "btn btn--wa btn--sm", msg)}</figcaption></figure>'''

def chooser():
    return f'''<section class="section" id="choose-style" data-loc="choose-your-style"><div class="container">
{sec_head("Choose Your Style", "Pick a garment and fit — we start the chat for you", "Select what you have in mind and your WhatsApp message is written for you. You can change anything once the chat opens.")}
<div class="chooser reveal" id="style-chooser">
 <div>
  <fieldset><legend>Garment</legend><div class="opts" data-garments></div></fieldset>
  <fieldset><legend>Fitting</legend><div class="opts" data-fits></div></fieldset>
 </div>
 <div class="chooser-out" aria-live="polite">
  <div class="muted" style="color:#cdbf9f;font-size:.85rem;letter-spacing:.1em;text-transform:uppercase">Your selection</div>
  <div class="preview">Pick a garment to begin.</div>
  <a class="btn btn--wa" id="style-go" href="#style-chooser">{WA}Discuss This Style on WhatsApp</a>
  <small id="style-hint" role="status"></small>
  <small>Prices and delivery time are discussed on WhatsApp.</small>
 </div>
</div></div></section>'''

def trio():
    return f'''<section class="section section--ivory" data-loc="real-trust"><div class="container">
{sec_head("Our promise", "Real Shop. Real Work. Real People.", "Behind this website is a real shop in Iqbal Town, an owner you can talk to, and stitching you can see up close.", center=True)}
<div class="trio" data-lb-group>
 <figure class="reveal">{img("shop/ashfaq-tailor-shop-exterior-faisalabad", "Front of the Ashfaq Tailor shop with a wooden glass door and a shelf of fabric", "(min-width:760px) 33vw, 100vw", extra='style="object-position:center 8%"')}<figcaption>The shop<small>Street No. 1, Iqbal Town, GM Abad</small></figcaption></figure>
 <figure class="reveal">{img("owner/faizan-ali-ashfaq-tailor-owner", "Faizan Ali, owner of Ashfaq Tailor, seated and wearing a brown kameez shalwar", "(min-width:760px) 33vw, 100vw", extra='style="object-position:center 20%"')}<figcaption>The owner<small>Faizan Ali</small></figcaption></figure>
 <figure class="reveal">{img(WORK[0][3], WORK[0][4], "(min-width:760px) 33vw, 100vw")}<figcaption>The work<small>Collar, placket and cuff detail</small></figcaption></figure>
</div></div></section>'''

def inside(h2="Inside Ashfaq Tailor", dark=False):
    btns = "".join(f'<button type="button" data-lb data-full="{full(p)}" data-alt="{e(a)}" data-title="{e(a)}" aria-label="View larger: {e(a)}">{img(p, a, "(min-width:860px) 25vw, 50vw")}</button>' for p, a in INSIDE)
    return f'''<section class="section" data-loc="inside-shop"><div class="container">
{sec_head("The workspace", h2, "See the place where your clothes are prepared and stitched — thread, trims, machines and cutting space.")}
<div class="inside reveal" data-lb-group>{btns}</div></div></section>'''

def owner(show_msg=True):
    msg = '''<blockquote class="msg reveal">“Every customer has a different style and fitting preference. At Ashfaq Tailor, our goal is to understand your requirements and provide stitching that you feel confident wearing.”<cite>— Faizan Ali<br>Owner, Ashfaq Tailor</cite></blockquote>''' if show_msg else ""
    return f'''<section class="section section--ivory" id="owner" data-loc="owner"><div class="container owner">
 <div class="owner-photo reveal">{img("owner/faizan-ali-ashfaq-tailor-owner", "Faizan Ali, owner of Ashfaq Tailor, seated and wearing a brown kameez shalwar", "(min-width:860px) 400px, 90vw")}</div>
 <div class="reveal">
  <span class="eyebrow" style="color:var(--gold-d)">Meet the Owner</span>
  <h2>Faizan Ali</h2>
  <p class="role">Owner — Ashfaq Tailor</p>
  <p>Faizan Ali is the owner of Ashfaq Tailor, focused on providing customers with professional stitching, comfortable fitting, quality finishing and personal service.</p>
  {msg}
  <div class="btn-row" style="margin-top:1.4rem">{wa_btn("Talk to Faizan on WhatsApp")}</div>
 </div></div></section>'''

def how():
    steps = [("Contact Us", "Contact us through WhatsApp or phone."),
             ("Discuss Requirements / Measurements", "Visit the shop and discuss fitting, measurements and style."),
             ("Professional Stitching", "Your clothes are prepared according to the agreed requirements."),
             ("Collect Your Clothes", "Visit Ashfaq Tailor to collect your completed order.")]
    li = "".join(f"<li class=\"reveal\"><h3>{t}</h3><p>{d}</p></li>" for t, d in steps)
    return f'''<section class="section section--dark on-dark" data-loc="how-it-works"><div class="container">
{sec_head("How it works", "Four simple steps", "From the first message to collecting your clothes.", center=True)}
<ol class="steps">{li}</ol></div></section>'''

def why():
    li = "".join(f"<li class=\"reveal\"><b>{t}</b><p>{d}</p></li>" for t, d in WHY)
    return f'''<section class="section" data-loc="why-choose"><div class="container">
{sec_head("Why Ashfaq Tailor", "Why choose Ashfaq Tailor", "Simple things done carefully: good measurements, neat stitching and a friendly conversation.")}
<ul class="why">{li}</ul></div></section>'''

def reviews():
    return f'''<section class="section section--ivory" id="reviews" data-loc="reviews"><div class="container">
{sec_head("Customer Reviews", "What customers say", "", center=True)}
<div data-reviews class="reveal"><div class="review-empty"><span class="tag">Placeholder</span><p>Real customer reviews will appear here. We only show genuine reviews from real customers — no made-up ratings.</p>
<a class="btn btn--gold" data-review-link data-track="review_link_click" href="#">Read / Leave a Google Review</a></div></div>
</div></section>
<section class="section" data-before-after hidden data-loc="before-after"><div class="container">
{sec_head("Before &amp; After", "Alterations and fitting improvements", "Real work, real garments.", center=True)}
<div data-ba-list></div></div></section>'''

def faq():
    items = "".join(f"<details><summary>{q}</summary><div class=\"ans\"><p>{a}</p></div></details>" for q, a in FAQS)
    return f'''<section class="section" id="faq" data-loc="faq"><div class="container">
{sec_head("Questions", "Frequently asked questions", "", center=True)}
<div class="faq reveal">{items}</div></div></section>'''

def info_list():
    return f'''<ul class="info-list">
 <li><span class="ico">{PIN}</span><div><b>Address</b>Ashfaq Tailor<br>Street No. 1, Iqbal Town, GM Abad,<br>Faisalabad, Pakistan</div></li>
 <li><span class="ico">{PHONE}</span><div><b>Phone</b><a data-call href="contact.html"><span data-f="phone">0311-4614341</span></a></div></li>
 <li><span class="ico">{WA}</span><div><b>WhatsApp</b><a data-wa href="contact.html"><span data-f="whatsapp">0327-7938569</span></a></div></li>
 <li><span class="ico">{CLOCK}</span><div><b>Opening hours</b><div data-hours></div></div></li>
</ul>'''

def map_box():
    return '''<div class="map" data-map></div><p class="placeholder-note" data-map-note>Map shows the area. The exact shop pin can be added in js/site-config.js.</p>'''

def visit(show_form=False):
    return f'''<section class="section section--ivory" id="visit" data-loc="visit-shop"><div class="container">
{sec_head("Find us", "Visit Ashfaq Tailor", "Come in, see the shop and talk about your clothes face to face.")}
<div class="visit">
 <div class="visit-photo reveal">{img("shop/ashfaq-tailor-shop-exterior-faisalabad", "Front of the Ashfaq Tailor shop with a wooden glass door and a shelf of fabric", "(min-width:900px) 420px, 90vw")}</div>
 <div class="reveal">
  <h3 style="font-size:1.6rem">Ashfaq Tailor</h3>
  {info_list()}
  <div class="btn-row">{wa_btn("Chat on WhatsApp")}{call_btn()}{dir_btn()}</div>
  {map_box()}
 </div>
</div></div></section>'''

def form_block(heading="Send an inquiry", sub="Fill in a few details and WhatsApp opens with your message ready to send."):
    opts = "".join(f'<option>{s["name"]}</option>' for s in SERVICES)
    return f'''<div class="reveal">
<h2 style="font-size:1.9rem">{heading}</h2><p class="muted">{sub}</p>
<form class="form" id="inquiry-form" novalidate>
 <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required><span class="err">Please enter your name.</span></div>
 <div class="row2">
  <div class="field"><label for="f-phone">Phone <span class="opt-tag">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
  <div class="field"><label for="f-service">Service needed</label><select id="f-service" name="service" required><option value="">Select a service</option>{opts}</select><span class="err">Please choose a service.</span></div>
 </div>
 <div class="field"><label for="f-date">Preferred date <span class="opt-tag">(optional)</span></label><input id="f-date" name="date" type="date"></div>
 <div class="field"><label for="f-message">Message <span class="opt-tag">(optional)</span></label><textarea id="f-message" name="message" placeholder="Tell us about the style, fabric or fitting you have in mind."></textarea></div>
 <button class="btn btn--wa" type="submit">{WA}Send Inquiry on WhatsApp</button>
 <p class="form-note">This opens WhatsApp with your message ready to send. Nothing is saved on this website.</p>
 <p id="form-done" hidden role="status" class="form-note"><strong>Thank you.</strong> If WhatsApp did not open, please use the WhatsApp button on this page.</p>
</form></div>'''

# ------------------------------------------------------------------ pages
def build_index():
    work = "".join(work_item(next(w for w in WORK if w[0] == i)) for i in HOME_WORK)
    h = head("Ashfaq Tailor | Tailor in Iqbal Town, GM Abad, Faisalabad",
             "Ashfaq Tailor in Iqbal Town, GM Abad, Faisalabad: shalwar kameez, kurta, shirt and pant stitching, alterations and custom fitting. WhatsApp or visit us.",
             "index.html", f'<script type="application/ld+json">{faq_ld()}</script>\n')
    body = f'''<section class="hero on-dark" data-loc="hero"><div class="container">
 <div>
  <span class="eyebrow">Local tailor · Iqbal Town, GM Abad, Faisalabad</span>
  <h1>Perfect Fit. <em>Professional Stitching.</em> Made for You.</h1>
  <p class="urdu" lang="ur">اشفاق ٹیلرز</p>
  <p class="lead">Ashfaq Tailor is a local tailoring shop in Faisalabad for shalwar kameez, kurta, shirt and pant stitching — with careful measurements and a personal fitting.</p>
  <div class="btn-row">{wa_btn("WhatsApp Now")}{call_btn()}{dir_btn()}</div>
  <ul class="ticks"><li>Professional Stitching</li><li>Attention to Fitting</li><li>Quality Finishing</li><li>Local Tailor in Faisalabad</li></ul>
 </div>
 <figure class="hero-photo" style="margin:0"><div class="frame">{img("shop/ashfaq-tailor-shop-exterior-faisalabad", "Front of the Ashfaq Tailor shop with a wooden glass door, a shop sign above and a shelf of fabric", "(min-width:900px) 420px, 380px", eager=True, extra='fetchpriority="high"')}</div>
  <figcaption><b>Ashfaq Tailor</b>Street No. 1, Iqbal Town, GM Abad, Faisalabad</figcaption></figure>
</div></section>
<div class="trust"><div class="container"><ul><li>Professional Stitching</li><li>Personal Fitting</li><li>Clean Finishing</li><li>Visit Us in Iqbal Town</li></ul></div></div>

<section class="section" id="services" data-loc="services"><div class="container">
{sec_head("What we stitch", "Tailoring services for every day and every occasion", "Tell us what you need on WhatsApp or visit the shop. Prices depend on the garment and style — message us for a quote.")}
<div class="grid grid--svc">{services_cards()}</div>
<p style="margin-top:1.6rem"><a class="btn btn--ghost btn--sm" style="color:var(--ink)" href="services.html">See all services in detail</a></p>
</div></section>

<section class="section section--ivory" id="our-work" data-loc="our-work"><div class="container" data-lb-group>
{sec_head("Our Work", "Styles we have stitched", "Collar, placket and cuff details. Tap any photo to see it larger.")}
<div class="work work--home">{work}</div>
<p style="margin-top:1rem"><a class="btn btn--ghost btn--sm" style="color:var(--ink)" href="our-work.html">View all our work</a></p>
</div></section>

{chooser()}
{trio()}
{inside()}
{owner()}
{how()}
{why()}
{reviews()}
{faq()}
{visit()}
<section class="section" id="inquiry" data-loc="inquiry-form"><div class="container split">
 <div class="reveal"><span class="eyebrow" style="color:var(--gold-d)">Quick inquiry</span><h2>Tell us what you need</h2><p class="muted">The quickest way to start is WhatsApp. You can also fill in this short form and we will receive it as a WhatsApp message.</p><div class="btn-row">{wa_btn("Chat on WhatsApp")}{call_btn()}</div></div>
 {form_block("Send an inquiry")}
</div></section>
'''
    return h + header("index.html") + body + footer()

def build_services():
    cards = []
    for s in SERVICES:
        top = (f'<div class="card-img">{img(s["img"], s["alt"], "(min-width:760px) 50vw, 100vw")}</div>' if s["img"] else "")
        ic = "" if s["img"] else f'<span class="icon">{icon(s["icon"])}</span>'
        pts = "".join(f"<li>✓ {p}</li>" for p in s["points"])
        msg = f"Assalam-o-Alaikum Ashfaq Tailor, I would like to ask about {s['name']}."
        cards.append(f'''<article class="card {"card--img" if s["img"] else ""} reveal" id="{s["id"]}">{top}<div class="{"card-body" if s["img"] else ""}">{ic}<h2 style="font-size:1.5rem">{s["name"]}</h2><p>{s["long"]}</p><ul class="muted" style="margin:.2rem 0 .8rem;font-size:.95rem">{pts}</ul>{wa_btn("Ask on WhatsApp", "btn btn--wa btn--sm", msg)}</div></article>''')
    h = head("Tailoring Services in Faisalabad | Ashfaq Tailor, Iqbal Town",
             "Shalwar kameez, kurta, shirt and pant stitching, waistcoat fitting and alterations at Ashfaq Tailor, Iqbal Town, GM Abad, Faisalabad. Ask on WhatsApp.",
             "services.html")
    body = page_hero("Tailoring Services at Ashfaq Tailor", "Stitching and fitting for men's everyday and occasion wear, from our shop in Iqbal Town, GM Abad, Faisalabad.", "Services") + f'''
<section class="section" data-loc="services-list"><div class="container">
<p class="muted reveal" style="max-width:44rem">We do not list fixed prices because they depend on the garment, fabric and style. Message us a photo or description on WhatsApp and we will discuss it with you.</p>
<div class="svc-detail">{"".join(cards)}</div></div></section>
{chooser()}
{cta_band()}'''
    return h + header("services.html") + body + footer()

def build_work():
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All</button>' + "".join(f'<button class="chip" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items())
    items = "".join(work_item(w) for w in WORK)
    h = head("Our Work — Stitched Kameez, Kurta & Shirts | Ashfaq Tailor Faisalabad",
             "See styles stitched at Ashfaq Tailor in Iqbal Town, Faisalabad: shalwar kameez, kurta and shirts with collar, placket and cuff detail. Discuss a style on WhatsApp.",
             "our-work.html")
    body = page_hero("Our Work", "Collar, placket and cuff details from Ashfaq Tailor. Tap any photo to see it larger, and message us if you like a style.", "Portfolio") + f'''
<section class="section" data-loc="portfolio"><div class="container" data-lb-group>
<div class="filters" role="group" aria-label="Filter by garment">{chips}</div>
<div class="work">{items}</div>
<div class="empty-note reveal" style="margin-top:1rem">Looking for pants, waistcoats or alterations? Send us a message on WhatsApp — more photos of our work are added over time.</div>
</div></section>
{inside("Where it is stitched")}
{cta_band("Like a style? Let us discuss it.")}'''
    return h + header("our-work.html") + body + footer()

def build_about():
    h = head("About Ashfaq Tailor & Owner Faizan Ali | Faisalabad",
             "Meet Faizan Ali, owner of Ashfaq Tailor in Iqbal Town, GM Abad, Faisalabad. Professional stitching, careful fitting, clean finishing and personal service.",
             "about.html")
    body = page_hero("About Ashfaq Tailor", "A local tailoring shop in Iqbal Town, GM Abad, Faisalabad, run by its owner, Faizan Ali.", "About us") + f'''
<section class="section" data-loc="about-story"><div class="container split">
 <div class="reveal"><span class="eyebrow" style="color:var(--gold-d)">Who we are</span><h2>Professional stitching with a personal touch</h2>
  <p>Ashfaq Tailor is a tailoring shop at Street No. 1, Iqbal Town, GM Abad, Faisalabad. We focus on professional stitching, comfortable fitting, clean finishing and personal service.</p>
  <p>Every customer has a different style and fitting preference, so we start by listening — then take measurements and stitch to what you agreed.</p>
  <div class="btn-row">{wa_btn()}{dir_btn()}</div></div>
 <div class="reveal visit-photo" style="justify-self:center">{img("shop/ashfaq-tailor-shop-exterior-faisalabad", "Front of the Ashfaq Tailor shop with a wooden glass door and a shelf of fabric", "(min-width:900px) 420px, 90vw")}</div>
</div></section>
{owner()}
{inside("A look inside the shop")}
{trio()}
{why()}
{cta_band()}'''
    return h + header("about.html") + body + footer()

def build_contact():
    h = head("Contact & Visit Ashfaq Tailor | Iqbal Town, GM Abad, Faisalabad",
             "Contact Ashfaq Tailor on WhatsApp or phone, or visit the shop at Street No. 1, Iqbal Town, GM Abad, Faisalabad. Get directions on Google Maps.",
             "contact.html")
    body = page_hero("Visit & Contact Ashfaq Tailor", "Message us on WhatsApp, call, or come to the shop. We are happy to talk through your style and fitting.", "Contact") + f'''
<section class="section" id="contact" data-loc="contact"><div class="container split">
 <div class="reveal">
  <h2 style="font-size:1.9rem">Ashfaq Tailor</h2>
  <p class="muted">Owner: <strong data-f="owner">Faizan Ali</strong></p>
  {info_list()}
  <div class="btn-row">{wa_btn("Chat on WhatsApp")}{call_btn()}{dir_btn()}</div>
  {map_box()}
 </div>
 {form_block()}
</div></section>
<section class="section section--ivory" data-loc="contact-photo"><div class="container split">
 <div class="visit-photo reveal" style="justify-self:center">{img("shop/ashfaq-tailor-shop-exterior-faisalabad", "Front of the Ashfaq Tailor shop with a wooden glass door and a shelf of fabric", "(min-width:900px) 420px, 90vw")}</div>
 <div class="reveal"><span class="eyebrow" style="color:var(--gold-d)">Look for this shop</span><h2>Easy to recognise</h2><p>We are in Iqbal Town, GM Abad. Look for the wooden glass door and the shelf of fabric by the entrance. If you get lost, message us on WhatsApp and we will guide you.</p></div>
</div></section>'''
    return h + header("contact.html") + body + footer()

def build_shop():
    h = head("Our Shop — Ashfaq Tailor, Iqbal Town, GM Abad, Faisalabad",
             "Visit the Ashfaq Tailor shop at Street No. 1, Iqbal Town, GM Abad, Faisalabad. See the shop front, the workspace inside, get directions and contact us on WhatsApp.",
             "shop.html")
    body = page_hero("Our Shop in Iqbal Town", "Street No. 1, Iqbal Town, GM Abad, Faisalabad. Come in, see where your clothes are stitched, and talk about your style face to face.", "The shop") + f'''
<section class="section" id="shop-front" data-loc="shop-front"><div class="container split">
 <div class="visit-photo reveal" style="justify-self:center">{img("shop/ashfaq-tailor-shop-exterior-faisalabad", "Front of the Ashfaq Tailor shop with a wooden glass door and a shelf of fabric", "(min-width:900px) 460px, 90vw", eager=True)}</div>
 <div class="reveal">
  <span class="eyebrow" style="color:var(--gold-d)">Look for this shop</span>
  <h2>Ashfaq Tailor, GM Abad</h2>
  <p>Look for the wooden glass door and the shelf of fabric by the entrance. If you get lost, message us on WhatsApp and we will guide you.</p>
  {info_list()}
  <div class="btn-row">{wa_btn("Chat on WhatsApp")}{call_btn()}{dir_btn()}</div>
 </div>
</div></section>
<section class="section section--ivory" data-loc="shop-do"><div class="container">
{sec_head("At the shop", "What you can do when you visit", "Measurements are normally taken at the shop so the fit is right.")}
<div class="grid grid--svc">
 <article class="card reveal"><h3>Get measured</h3><p>We take your measurements in person so the fit is right.</p></article>
 <article class="card reveal"><h3>Choose your style</h3><p>Pick the collar, placket and cuff style, or show us a photo you like.</p></article>
 <article class="card reveal"><h3>Bring clothes for alteration</h3><p>Bring the garment and we will tell you what can be done.</p></article>
 <article class="card reveal"><h3>Ask anything</h3><p>Talk through fit, fabric and timing before you decide.</p></article>
</div></div></section>
{inside("Inside the shop")}
<section class="section section--ivory" id="find-us" data-loc="shop-map"><div class="container">
{sec_head("Find us", "Directions to Ashfaq Tailor", "Tap Get Directions to open the route in Google Maps.")}
{map_box()}
<div class="btn-row" style="margin-top:1rem">{dir_btn("Get Directions", "btn btn--gold")}{wa_btn()}</div>
</div></section>
{cta_band("Visit the shop or message us first")}'''
    return h + header("shop.html") + body + footer()


def howto_page():
    steps = [
     ("Browse our services", "Open <a href=\"services.html\">Services</a> to see what we stitch: shalwar kameez, kurta, shirts, pants and trousers, waistcoats and alterations."),
     ("See our work", "Open <a href=\"our-work.html\">Our Work</a> to look at real stitching. Use the category buttons to filter, and tap any photo to see it larger."),
     ("Choose your style", "On the <a href=\"index.html#choose-style\">Home page</a>, use <em>Choose Your Style</em>. Pick a garment and a fitting, and your WhatsApp message is written for you."),
     ("Message or call us", "Tap the green WhatsApp button, or Call Now. You can also use the inquiry form on the <a href=\"contact.html\">Contact page</a>; it opens WhatsApp with your message ready to send."),
     ("Visit the shop", "Open the <a href=\"shop.html\">Shop page</a>, tap the map or Get Directions, and come to Iqbal Town, GM Abad. Measurements are normally taken at the shop so the fit is right."),
    ]
    li = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps)
    btns = [
     ("WhatsApp", "Opens WhatsApp with a message ready to send to the shop."),
     ("Call Now", "Calls the shop phone number. It works on phones."),
     ("Get Directions", "Opens Google Maps with directions to the shop."),
     ("The map", "Tap the map and the shop location opens in Google Maps in a new tab."),
    ]
    cards = "".join(f'<article class="card reveal"><h3>{t}</h3><p>{d}</p></article>' for t, d in btns)
    faqs = [
     ("Do I need an account to use this website?", "No. There is nothing to sign up for. Just browse and message us."),
     ("Is my information saved on the website?", "No. The inquiry form only builds a WhatsApp message in your browser. Nothing is saved on this website."),
     ("Can I pay online here?", "No. This website does not take online payments. Orders, prices and delivery time are talked through with the shop on WhatsApp, by phone, or in person."),
     ("What should I send in my first message?", "Tell us which garment you want, the style you like (a photo helps), and when you would like to visit the shop."),
    ]
    fq = "".join(f"<details><summary>{q}</summary><div class=\"ans\"><p>{a}</p></div></details>" for q, a in faqs)
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "How to use the Ashfaq Tailor website and get your clothes stitched",
          "step": [{"@type": "HowToStep", "position": k + 1, "name": t, "text": re.sub("<[^>]+>", "", d)} for k, (t, d) in enumerate(steps)]}
    h = head("How to Use This Website | Ashfaq Tailor, Faisalabad",
             "A simple guide to using the Ashfaq Tailor website: browse services, see our work, choose your style, message us on WhatsApp and visit the shop in Iqbal Town, Faisalabad.",
             "how-to-use.html", '<script type="application/ld+json">' + json.dumps(ld) + '</script>\n')
    body = page_hero("How to Use This Website", "A quick guide to finding what you need, choosing your style and getting in touch with Ashfaq Tailor.", "Guide") + f'''
<section class="section section--dark" data-loc="howto-steps"><div class="container">
{sec_head("Five easy steps", "From browsing to your first fitting", "", True)}
<ol class="steps steps--wide reveal">{li}</ol></div></section>
<section class="section section--ivory" data-loc="howto-buttons"><div class="container">
{sec_head("Buttons explained", "What each button does", "")}
<div class="grid grid--svc">{cards}</div></div></section>
<section class="section" data-loc="howto-faq"><div class="container">
{sec_head("Good to know", "Common questions", "", True)}
<div class="faq reveal">{fq}</div></div></section>
{cta_band("Ready to start? Message us on WhatsApp")}'''
    return h + header("how-to-use.html") + body + footer()

def privacy_page():
    inner = """<p class="post-meta">Last updated: October 24, 2026</p>
<p>This policy explains what happens to your information when you use the Ashfaq Tailor website. We keep things simple: this is a small tailoring shop website, and we collect very little.</p>
<h2>1. Information you share with us</h2>
<p>This website has no accounts or sign-up. If you contact us on WhatsApp or by phone, or use the inquiry form, we receive the details you choose to send, such as your name, phone number and the clothes you want stitched. We use them only to reply to you and to serve your tailoring order.</p>
<h2>2. The inquiry form</h2>
<p>The inquiry form does not send your details to our servers. It prepares a WhatsApp message in your browser and opens WhatsApp. Nothing you type is stored on this website. What you send in WhatsApp is handled under WhatsApp’s own terms and privacy policy.</p>
<h2>3. Cookies and analytics</h2>
<p>This website does not use advertising cookies. If we turn on a website analytics tool in the future, it would show us general usage, such as which pages are visited, and we would update this page.</p>
<h2>4. Third-party services</h2>
<ul><li><strong>Google Maps:</strong> the map on some pages loads from Google, and Google may collect technical information such as your IP address when it loads. See Google’s privacy policy.</li>
<li><strong>WhatsApp:</strong> buttons open WhatsApp, which is run by a separate company with its own privacy policy.</li>
<li><strong>Hosting:</strong> the company that hosts this website may keep standard technical logs, such as IP addresses, for security and reliability.</li></ul>
<h2>5. Photos on this website</h2>
<p>We show photos of our shop and our stitching work. If you believe a photo shows your clothes or your image and you would like it removed, contact us and we will look into it.</p>
<h2>6. How we protect and keep information</h2>
<p>We keep customer details only as long as needed to serve your order and answer your questions, and we do not sell your information.</p>
<h2>7. Children</h2>
<p>This website is meant for adults arranging tailoring. We do not knowingly collect information from children through the website.</p>
<h2>8. Your choices</h2>
<p>You can ask us to stop messaging you, or to delete the details you sent us, by contacting us using the details below.</p>
<h2>9. Changes to this policy</h2>
<p>We may update this page from time to time. The date at the top shows when it was last changed.</p>
<h2>10. Contact us</h2>
<p>Ashfaq Tailor, Street No. 1, Iqbal Town, GM Abad, Faisalabad, Pakistan.<br>Phone: <a data-call href="contact.html"><span data-f="phone">0311-4614341</span></a><br>WhatsApp: <a data-wa href="contact.html"><span data-f="whatsapp">0327-7938569</span></a><br>Or use the <a href="contact.html">Contact page</a>.</p>"""
    h = head("Privacy Policy | Ashfaq Tailor, Faisalabad",
             "Privacy policy for the Ashfaq Tailor website: what information we receive, how the WhatsApp inquiry form works, and which third-party services are used.",
             "privacy-policy.html")
    body = page_hero("Privacy Policy", "How the Ashfaq Tailor website handles your information.", "Privacy") + f'<section class="section"><div class="container"><div class="prose">{inner}</div></div></section>'
    return h + header("privacy-policy.html") + body + footer()

def nice_date(d):
    import datetime
    t = datetime.date.fromisoformat(d)
    return f"{t.day} {t.strftime('%B %Y')}"

def post_card(x):
    return f'''<article class="card post-card reveal">
 {img(x["img"], x["alt"], "(min-width:900px) 360px, 90vw")}
 <p class="post-meta" style="margin:0">{nice_date(x["date"])}</p>
 <h3><a href="{x["file"]}">{x["title"]}</a></h3>
 <p>{x["desc"]}</p>
 <a class="more" href="{x["file"]}">Read more &rarr;</a>
</article>'''

def build_blog():
    h = head("Tailoring Tips & Guides | Ashfaq Tailor Blog, Faisalabad",
             "Practical tailoring tips from Ashfaq Tailor in Faisalabad: measurements, fabric choice for the weather, and what to expect on your first visit to a tailor.",
             "blog.html")
    cards = "".join(post_card(x) for x in POSTS)
    body = page_hero("Blog: Tailoring Tips & Guides", "Simple, practical advice on measurements, fabric and style, written by the team at Ashfaq Tailor.", "Blog") + f'''
<section class="section" data-loc="blog-list"><div class="container"><div class="grid grid--posts">{cards}</div></div></section>
{cta_band("Have a question about your clothes? Ask us on WhatsApp")}'''
    return h + header("blog.html") + body + footer()

def best_img(prefix):
    files = glob.glob(os.path.join(ROOT, "images", prefix + "-*.webp"))
    big = max(files, key=lambda f: int(re.search(r"-(\d+)\.webp$", f).group(1)))
    return os.path.relpath(big, ROOT).replace(os.sep, "/")

def build_post(x):
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": x["title"], "description": x["desc"],
          "datePublished": x["date"], "dateModified": x["date"], "inLanguage": "en-PK",
          "mainEntityOfPage": DOMAIN + "/" + x["file"],
          "image": DOMAIN + "/" + best_img(x["img"]),
          "author": {"@type": "Organization", "name": "Ashfaq Tailor"},
          "publisher": {"@type": "Organization", "name": "Ashfaq Tailor", "logo": {"@type": "ImageObject", "url": DOMAIN + "/images/brand/favicon-180.png"}}}
    h = head(x["title"] + " | Ashfaq Tailor", x["desc"], x["file"], '<script type="application/ld+json">' + json.dumps(ld) + '</script>\n')
    others = "".join(post_card(o) for o in POSTS if o["file"] != x["file"])
    body = page_hero(x["title"], x["desc"], "Blog") + f'''
<section class="section"><div class="container"><article class="prose">
 <p class="post-meta">By Ashfaq Tailor · {nice_date(x["date"])} · <a href="blog.html">All articles</a></p>
 {img(x["img"], x["alt"], "(min-width:900px) 740px, 92vw", cls="post-img", eager=True)}
 {x["body"]}
</article></div></section>
<section class="section section--ivory"><div class="container">{sec_head("Keep reading", "More from the blog", "")}<div class="grid grid--posts">{others}</div></div></section>
{cta_band("Ready to get your clothes stitched?")}'''
    return h + header("blog.html") + body + footer()

def build_404():
    h = head("Page not found | Ashfaq Tailor", "This page could not be found. Go back to the Ashfaq Tailor home page.", "404.html").replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    body = page_hero("Page not found", "Sorry, we could not find that page.", "Error") + f'<section class="section"><div class="container"><div class="btn-row"><a class="btn btn--gold" href="index.html">Go to home page</a>{wa_btn()}</div></div></section>'
    return h + header("") + body + footer()


# ------------------------------------------------------------------ hosting files (fix 404 on clean links)
HTACCESS = """# Apache / cPanel hosting
DirectoryIndex index.html
ErrorDocument 404 /404.html
RewriteEngine On
# /services -> services.html (works with or without .html)
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
# /index.html -> / (direct browser requests only, avoids loops)
RewriteCond %{THE_REQUEST} \\s/index\\.html[\\s?]
RewriteRule ^index\\.html$ / [R=301,L]
"""

REDIRECTS = """# Netlify / Cloudflare Pages
/index.html  /  301
/home        /  301
/service     /services.html  301
/services    /services.html  200
/our-work    /our-work.html  200
/work        /our-work.html  301
/shop        /shop.html  200
/blog        /blog.html  200
/how-to-use  /how-to-use.html  200
/privacy-policy  /privacy-policy.html  200
/about       /about.html  200
/contact     /contact.html  200
"""

VERCEL = """{
  "cleanUrls": true,
  "trailingSlash": false
}
"""

def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    pages = {"index.html": build_index(), "services.html": build_services(), "our-work.html": build_work(), "shop.html": build_shop(), "how-to-use.html": howto_page(), "blog.html": build_blog(),
             "privacy-policy.html": privacy_page(),
             "about.html": build_about(), "contact.html": build_contact(), "404.html": build_404()}
    for x in POSTS: pages[x["file"]] = build_post(x)
    for n, c in pages.items(): write(n, c)
    urls = "".join(f"<url><loc>{DOMAIN}/{'' if n == 'index.html' else n}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for n in pages if n != "404.html")
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    write(".htaccess", HTACCESS)
    write("_redirects", REDIRECTS)
    write("vercel.json", VERCEL)
    print("generated", ", ".join(pages))
