import json, os, html, hashlib

OUT = os.path.dirname(os.path.abspath(__file__))
# Changes whenever styles.css changes, so browsers fetch the new stylesheet instead of a cached one.
CSS_V = hashlib.md5(open(os.path.join(OUT, "styles.css"), "rb").read()).hexdigest()[:8]
BASE = "https://www.thepowerofheart.com"
NAME = "The Power of Heart"
EMAIL = "pamela@thepowerofheart.com"
BOOKING = "https://calendly.com/pamela-thepowerofheart/30min"

MENU = [("Home", "index.html"), ("About", "about.html"), ("Services", "services.html"),
        ("Projects", [("Books", "books.html"), ("Productions", "productions.html")]), ("Inspirations", "inspirations.html")]
FOOTER_MENU = [(l, h) for l, h in MENU if isinstance(h, str)][:3] + [("Books", "books.html"), ("Productions", "productions.html"), ("Inspirations", "inspirations.html"), ("Contact", "contact.html")]

FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap"

WAVE = '<svg class="wave{cls}" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0,44 C220,78 460,6 720,30 C980,54 1210,12 1440,38 L1440,80 L0,80 Z"/></svg>'
def wave(cls=""): return ""
SHORE = ''
SIZES = {"stone-buddha.jpg": (1013, 758), "coral-heart-in-hand.jpg": (1168, 800), "ocean-sparkle.jpg": (980, 1095), "hendrys-beach.jpg": (2000, 743), "golden-water.jpg": (982, 1236), "sea-foam.jpg": (2000, 1278), "coral-heart-rocks-on-lava.jpg": (1446, 1356), "silver-ocean.jpg": (1452, 1362), "heart-rocks-sandstone.jpg": (1340, 1362), "shoreline-pebbles.jpg": (1452, 1360), "pamela-sunset-beach.jpg": (880, 1100), "hearts-of-hendrys-cover.jpg": (1016, 762)}

def img(name, alt, cls="", eager=False):
    w, h = SIZES[name]
    load = ""
    return f'<div class="photo {cls}"><img src="images/{name}" alt="{alt}" width="{w}" height="{h}"{load} decoding="async"></div>'

def band(img, place, where):
    return f'''<figure class="band" style="--photo: url('images/{img}')">
</figure>'''
FOAM = band("sea-foam.jpg", "White sea foam", "Where the ocean meets the shore")
MKB = band("coral-heart-rocks-on-lava.jpg", "Coral hearts on lava rock", "Gifts from the shore")
HENDRY = band("hendrys-beach.jpg", "Hendry's Beach", "Santa Barbara · California")

def book_img(name, alt):
    return f'<figure class="book-mock"><img src="images/{name}" alt="{alt}" width="614" height="520" loading="lazy" decoding="async"></figure>'

def stripe(key): return f"https://buy.stripe.com/REPLACE_{key}"

def header(slug):
    def li(label, href):
        if isinstance(href, list):
            cur = any(h == slug for _, h in href)
            subs = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == slug else ""}>{l}</a></li>' for l, h in href)
            return (f'      <li class="has-sub"><details><summary{" class=\"current\"" if cur else ""}>{label}</summary>'
                    f'<ul class="sub">{subs}</ul></details></li>')
        return f'      <li><a href="{href}"{" aria-current=\"page\"" if href == slug else ""}>{label}</a></li>'
    items = "\n".join(li(l, h) for l, h in MENU)
    return f'''<header id="site-header">
  <div class="bar">
    <a class="brand" href="index.html">{NAME}</a>
    <!-- MENU START: edit the menu here, then copy this block to every page -->
    <nav id="site-menu" aria-label="Main">
      <ul>
{items}
      </ul>
      <a class="btn btn-small" href="{BOOKING}" target="_blank" rel="noopener">Book a discovery call</a>
    </nav>
    <!-- MENU END -->
  </div>
</header>'''

def footer():
    links = "\n".join(f'      <a href="{h}">{l}</a>' for l, h in FOOTER_MENU)
    return f'''<footer id="site-footer">
  <div class="footer-inner">
    <div>
      <p class="footer-name">{NAME}</p>
      <p class="footer-tag">Coaching and spiritual teaching rooted in ancient lineages, creative projects, and The Hearts of… book series.</p>
    </div>
    <nav class="footer-links" aria-label="Footer">
{links}
    </nav>
    <div class="footer-contact">
      <p><a href="mailto:{EMAIL}" style="color:inherit">{EMAIL}</a></p>
      <p class="footer-social"><!-- Add social links, e.g. <a href="https://instagram.com/yourname">Instagram</a> --></p>
    </div>
  </div>
  <p class="footer-copy">© 2026 {NAME}. All rights reserved.</p>
</footer>'''

def page(slug, title, desc, body, schema=None):
    url = BASE + "/" + ("" if slug == "index.html" else slug)
    ld = ""
    if schema:
        ld = '\n<script type="application/ld+json">\n' + json.dumps(schema, indent=2, ensure_ascii=False) + "\n</script>"
    t, d = html.escape(title), html.escape(desc)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/images/share-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="styles.css?v={CSS_V}">{ld}
