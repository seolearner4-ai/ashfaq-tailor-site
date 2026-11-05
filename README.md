# Ashfaq Tailor — Website

A fast, mobile-first website made of plain HTML, CSS and a little JavaScript. No framework, no build step, no database. Open `index.html` in a browser to preview it.

**Pages:** `index.html` (Home) · `services.html` · `our-work.html` · `shop.html` (Shop page) · `about.html` · `contact.html` · `404.html`

## Before you publish — please confirm these

1. **Phone numbers.** I took them from your logo: WhatsApp `0327-7938569`, phone `0311-4614341`. The shop sign photo shows different numbers, so please confirm which are correct.
2. **Opening hours** are empty on purpose. Until you add them, the site says "Message us on WhatsApp to confirm today's timings."
3. **Google Maps pin.** Until you add your Maps link, "Get Directions" searches Google Maps for the address.
4. **Your domain.** Replace the placeholder `https://YOUR-DOMAIN.com` (see section 10).
5. **Suggested wording** (editable): the owner message, the FAQ answers and the "How it works" steps. Check that they match how you really work, especially FAQ "How long does stitching take?" and "Do I need to visit for measurements?".

---

## 1–4. Change WhatsApp, phone, address, opening hours

Open **`js/site-config.js`** in any text editor (Notepad is fine). It is the only file you need for contact details. Change the value between the quotes, save, and upload the file again. Every page updates.

| What | Setting | Example |
|---|---|---|
| WhatsApp number | `whatsappNumber` | `"923277938569"` (92 + number without the first 0, no + or spaces) |
| WhatsApp shown on site | `whatsappDisplay` | `"0327-7938569"` |
| Phone (call button) | `phoneNumber` | `"+923114614341"` |
| Phone shown on site | `phoneDisplay` | `"0311-4614341"` |
| Address | `address` | street, city … |
| Opening hours | `hours` | see the example inside the file |
| Default WhatsApp message | `defaultMessage` | any text |
| Seasonal banner (Eid etc.) | `banner` | `enabled: true` and edit `text` |

The address in the page text and the search-engine data is also written in the HTML. If the address ever changes, search for `Street No. 1` in the `.html` files and replace it (or ask a developer to run `tools/generate.py` after editing it there).

## 5. Replace or add shop photos

Photos are in `images/shop/` (exterior and interior), `images/owner/` and `images/brand/`.

- **To replace a photo:** save the new photo as WebP (or convert at squoosh.app) and give it the **same file name** as the old one, e.g. `ashfaq-tailor-shop-exterior-faisalabad-941.webp`. Each photo has two sizes (e.g. `-640` and `-941`); replace both, or just the larger one.
- Keep the file names — they help Google understand the images.

## 6. Add portfolio photos

Portfolio photos are in `images/portfolio/`. Each work item is a block in `our-work.html` (and the Home page) that looks like:

```html
<figure class="work-item" data-cat="shirts"> ... </figure>
```

Easiest way: copy one existing `<figure class="work-item …>…</figure>` block, paste it below, then change the image file name, the title text and `data-cat` (`shalwar-kameez`, `kurta` or `shirts`). Upload your photo (width about 900 px, WebP, under 150 KB) to `images/portfolio/`. For many new photos, ask a developer to add them to `tools/generate.py` (list called `WORK`) and run `python3 tools/generate.py`.

## 7. Add real customer reviews

In `js/site-config.js`, fill the `reviews` list with **genuine** reviews only:

```js
reviews: [
  { name: "Customer name", text: "What the customer said." },
  { name: "Another customer", text: "…" }
],
```

The placeholder disappears automatically. Put your Google review link in `googleReviewUrl` so the button says **Read / Leave a Google Review**. No star ratings are shown, and none are in the search-engine data.

The same file has `beforeAfter` for real before/after alteration photos. That section stays hidden until you add some.

## 8. Connect Google Maps

1. Open Google Maps, find your shop (or add it with Google Business Profile).
2. **Share → Copy link** → paste into `mapUrl` in `js/site-config.js`. All "Get Directions" buttons now open your exact shop.
3. **Share → Embed a map →** copy only the `https://www.google.com/maps/embed?...` link inside `src="..."` → paste into `mapEmbedUrl`.

Tip: create a free **Google Business Profile** for Ashfaq Tailor. It matters most for "tailor near me" searches.

## 9. Connect Google Analytics and Search Console

1. Create a GA4 property at analytics.google.com and copy the Measurement ID (`G-XXXXXXXXXX`).
2. Paste it into `ga4Id` in `js/site-config.js`. Nothing is loaded until you do.
3. Events are already named for you: `whatsapp_click`, `phone_click`, `directions_click`, `inquiry_submit`, `style_chooser_whatsapp`, `lightbox_whatsapp_click`, `review_link_click`, `banner_click`. In GA4 → Admin → Events, mark the ones you care about as **Key events**.
4. Search Console: add your domain, verify it, then submit `https://your-domain/sitemap.xml`.

## 10. Deploy (publish)

1. Buy a domain (for example from a Pakistani registrar or Namecheap).
2. Set your address everywhere in one step: `python3 tools/set_domain.py https://www.yourdomain.com` (or use Find & Replace in all files for `https://YOUR-DOMAIN.com`). Also put it in `siteUrl` in `js/site-config.js`.
3. Upload the whole folder to a free static host. Easiest options:
   - **Netlify** — drag and drop the folder at app.netlify.com/drop, then add your domain.
   - **Cloudflare Pages** or **GitHub Pages** — also free.
   - Any normal web hosting — upload the folder contents to `public_html`.
4. Check the live site on your phone: WhatsApp, Call and Directions buttons.

## 404 error on buttons — hosting notes

All links inside the site are relative (`services.html`, `shop.html` ...) and a local crawl finds no broken file. If you still see 404 online, it is the hosting setup:

- Upload the **contents** of the folder (so `index.html` sits at the top level), not the folder itself.
- Do not open the site from inside the zip file; extract it first.
- The folder now includes `.htaccess` (Apache/cPanel), `_redirects` (Netlify / Cloudflare Pages) and `vercel.json` (Vercel), so `/services`, `/shop`, `/contact` also work without `.html`.

## SEO checklist (do these after publishing)

1. Run `python3 tools/set_domain.py https://www.yourdomain.com`. **Until you do this, canonical links, sitemap and search data point to the placeholder domain, and Google will not rank the real site.**
2. Create a free Google Business Profile for Ashfaq Tailor (most important for "tailor near me" in Faisalabad) and paste the Maps link in `mapUrl`.
3. Add the site in Google Search Console and submit `sitemap.xml`.
4. Add real customer reviews and Google review link (see section 7).

## Urdu version later

Pages use `lang="en"` and `dir="ltr"`, and the CSS uses direction-aware spacing. To add Urdu: copy the pages into a folder `ur/`, set `lang="ur" dir="rtl"`, translate the text, and add `hreflang` links.

## Notes

- All photos are optimized WebP with correct dimensions and lazy loading.
- The inquiry form needs no server: it opens WhatsApp with a ready message.
- Never add fake reviews, ratings or prices — Google can penalise that, and customers notice.
