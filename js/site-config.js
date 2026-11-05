/* ============================================================
   ASHFAQ TAILOR — SITE SETTINGS
   This is the ONLY file you need to edit to change contact
   details, hours, links, banner, reviews and analytics.
   Save the file, upload it again, and every page updates.
   ============================================================ */
window.SITE = {

  businessName: "Ashfaq Tailor",
  ownerName: "Faizan Ali",

  /* Your real website address (no slash at the end). */
  siteUrl: "https://YOUR-DOMAIN.com",

  /* --- WhatsApp: country code + number, digits only, no + or 0 at start.
        0327-7938569  ->  923277938569
        (Number taken from the shop logo. Please confirm it.) --- */
  whatsappNumber: "923277938569",
  whatsappDisplay: "0327-7938569",

  /* --- Phone calls: international format for the call button. --- */
  phoneNumber: "+923277938569",
  phoneDisplay: "03277938569",

  address: {
    street: "Street No. 1, Iqbal Town, GM Abad",
    city: "Faisalabad",
    region: "Punjab",
    country: "PK",
    countryName: "Pakistan"
  },

  /* --- Opening hours. Leave the list EMPTY until you confirm them:
        the site then shows "message us to confirm timings".
        Example of how to fill it:
        hours: [
          { label: "Monday – Saturday", days: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], opens: "10:00", closes: "21:00", display: "10:00 AM – 9:00 PM" },
          { label: "Sunday", closed: true }
        ]
  --- */
  hours: [],

  /* --- Google Maps ---
     mapUrl: paste the "Share > Copy link" of your shop on Google Maps.
             Used by every "Get Directions" button.
     mapEmbedUrl: from Google Maps > Share > Embed a map > copy the src="..." link only.
     If both are empty, the site searches Google Maps for the address. */
  mapUrl: "",
  mapEmbedUrl: "",

  /* --- Google Reviews: paste your "Get more reviews" link. --- */
  googleReviewUrl: "",

  /* --- Social links: leave "" if you do not have one (it will be hidden). --- */
  social: {
    facebook: "https://www.facebook.com/share/1F3LFsWmyc/",
    instagram: "https://www.instagram.com/ashfa.qtailor?psln=MTB0bnZwaWNzM3k1NA==",
    tiktok: "https://www.tiktok.com/@ahsfaq.tailor?_r=1&_t=ZS-9Ahfs4FduSq"
  },

  /* --- Google Analytics 4: paste your Measurement ID like "G-XXXXXXXXXX". --- */
  ga4Id: "",

  /* --- Default WhatsApp message (used by WhatsApp buttons). --- */
  defaultMessage: "Assalam-o-Alaikum Ashfaq Tailor, I found your website and would like information about stitching.",

  /* --- Seasonal banner. Set enabled: true to show it on every page. --- */
  banner: {
    enabled: false,
    text: "Eid stitching slots are filling — contact us to check availability.",
    linkText: "Message us on WhatsApp"
  },

  /* --- Real customer reviews. Add ONLY genuine ones, for example:
        { name: "Customer name", text: "What they said." }
  --- */
  reviews: [],

  /* --- Real before/after photos (alterations etc.). The section stays hidden while empty.
        { before: "images/portfolio/before-1.webp", after: "images/portfolio/after-1.webp", caption: "Trouser length alteration" }
  --- */
  beforeAfter: [],

  /* --- Choose Your Style options. Add or remove words here. --- */
  styleOptions: {
    garments: ["Shalwar Kameez", "Kurta", "Shirt", "Pant", "Waistcoat"],
    fits: ["Regular Fit", "Slim Fit", "Relaxed Fit"]
  }
};