</head>
<body>
{header(slug)}
<main>
{body}
</main>
{REQUEST_MODAL if 'href="#request-book"' in body else ''}
{REQUEST_MODAL_HENDRYS if 'href="#request-hendrys"' in body else ''}
{footer()}
</body>
</html>
'''

ORG = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": NAME,
       "url": BASE + "/", "email": EMAIL, "image": BASE + "/images/share-image.jpg",
       "description": "Heart-focused alignment coaching and spiritual teaching for individual clients, plus creative projects and The Hearts of… book series.",
       "areaServed": "Worldwide", "founder": {"@type": "Person", "name": "Pamela"}}

CTA = f'''{FOAM}
<section class="section section-tide">
  <div class="wrap cta">
    <div>
      <p class="eyebrow">Start here</p>
      <h2>Book a free discovery call</h2>
      <p>A relaxed conversation about where you are, where you want to go, and whether working together feels right.</p>
    </div>
    <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Choose a time</a>
  </div>
</section>'''

PILLARS = '<ul class="pillars" aria-label="What clients move toward"><li>Peace</li><li>Fulfillment</li><li>Joy</li><li>Clarity</li><li>Abundance</li></ul>'

home = f'''<section class="hero hero-photo" style="--photo: url('images/ocean-sparkle.jpg')">
  <div class="wrap hero-grid">
    <div class="hero-text stack-lg">
      <h1>Ancient wisdom.<br><em>Undiscovered awareness.</em></h1>
    </div>
    <a class="hero-cover" href="books.html" aria-label="The Hearts of Mauna Kea book">
      {img("coral-heart-in-hand.jpg", "The Hearts of Mauna Kea: a heart-shaped piece of coral held on a sandy beach")}
    </a>
  </div>
</section>
<div class="hero-after">
  <div class="wrap">
    <p class="lede">Coaching rooted across ancient lineages and merged with modern-day insight, for the awareness most of modern life has left undiscovered: the intelligence of the heart.</p>
    <div class="actions">
      <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Book a discovery call</a>
      <a class="btn btn-ghost" href="services.html">Explore services</a>
    </div>
  </div>
</div>

<section class="section heartfulness" id="heartfulness">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="thread-line">When everything else feels elusive, something in you still knows. Beneath the noise, there is an awareness of what wants to be known.</p>
      <p class="eyebrow">Why the heart</p>
      <h2>The oldest intelligence <em>we have</em></h2>
      <p class="lede">Long before anyone studied the mind, the great wisdom traditions pointed to the heart as the seat of knowing. Most of us were never taught how to use it.</p>
      <p>This is not sentiment. The heart is a center of intelligence, where intuition, courage, and truth meet. The mind can analyze a life, but only the heart can tell you whether it is yours. When it leads, decisions become clear, relationships become honest, and purpose stops being something to chase and becomes something to live.</p>
      <p>Mindfulness taught a generation to quiet the mind. Heartfulness is the next step, and it has never mattered more. In a world that is louder, faster, and more divided than ever, a quiet mind is no longer enough. The awareness these traditions have guarded all along is still waiting to be discovered.</p>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Ways to work together</p>
      <h2>Find your way in</h2>
    </div>
    <div class="paths">
      <article class="path">
        <h3>Alignment Coaching</h3>
        <p>One-to-one work, grounded in ancient practice, to bring the way you live into line with what you most deeply know.</p>
        <a class="more" href="services.html">Coaching services</a>
      </article>
      <article class="path">
        <h3>Spiritual Teaching</h3>
        <p>Teachings, gatherings, and practices that help you reconnect with your purpose and the wisdom within.</p>
        <a class="more" href="services.html">Teaching offerings</a>
      </article>
      <article class="path">
        <h3>Projects &amp; Books</h3>
        <p>The Hearts of Mauna Kea pairs photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning.</p>
        <a class="more" href="books.html">See the books</a>
      </article>
    </div>
  </div>
</section>
{HENDRY}

<section class="section">
  <div class="wrap split">
    {img("coral-heart-rocks-on-lava.jpg", "White coral hearts resting on black lava rock", "wide")}
    <div class="stack">
      <p class="eyebrow">Featured project</p>
      <h2>The Hearts of Mauna Kea</h2>
      <p>The first book in The Hearts of… series pairs photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning.</p>
      <div class="actions">
        <a class="btn" href="#request-book">Buy the book</a>
        <a class="btn btn-ghost" href="book-preview.html">Look inside the book</a>
      </div>
      <p class="secure-note">The book preview is password protected.</p>
    </div>
  </div>
</section>
{CTA}'''

about = f'''<section class="page-hero about-hero">
  <div class="wrap">
    {img("pamela-sunset-beach.jpg", "Pamela in a woven hat, looking out to sea in golden evening light at Hendry's Beach")}
    <div class="about-intro">
      <h1>Hello and welcome</h1>
      <p class="lede">My work serves the journey of the soul: helping you live the dharma and the purpose you came here to fulfill.</p>
      <p>Everything I offer was first given to me. My coaching draws on years of study with lineage holders across acting, leadership, transformation, yoga, meditation, and Buddhism. Each tradition opened a different doorway into the same truth, and together they shape how I listen, guide, and walk beside the people I work with.</p>
      <p>I have been a student of teachers who carry living lineages, each one handed down from teacher to student over generations. This is the ground my coaching stands on. And it is why I teach: I am grateful for every teacher I have ever had, and passing on what they gave me is how I honor them.</p>
      <div class="actions">
        <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Book a discovery call</a>
        <a class="btn btn-ghost" href="services.html">Explore services</a>
      </div>
    </div>
  </div>
