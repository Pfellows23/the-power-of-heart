# The Power of Heart website (thepowerofheart.com)

Plain HTML and CSS, with no build step and no JavaScript. Every page has its
menu, text, and footer written right into the HTML, so search engines can
read everything. Upload every file in this folder to your host's public folder.

## Pages
| Page | File |
|---|---|
| Home | index.html |
| About | about.html |
| Services (coaching, spiritual teaching, Stripe checkout) | services.html |
| Projects (The Hearts of Mauna Kea, artistic projects) | projects.html |
| Contact (book a discovery call) | contact.html |

## Stripe payment links
Every Buy or Pay button points to a placeholder like
`https://buy.stripe.com/REPLACE_SINGLE_SESSION`. Search for `REPLACE_` and paste
the matching Stripe Payment Link in its place:

- REPLACE_SINGLE_SESSION: services.html
- REPLACE_COACHING_PACKAGE: services.html
- REPLACE_PROGRAM_1, REPLACE_PROGRAM_2: services.html
- REPLACE_BOOK_HEARTS_OF_MAUNA_KEA: index.html and projects.html
- REPLACE_PRODUCT_1, _2, _3: projects.html

## Booking link
Every "Book a discovery call" button opens https://calendly.com/pamela-thepowerofheart/30min. To change it, edit BOOKING at the top of build.py and run it.

## Menu
The menu sits between `<!-- MENU START -->` and `<!-- MENU END -->` at the top
of each page. Change it on one page, then copy that block to the other pages.
The only difference between pages is `aria-current="page"`, which marks the
page you're on.

## SEO already included
- A unique title and description on every page
- Canonical URLs on https://www.thepowerofheart.com
- Social sharing tags (add an image at images/share-image.jpg, 1200×630)
- Structured data for the business, the services, and the book
- sitemap.xml and robots.txt. Submit the sitemap in Google Search Console after launch.

When you leave Squarespace, ask your host to redirect old page URLs
(for example /products-programs) to the new pages so search rankings carry over.

## Beach photos (they appear automatically)
Put these three photos in the `images` folder with exactly these names:
- `mauna-kea-beach.jpg`: the large photo behind the home page heading, and a band on Projects
- `hendrys-beach.jpg`: Hendry's Beach, Santa Barbara (Home and About)
- `sea-foam.jpg`: white sea foam on sand (above the booking section on every page)
Wide, landscape photos at least 2000 pixels across work best.

## Other photos
Make an `images` folder. Replace a placeholder like
`<div class="photo"><span class="photo-label">…</span></div>` with
`<div class="photo"><img src="images/photo.jpg" alt="Describe the photo"></div>`.

Text in [square brackets] is a placeholder for your own copy.

## Password-protected book preview
book-preview.html is a click-through preview of The Hearts of Mauna Kea. It's
hidden from search engines and left out of the menu and sitemap. A plain HTML
site can't check passwords by itself, so the password is set at your host:
- **Cloudflare Pages** (free): protect `/book-preview.html` with Cloudflare Access.
- **Netlify**: add password protection for that path in Site settings (paid plans).
Ask your host or web helper to protect that one page and choose the password.

## Hosting on Railway
The site deploys to Railway from this GitHub repo. `Dockerfile` and `Caddyfile`
run a small Caddy web server that serves these files on the port Railway gives
it, and `railway.json` tells Railway to use them. Pages also work without
`.html` (for example `/about`). `build.py`, this README, and the server files
are kept out of the public site.

Every push to `main` redeploys the site automatically.