</section>
{HENDRY}
<section class="section section-sand">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">The lineages behind this work</p>
      <h2>Many lineages, in support of truth and authenticity</h2>
    </div>
    <div class="offers bold-heads">
      <div class="offer"><h3>Acting</h3><p>A graduate of the Meisner Technique Acting Studio, where the practice is presence itself: listening fully and responding truthfully, moment to moment.</p></div>
      <div class="offer"><h3>Leadership</h3><p>Training in leading a life and a body of work from clarity and inner alignment, and in helping others do the same.</p></div>
      <div class="offer"><h3>Transformation</h3><p>Certified in Women's Energetics, the study of the subtle energy that moves through us and how real change takes root.</p></div>
      <div class="offer"><h3>Yoga</h3><p>More than 1,000 hours of RYT certification, grounded in the body, the breath, and the wisdom traditions of yoga.</p></div>
      <div class="offer"><h3>Meditation</h3><p>Over ten years of teaching meditation and chakra meditation, guiding people beyond the busy mind and home to their own center.</p></div>
      <div class="offer"><h3>Buddhism</h3><p>Teachings on awareness, compassion, and the nature of mind, received from teachers within the tradition.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">What I specialize in</p>
      <h2>Support for the turning points</h2>
      <p>People often find me when life is asking something new of them. These are the places I know best.</p>
    </div>
    <div class="paths bold-heads">
      <div class="stack"><h3>Relationships</h3><p>Coaching for the relationships that matter most, beginning with the one you have with yourself, so you can love and be loved from a whole heart.</p></div>
      <div class="stack"><h3>Women's coaching</h3><p>For women who hold many roles and carry many gifts, and who want to honor every part of who they are instead of choosing just one.</p></div>
      <div class="stack"><h3>Transition and awakening</h3><p>Steady support through times of change, through the dark night of the soul when the old life falls away, and through the awakening that follows.</p></div>
    </div>
  </div>
</section>
<section class="section section-sand">
  <div class="wrap quote">
    <p class="eyebrow">My commitment</p>
    <p class="q">These are not my teachings. I have received the empowerments to teach, and my part is to share what has been shared with me.</p>
    <p>I hold that as a responsibility and a gift. What my teachers passed to me was never meant to stop with me. It is meant to move through me, person to person and heart to heart, in service of your highest and most aligned path.</p>
    <p>To that end, my work is simple: to empower, to align, and to create connections that elevate.</p>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="stack">
      <p class="eyebrow">Who this coaching is for</p>
      <h2>For finders of truth, <em>not only seekers</em></h2>
    </div>
    <div class="stack">
      <p class="lede">This work is for those who want to be finders of truth, rather than seekers of an elusive point of arrival.</p>
      <p>Seeking can go on forever, always one more book, one more retreat, one more someday. Finding happens here, in your own heart and your own life. If you are ready to stop circling and start living your dharma, with peace, clarity, and purpose, this coaching is for you.</p>
    </div>
  </div>
</section>
{CTA}'''

def product(title, meta, price, text, key, label="Buy now", photo=None, href=None):
    ph = ""
    ext = ' target="_blank" rel="noopener"' if href else ""
    return f'''      <article class="product">
        {ph}<h3>{title}</h3>
        <p class="meta">{meta}</p>
        <p class="price">{price}</p>
        <p>{text}</p>
        <a class="btn" href="{href or stripe(key)}"{ext}>{label}</a>
      </article>'''

REEL_FRAMES = [("ocean-sparkle.jpg", "Sunlight sparkling on the ocean"), ("coral-heart-in-hand.jpg", "A heart-shaped piece of coral held in a hand"), ("golden-water.jpg", "Golden evening light on gentle waves"), ("sea-foam.jpg", "White sea foam on the sand"), ("heart-rocks-sandstone.jpg", "Heart-shaped stones beside a sandstone boulder"), ("silver-ocean.jpg", "Silver light on the open ocean"), ("shoreline-pebbles.jpg", "Pebbles along the shoreline")]
# Pamela's inspirations (added 2026-11-19). The screen line shows over the nature frames only,
# so it never sits on top of a quote.
REEL_INSPIRATIONS = [
    ("insp-swami-om.jpg", "A sign with a teaching on happiness by Swami Purushottamananda"),
    ("insp-grateful-spiral.jpg", "Spiral lettering: I am grateful for everything I know, everything I am, everything I have"),
    ("insp-life-is-beautiful.jpg", "Children cuddled close in golden light, with the words Life is beautiful"),
    ("insp-mary-oliver.jpg", "Mary Oliver: Keep some room in your heart for the unimaginable"),
    ("insp-little-prince.jpg", "The Little Prince: If someone loves a flower, of which just one exists in all the millions and millions of stars"),
    ("insp-sunlit-portrait.jpg", "Pamela in warm sunlight"),
    ("insp-what-if-rock.jpg", "A painted heart rock: What if everything you are going through right now is preparing you for a dream bigger than you can imagine"),
    ("insp-and-then-one-day.jpg", "An open book on the beach at sunset: and then one day"),
    ("insp-happiness-sign.jpg", "A sign: Happiness is letting go of what you think your life is supposed to look like"),
    ("insp-choose-love.jpg", "A framed sign: Choose love. Be kind. Find joy. Feel happy. Smile."),
]
REEL_ALL = REEL_FRAMES  # REEL_INSPIRATIONS removed from the reel at Pamela's request (2026-11-20)
REEL_SECS = 6
def _frames():
    return "".join(f'<img src="images/{n}" alt="{a}" width="800" height="600" style="--i:{i}" loading="{'eager' if i < 2 else 'lazy'}" decoding="async">' for i, (n, a) in enumerate(REEL_ALL))
def _reel_style():
    n = len(REEL_ALL); total = n * REEL_SECS; one = 100 / n
    line_end = len(REEL_FRAMES) * one
    return (f"<style>.screen img {{ animation-duration: {total}s, 0.9s; }}"
            f"@keyframes screen-show {{ 0% {{ opacity: 0; }} {one*0.18:.2f}% {{ opacity: 1; }} {one:.2f}% {{ opacity: 1; }} {one*1.18:.2f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}"
            + ((f".screen-line {{ animation: screen-line {total}s linear infinite; }}"
            f"@keyframes screen-line {{ 0%, {line_end - one*0.25:.2f}% {{ opacity: 1; }} {line_end:.2f}%, {100 - one*0.2:.2f}% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}"
            f"@media (prefers-reduced-motion: reduce) {{ .screen-line {{ animation: none; }} }}") if len(REEL_ALL) > len(REEL_FRAMES) else "")
            + "</style>")
REEL = f'''<figure class="screen-wrap">
  {_reel_style()}
  <div class="screen">
    {_frames()}
    <figcaption class="screen-line">We all want to see our most <em>authentic story</em> play out.</figcaption>
  </div>
</figure>'''

services = f'''<section class="page-hero">
  <div class="wrap stack measure">
    <p class="eyebrow">Services</p>
    <h1>Live your life <em>aligned</em></h1>
    <p class="lede">Specialized coaching and spiritual teaching for individual clients, to bring you into inner alignment and empower you along your path of purpose.</p>
  </div>
  {REEL}
</section>

<section class="section" id="coaching" style="padding-top:0">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <h2>The mind can only take you <em>so far</em></h2>
      <p class="lede">After that, how fulfilled you feel in your life comes down to the heart.</p>
      <p>The mind is a brilliant tool. It can plan, solve, and achieve. But it does not drive itself. What moves it is something deeper: what resonates with you, what you love, what feels true. For too long that has been overlooked, and it is why so many people reach their goals and still feel that something is missing.</p>
      <p>Specialized coaching begins there. Together we listen for what truly resonates, and empower what drives the mind, so your choices, your work, and your relationships line up with who you really are.</p>
    </div>
    <div class="products">
{product("Discovery Call", "30 minutes · Zoom or phone", "Free", "A first conversation to see if we are a good fit.", "", "Book", href=BOOKING)}
{product("Single Coaching Session", "45 minutes", "$108", "One session, one commitment: to meet you where you are, bring what you know into alignment with how you live, and leave with a clear path forward.", "", "Book", href=BOOKING)}
{product("Three-Month Coaching", "6 sessions · every other week", "$444", "The work I recommend. Insight can arrive in a single session, but lasting change takes root over time. Across three months we set a clear intention, carry it into your daily life, and return to it every two weeks to refine what you are learning, until alignment is no longer something you visit but the way you live.", "", "Book", href=BOOKING)}
    </div>
  </div>
</section>

{CTA}'''

services_schema = {"@context": "https://schema.org", "@type": "Service", "name": "Heart-focused coaching and spiritual teaching",
                   "provider": {"@type": "ProfessionalService", "name": NAME, "url": BASE + "/"},
                   "serviceType": "Life coaching", "areaServed": "Worldwide",
                   "description": "Inner alignment coaching for individual clients, connecting them with peace, fulfillment, joy, clarity, and abundance."}

books = f'''<section class="page-hero">
  <div class="wrap stack measure">
    <p class="eyebrow">Projects</p>
    <h1>The Hearts of Mauna Kea</h1>
    <p class="lede">This book pairs photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split">
    {book_img("book-hearts-of-mauna-kea.webp", "Hearts of Mauna Kea, Reflections of Love and Gratitude: book cover showing a heart-shaped piece of coral held on the beach")}
    <div class="stack">
      <p class="eyebrow">Book one of The Hearts of… series</p>
      <h2>About the book</h2>
      <p><em>Hearts of Mauna Kea</em> is a visually captivating coffee table book that celebrates the spirit, beauty, and timeless legacy of the Mauna Kea Beach Hotel on the Island of Hawai‘i. Through Pamela Fellows’ original photography and reflective prose, the book captures the profound sense of love and aloha that has defined this extraordinary place for generations.</p>
      <dl class="field-note">
        <dt>Price</dt><dd>$88</dd>
        <dt>Place</dt><dd>Mauna Kea Beach Hotel, Kauna‘oa Bay, Hawai‘i Island</dd>
      </dl>
      <div class="actions">
        <a class="btn" href="#request-book">Buy the book</a>
      </div>
    </div>
  </div>
</section>

<section class="testimonials" aria-label="What readers say">
  <div class="wrap">
    <p class="eyebrow">What readers say</p>
    <div class="quote-rotator">
      <figure class="quote"><blockquote>“This is the only book I have ever seen that has made the real true connection between reality and the magic of the Mauna Kea. It’s such a special place that deserves to be appreciated in this way.”</blockquote><figcaption>Grier Eliasek<span>Resident and long-time visitor of the Mauna Kea</span></figcaption></figure>
      <figure class="quote"><blockquote>“This is my 38th year coming to the Mauna Kea, and after reading this book it seems to be an ideal gift to every single guest upon check-in, because it captures the uniqueness and essence of this beautiful property.”</blockquote><figcaption>Jim Jarrett<span>Filmmaker, actor, teacher</span></figcaption></figure>
      <figure class="quote"><blockquote>“I think those who have returned to the Mauna Kea would appreciate giving and receiving this gift.”</blockquote><figcaption>Marcia Ray<span>In-residence artist of the Mauna Kea</span></figcaption></figure>
      <figure class="quote"><blockquote>“Tell Brad I like it!”</blockquote><figcaption>Vicky Kometani<span>PR consultant, Mauna Kea Resort</span></figcaption></figure>
      <figure class="quote"><blockquote>“Hearts of Mauna Kea is a wonderful manuscript with some very enlightening messages for us all.”</blockquote><figcaption>Bradley D. Doell</figcaption></figure>
    </div>
  </div>
</section>

<section class="section" id="hearts-of-hendrys">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <h2 class="h1-size">Hearts of Hendry's</h2>
      <p class="lede">Listening from the Beach.</p>
    </div>
    <div class="split">
      {book_img("book-hearts-of-hendrys.webp", "Hearts of Hendry's, Listening from the Beach: book cover showing a heart-shaped stone held up against a sunset over the ocean")}
      <div class="stack">
        <p class="eyebrow">Book two of The Hearts of… series</p>
        <h3 class="h2-size">About the book</h3>
        <p>The second book in the Hearts of… series turns to Hendry's Beach in Santa Barbara. Tide-worn heart rocks, coastal light and the quiet teachings of this shoreline, gathered over years of experiencing it.</p>
        <dl class="field-note">
          <dt>Price</dt><dd>$88</dd>
          <dt>Place</dt><dd>Hendry's Beach, Santa Barbara, California</dd>
        </dl>
        <div class="actions">
          <a class="btn" href="#request-hendrys">Buy the book</a>
        </div>
      </div>
    </div>
  </div>
</section>
{MKB}
<section class="section section-sand">
  <div class="wrap cta">
    <div>
      <p class="eyebrow">Inside The Hearts of Mauna Kea</p>
      <h2>Turn the pages</h2>
      <p>Step through the book one spread at a time. The preview is password protected.</p>
    </div>
    <a class="btn btn-ghost" href="book-preview.html">Look inside the book</a>
  </div>
  <a class="wrap inside-photo" href="book-preview.html" aria-label="Look inside The Hearts of Mauna Kea">
      <img class="inside-framed" src="images/stone-buddha.jpg" alt="A stone Buddha resting beneath a tree in Hawaiian sunlight" width="1013" height="758" loading="lazy" decoding="async">
    
  </a>
</section>
{wave("wave-flip")}
{CTA}'''

productions = f'''<section class="page-hero" id="in-the-works">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Productions</p>
      <h1>In the <em>works</em></h1>
      <p>Two acclaimed one-man plays, both performed by Jim Jarrett, coming to Santa Barbara as benefit engagements through Wilder Creative Productions.</p>
    </div>
    <div class="plays">
      <article class="play">
        <img class="play-poster" src="images/play-vincent.jpg" alt="Poster for Vincent: Jim Jarrett as Theo van Gogh over a painted landscape" width="640" height="887" loading="lazy" decoding="async">
        <div class="play-text">
        <p class="meta">Coming soon · Santa Barbara</p>
        <h3>Vincent</h3>
        <p class="play-by">By Leonard Nimoy · starring Jim Jarrett</p>
        <p>Paris, 1890. A week after Vincent van Gogh's death, his brother Theo rents a hall to tell the story he could not speak at the funeral, with Vincent's paintings projected behind him. Seen by a quarter of a million people on four continents.</p>
        </div>
      </article>
      <article class="play">
        <img class="play-poster" src="images/play-meisner.jpg" alt="Poster for Meisner: a line drawing of Sanford Meisner" width="616" height="900" loading="lazy" decoding="async">
        <div class="play-text">
        <p class="meta">Coming soon · Santa Barbara</p>
        <h3>Meisner</h3>
        <p class="play-by">Created, performed, and directed by Jim Jarrett</p>
        <p>Two acts, thirty years apart, with the legendary acting teacher Sanford Meisner, brought to life by his last teaching protégé. "As close as you're ever going to get to experiencing the genius of Sanford Meisner." Jon Voight</p>
        </div>
      </article>
    </div>
  </div>
</section>
{CTA}'''

book_schema = {"@context": "https://schema.org", "@type": "Book", "name": "The Hearts of Mauna Kea",
               "author": {"@type": "Person", "name": "Pamela"}, "url": BASE + "/books.html",
               "isPartOf": {"@type": "BookSeries", "name": "The Hearts of…"},
               "about": "Photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning."}

contact = f'''<section class="page-hero" id="book">
  <div class="wrap split">
    <div class="stack">
      <p class="eyebrow">Contact</p>
      <h1>Let's talk</h1>
      <p class="lede">Book a free 30-minute discovery call by phone or video. No preparation needed, just come as you are.</p>
      <ul class="checklist">
        <li>Share where you are and what feels out of alignment</li>
        <li>Talk about what you want to create next</li>
        <li>Hear how coaching works and whether it fits you</li>
        <li>Leave with at least one clear next step</li>
      </ul>
    </div>
    <div class="booking-box">
      <h2>Book a discovery call</h2>
      <p>Pick a time that works for you. You will get a confirmation email with the details.</p>
      <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Open the booking calendar</a>
      <p class="muted">Or write to <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </div>
</section>
{wave()}
<section class="section section-sand">
  <div class="wrap stack-lg">
    <div class="stack measure"><p class="eyebrow">Questions</p><h2>Before you book</h2></div>
    <div class="offers">
      <div class="offer"><h3>Is the call really free?</h3><p>Yes. It is a chance for us both to see if working together feels right.</p></div>
      <div class="offer"><h3>Where does it happen?</h3><p>[Zoom, phone, or in person.]</p></div>
      <div class="offer"><h3>How do I pay for sessions?</h3><p>Each service has a secure Stripe checkout link on the <a href="services.html">Services</a> page.</p></div>
      <div class="offer"><h3>What happens after?</h3><p>If we decide to work together, I will send details on next steps.</p></div>
    </div>
  </div>
</section>
{FOAM}'''

def rock(cls, place, note):
    return f'''      <figure class="project">
        {img(cls[0], cls[1], "square")}
        <figcaption><p>{note}</p></figcaption>
      </figure>'''

# Film clips on the Inspirations page. Paste a YouTube link in place of "" to show the video.
FILMS = [
    ("Roberto Benigni on the Ten Commandments", "", "https://youtu.be/EatwzkvOWf4"),
    ("[Film title and scene]", "[A line or two on what this scene teaches.]", ""),
]
def more_films():
    rest = [f for f in FILMS[1:] if f[2]]
    if not rest: return ""
    return '    <div class="films">\n' + chr(10).join(film(*f) for f in rest) + '\n    </div>'

def film(title, note, url, feature=False):
    import re
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})", url or "")
    if m:
        frame = f'<iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" title="{title}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
    else:
        frame = '<p class="film-soon">Clip coming soon</p>'
    watch = f'\n        <p><a class="more" href="https://www.youtube.com/watch?v={m.group(1)}" target="_blank" rel="noopener">Watch on YouTube</a></p>' if m else ""
    cls = "film film-feature" if feature else "film"
    return f'''      <article class="{cls}">
        <div class="film-frame">{frame}</div>
        <h3>{title}</h3>
        {f'<p>{note}</p>' if note else ''}{watch}
      </article>'''

def teaching(text, place):
    return f'''      <div class="teaching">
        <blockquote>{text}</blockquote>
        <p class="meta muted" style="font-size:.8rem;letter-spacing:.14em;text-transform:uppercase">{place}</p>
      </div>'''

# Hidden until Pamela fills it in: change `if True` to `if False` in the inspirations page.
WISDOM = f'''<section class="section section-sand">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Wisdom teachings</p>
      <h2>Words to carry with you</h2>
    </div>
    <div class="split">
{teaching("[A wisdom teaching or inspiring quote.]", "[Place or source]")}
{teaching("[A wisdom teaching or inspiring quote.]", "[Place or source]")}
    </div>
  </div>
</section>'''

# Hidden until Pamela decides what goes on this page (2026-11-19).
ROCKS_AND_REFLECTIONS = f'''<section class="section">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Heart rocks</p>
      <h2>Found in nature</h2>
      <p>Each heart-shaped stone was found, not made. Here are a few, with where they turned up.</p>
    </div>
    <div class="projects">
{rock(("heart-rocks-sandstone.jpg", "Heart-shaped stones gathered beside a sandstone boulder"), "[Where it was found]", "[A line about finding these.]")}
{rock(("coral-heart-rocks-on-lava.jpg", "White coral hearts on black lava rock"), "[Where it was found]", "[A line about finding these.]")}
{rock(("coral-heart-in-hand.jpg", "A heart-shaped piece of coral held in a hand on a sandy beach"), "[Where it was found]", "[A line about finding this one.]")}
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Reflections</p>
      <h2>Notes from the path</h2>
      <p>[Short reflections, meditations, or journal entries. Each can become its own page later.]</p>
    </div>
    <div class="offers">
      <div class="offer"><p class="meta">[Month Year]</p><h3>[Reflection title]</h3><p>[A two-sentence preview.]</p></div>
      <div class="offer"><p class="meta">[Month Year]</p><h3>[Reflection title]</h3><p>[A two-sentence preview.]</p></div>
    </div>
  </div>
</section>
'''

inspirations = f'''<section class="page-hero">
  <div class="wrap stack measure">
    <p class="eyebrow">Inspirations</p>
    <h1>Inspirations for <em>a soul-aligned life</em></h1>
    <p class="lede">Films, quotes, and writing gathered along the way. Take what speaks to you.</p>
  </div>
</section>

{HENDRY}

<section class="section" id="film">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Film</p>
      <h2>Film as <em>a teacher of life</em></h2>
      <p>A great film can show us ourselves in two hours: what we love, what we fear, and what we are capable of. Storytelling is one of the oldest ways the heart has learned, and it is an art worth preserving. These are scenes I return to.</p>
    </div>
{film(*FILMS[0], feature=True)}
{more_films()}
  </div>
</section>

<section class="section section-sand" id="reading">
  <div class="wrap split reading">
    <a class="book-cover-link" href="https://www.amazon.com/dp/1572245379" target="_blank" rel="noopener" aria-label="Buy The Untethered Soul by Michael A. Singer">
      <span class="book-cover" role="img" aria-label="Cover of The Untethered Soul by Michael A. Singer">
        <span class="book-cover-fallback"><em>The Untethered Soul</em><small>Michael A. Singer</small></span>
        <span class="book-cover-img" style="--cover: url('https://covers.openlibrary.org/b/isbn/9781572245372-L.jpg')"></span>
      </span>
    </a>
    <div class="stack">
      <p class="eyebrow">Reading</p>
      <h2>The Untethered Soul</h2>
      <p class="play-by">Michael A. Singer</p>
      <p>A clear, practical guide to the oldest question in the wisdom traditions: who is the one who notices your thoughts? Singer shows how to stop being pulled along by the noise of the mind and rest in the quiet awareness beneath it.</p>
      <div class="actions"><a class="btn" href="https://www.amazon.com/dp/1572245379" target="_blank" rel="noopener">Get the book</a></div>
    </div>
  </div>
</section>

{'' if True else WISDOM}

{'' if True else ROCKS_AND_REFLECTIONS}
{CTA}'''

book_preview = f'''<section class="section book">
  <div class="wrap stack-lg">
    <div class="stack measure"><p class="eyebrow">Book preview</p><h1>The Hearts of Mauna Kea</h1></div>
    <article class="spread" id="p1">
      {img("coral-heart-in-hand.jpg", "The Hearts of Mauna Kea: a heart-shaped piece of coral held on a sandy beach")}
      <div class="stack">
        <p class="lede">On the Kohala Coast of Hawai‘i Island stands the Mauna Kea Beach Hotel, the first of Laurance Rockefeller’s resorts, opened in 1965 on the white crescent of Kauna‘oa Bay and built to honor the land and sea around it.</p>
        <p>I arrived there in a season of my life when everything was shifting. What followed was a quiet run of serendipity: chance meetings, perfect timing, and heart-shaped stones appearing on the shore as if they had been waiting for me.</p>
        <p>This book gathers those moments. It is a record of how a rare place, the right time, and the right people can set the unexpected in motion and awaken the soul.</p>
        <nav class="book-nav" aria-label="Book pages"><span></span><span class="book-count">1 / 7</span><a class="btn btn-small" href="#p2">Next page</a></nav></div>
    </article>
    <article class="spread" id="p2">
      {img("ocean-sparkle.jpg", "Sunlight sparkling across a calm blue sea", "wide")}
      <div class="stack">
        <blockquote class="spread-words">[Sentiment from this page.]</blockquote>
        <dl class="field-note"><dt>Place</dt><dd>[Place]</dd><dt>Heart rock</dt><dd>[Where it arrived]</dd></dl>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p1">Previous</a><span class="book-count">2 / 7</span><a class="btn btn-small" href="#p3">Next page</a></nav>
      </div>
    </article>
    <article class="spread" id="p3">
      {img("golden-water.jpg", "Golden light on ocean waves", "wide")}
      <div class="stack">
        <blockquote class="spread-words">[Sentiment from this page.]</blockquote>
        <dl class="field-note"><dt>Place</dt><dd>[Place]</dd><dt>Heart rock</dt><dd>[Where it arrived]</dd></dl>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p2">Previous</a><span class="book-count">3 / 7</span><a class="btn btn-small" href="#p4">Next page</a></nav>
      </div>
    </article>
    <article class="spread" id="p4">
      {img("silver-ocean.jpg", "Silver light on the ocean at the shore", "wide")}
      <div class="stack">
        <blockquote class="spread-words">[Sentiment from this page.]</blockquote>
        <dl class="field-note"><dt>Place</dt><dd>[Place]</dd><dt>Heart rock</dt><dd>[Where it arrived]</dd></dl>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p3">Previous</a><span class="book-count">4 / 7</span><a class="btn btn-small" href="#p5">Next page</a></nav>
      </div>
    </article>
    <article class="spread" id="p5">
      {img("shoreline-pebbles.jpg", "Stones on wet sand as a wave arrives", "wide")}
      <div class="stack">
        <blockquote class="spread-words">[Sentiment from this page.]</blockquote>
        <dl class="field-note"><dt>Place</dt><dd>[Place]</dd><dt>Heart rock</dt><dd>[Where it arrived]</dd></dl>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p4">Previous</a><span class="book-count">5 / 7</span><a class="btn btn-small" href="#p6">Next page</a></nav>
      </div>
    </article>
    <article class="spread" id="p6">
      {img("hendrys-beach.jpg", "Hendry's Beach at sunset", "wide")}
      <div class="stack">
        <blockquote class="spread-words">[Sentiment from this page.]</blockquote>
        <dl class="field-note"><dt>Place</dt><dd>[Place]</dd><dt>Heart rock</dt><dd>[Where it arrived]</dd></dl>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p5">Previous</a><span class="book-count">6 / 7</span><a class="btn btn-small" href="#p7">Next page</a></nav>
      </div>
    </article>
    <article class="spread" id="p7">
      {img("sea-foam.jpg", "White sea foam on the shore", "wide")}
      <div class="stack">
        <h2>Continue the journey</h2>
        <p>The full book holds every place, sentiment, and heart rock.</p>
        <div class="actions"><a class="btn" href="#request-book">Buy the book</a></div>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p6">Previous</a><span class="book-count">7 / 7</span><a class="btn btn-small" href="books.html">Back to Books</a></nav>
      </div>
    </article>
  </div>
</section>'''

# Hearts of Mauna Kea is sold out: every "Buy the book" button opens this pop-up
# (CSS-only, via :target, no JavaScript). page() adds it to any page that links to #request-book.
# FormSubmit emails each request to EMAIL. The very first submission sends Pamela
# a one-time activation email from FormSubmit that she must confirm.
def request_modal(mid, book, note):
    return f'''<div class="modal" id="{mid}" role="dialog" aria-modal="true" aria-labelledby="{mid}-title">
  <a class="modal-backdrop" href="#_" aria-label="Close"></a>
  <div class="modal-card">
    <a class="modal-close" href="#_" aria-label="Close">&times;</a>
    <p class="eyebrow">{book}</p>
    <h2 id="{mid}-title">Request a copy</h2>
    <p class="modal-note">{note}</p>
    <form class="request-form" action="https://formsubmit.co/{EMAIL}" method="POST">
      <input type="hidden" name="_subject" value="Book request: {book}">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="Book" value="{book}">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="form-row">
        <label>Name<input type="text" name="name" autocomplete="name" required></label>
        <label>Email<input type="email" name="email" autocomplete="email" required></label>
      </div>
      <label class="copies">Copies<input type="number" name="copies" min="1" value="1" inputmode="numeric"></label>
      <label><span>Message <span class="muted">(optional)</span></span><textarea name="message" rows="3"></textarea></label>
      <button class="btn" type="submit">Send request</button>
    </form>
  </div>
</div>'''

REQUEST_MODAL = request_modal("request-book", "The Hearts of Mauna Kea",
    "The first edition has sold out. Leave your details and I will be in touch as soon as more copies are available.")
REQUEST_MODAL_HENDRYS = request_modal("request-hendrys", "Hearts of Hendry's",
    "This book is still being created. Request your copy and I will follow up personally as soon as it is ready.")

pages = [
    ("index.html", "The Power of Heart | Alignment Coaching & Spiritual Teaching",
     "Alignment coaching and spiritual teaching rooted in ancient lineages of yoga, meditation, and Buddhism. Home of The Hearts of Mauna Kea book.", home, ORG),
    ("about.html", "About Pamela | The Power of Heart",
     "Meet Pamela: alignment coach drawing on leadership training, Women's Energetics, 1,000+ hours of yoga certification, and the Meisner Technique.", about, None),
    ("services.html", "Coaching & Spiritual Teaching Services | The Power of Heart",
     "Alignment coaching sessions and a three-month coaching program rooted in ancient lineages. Book a free discovery call.", services, services_schema),
    ("books.html", "The Hearts of… Books | The Power of Heart",
     "The Hearts of Mauna Kea and Hearts of Hendry's pair photographs and sentiments from special places, with heart-shaped rocks that carry a depth of heartfulness and meaning. Order your copy.", books, book_schema),
    ("productions.html", "Productions: Vincent & Meisner in Santa Barbara | The Power of Heart",
     "Two acclaimed one-man plays performed by Jim Jarrett, Vincent by Leonard Nimoy and Meisner, coming to Santa Barbara as benefit engagements.", productions, None),
    ("inspirations.html", "Inspirations: Heart Rocks & Wisdom Teachings | The Power of Heart",
     "Heart rocks found in nature, wisdom teachings, and reflections from Mauna Kea and Hendry's Beach in Santa Barbara.", inspirations, None),
    ("contact.html", "Book a Free Discovery Call | The Power of Heart",
     "Book a free 30-minute discovery call for heart-focused coaching, or get in touch with The Power of Heart.", contact, None),
]

for f in ["request-book.html", "coaching.html", "creative.html", "book-a-call.html", "site.js", "projects.html"]:
    p = os.path.join(OUT, f)
    if os.path.exists(p): os.remove(p)

for slug, t, d, b, s in pages:
    open(os.path.join(OUT, slug), "w").write(page(slug, t, d, b, s))
# Sign-in page for the private book area. server/book_auth.py serves it and fills in
# <!--BOOK_ERROR-->; the form posts to /book-login (handled by that helper, not static).
book_login = f'''<section class="section book-login">
  <div class="wrap">
    <div class="login-card stack">
      <p class="eyebrow">Inside The Hearts of Mauna Kea</p>
      <h1>Turn the pages</h1>
      <p>The book preview is private. Enter your email and the password you were given to step inside.</p>
      <!--BOOK_ERROR-->
      <form class="request-form" method="post" action="/book-login">
        <input type="hidden" name="next" value="/book-preview.html">
        <label>Email<input type="email" name="email" autocomplete="email" required></label>
        <label>Password<input type="password" name="password" autocomplete="current-password" required></label>
        <button class="btn" type="submit">Open the book</button>
      </form>
      <p class="secure-note">Don't have the password? <a href="contact.html">Get in touch</a>.</p>
    </div>
  </div>
</section>'''
bl = page("book-login.html", "Book Preview Sign In | The Power of Heart", "Sign in to preview The Hearts of Mauna Kea.", book_login)
bl = bl.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, nofollow">')
open(os.path.join(OUT, "book-login.html"), "w").write(bl)

# Private book preview: not in the menu, sitemap, or search results.
bp = page("book-preview.html", "Book Preview | The Power of Heart", "A page-by-page preview of The Hearts of Mauna Kea.", book_preview)
bp = bp.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, nofollow">')
open(os.path.join(OUT, "book-preview.html"), "w").write(bp)

urls = "\n".join(f"  <url><loc>{BASE}/{'' if s == 'index.html' else s}</loc><lastmod>2026-10-30</lastmod></url>" for s, *_ in pages)
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /book-preview\nDisallow: /book-login\n\nSitemap: {BASE}/sitemap.xml\n")
print("built")
