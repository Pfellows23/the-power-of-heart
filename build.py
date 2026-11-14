import json, os, html

OUT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.thepowerofheart.com"
NAME = "The Power of Heart"
EMAIL = "pamela@thepowerofheart.com"
BOOKING = "https://calendly.com/pamela-thepowerofheart/30min"

MENU = [("Home", "index.html"), ("About", "about.html"), ("Services", "services.html"),
        ("Projects", "projects.html"), ("Inspirations", "inspirations.html")]
FOOTER_MENU = MENU + [("Contact", "contact.html")]

FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap"

WAVE = '<svg class="wave{cls}" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0,44 C220,78 460,6 720,30 C980,54 1210,12 1440,38 L1440,80 L0,80 Z"/></svg>'
def wave(cls=""): return ""
SHORE = ''
SIZES = {"coral-heart-in-hand.jpg": (1168, 800), "ocean-sparkle.jpg": (980, 1095), "hendrys-beach.jpg": (2000, 743), "golden-water.jpg": (982, 1236), "sea-foam.jpg": (2000, 1278), "coral-heart-rocks-on-lava.jpg": (1446, 1356), "silver-ocean.jpg": (1452, 1362), "heart-rocks-sandstone.jpg": (1340, 1362), "shoreline-pebbles.jpg": (1452, 1360), "pamela-sunset-beach.jpg": (720, 900), "hearts-of-hendrys-cover.jpg": (1016, 762)}

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

def stripe(key): return f"https://buy.stripe.com/REPLACE_{key}"

def header(slug):
    items = "\n".join(
        f'      <li><a href="{href}"{" aria-current=\"page\"" if href == slug else ""}>{label}</a></li>'
        for label, href in MENU)
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
      <p class="footer-tag">Heart-focused coaching, spiritual teaching, creative projects, and The Hearts of… book series.</p>
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
<link rel="stylesheet" href="styles.css">{ld}
</head>
<body>
{header(slug)}
<main>
{body}
</main>
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
      <h1>Live from the <em>wisdom of your heart</em></h1>
      <p class="lede">Heart-focused coaching for inner alignment, empowering you in every area of life and along your path of purpose.</p>
      <div class="actions">
        <a class="btn" href="{BOOKING}" target="_blank" rel="noopener">Book a discovery call</a>
        <a class="btn btn-ghost" href="services.html">Explore services</a>
      </div>
    </div>
    <a class="hero-cover" href="projects.html" aria-label="The Hearts of Mauna Kea book">
      {img("coral-heart-in-hand.jpg", "The Hearts of Mauna Kea: a heart-shaped piece of coral held on a sandy beach")}
    </a>
  </div>
</section>

<section class="section heartfulness" id="heartfulness">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Why the heart</p>
      <h2>From mindfulness to <em>heartfulness</em></h2>
      <p class="lede">Mindfulness taught us to watch the mind and find stillness. Heartfulness is the next step: living from the place in us that already knows.</p>
      <p>The heart is more than a feeling. It is a center of intelligence, where love, intuition, courage, and truth meet. The mind can analyze a life, but only the heart can tell you whether it is yours. When we lead from the heart, decisions become clearer, relationships become more honest, and purpose stops being something to chase and becomes something to live.</p>
      <p>This has never been more important. In a world that is louder, faster, and more divided than ever, a quiet mind is no longer enough. What we need now is the coherence, compassion, and connection that the heart brings, in ourselves first and then in everything we touch.</p>
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
        {img("silver-ocean.jpg", "Sunlight sparkling on the ocean near the shore")}
        <h3>Heart-Focused Coaching</h3>
        <p>One-to-one sessions for inner alignment, so the choices you make each day match what your heart already knows.</p>
        <a class="more" href="services.html#coaching">Coaching services</a>
      </article>
      <article class="path">
        {img("golden-water.jpg", "Golden evening light on gentle ocean waves")}
        <h3>Spiritual Teaching</h3>
        <p>Teachings, gatherings, and practices that help you reconnect with your purpose and the wisdom within.</p>
        <a class="more" href="services.html#teaching">Teaching offerings</a>
      </article>
      <article class="path">
        {img("heart-rocks-sandstone.jpg", "Heart-shaped stones gathered beside a sandstone boulder on the beach")}
        <h3>Projects &amp; Books</h3>
        <p>The Hearts of Mauna Kea pairs photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning.</p>
        <a class="more" href="projects.html">See projects</a>
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
        <a class="btn" href="{stripe("BOOK_HEARTS_OF_MAUNA_KEA")}">Buy the book</a>
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
      <p>Everything I offer was first given to me. My coaching draws on years of study with lineage holders across acting, leadership, transformation, yoga, meditation, and Buddhism. Each tradition opened a different doorway into the same truth, and together they shape how I listen, how I guide, and how I walk beside the people I work with.</p>
      <p>I have been a student of teachers who carry living lineages, each one handed down from teacher to student over generations. This is the ground my coaching stands on.</p>
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
      <h2>Many traditions, one heart</h2>
    </div>
    <div class="offers">
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
    <div class="paths">
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

def product(title, meta, price, text, key, label="Buy now", photo=None):
    ph = ""
    return f'''      <article class="product">
        {ph}<h3>{title}</h3>
        <p class="meta">{meta}</p>
        <p class="price">{price}</p>
        <p>{text}</p>
        <a class="btn" href="{stripe(key)}">{label}</a>
      </article>'''

REEL_FRAMES = [("ocean-sparkle.jpg", "Sunlight sparkling on the ocean"), ("coral-heart-in-hand.jpg", "A heart-shaped piece of coral held in a hand"), ("golden-water.jpg", "Golden evening light on gentle waves"), ("sea-foam.jpg", "White sea foam on the sand"), ("heart-rocks-sandstone.jpg", "Heart-shaped stones beside a sandstone boulder"), ("silver-ocean.jpg", "Silver light on the open ocean"), ("shoreline-pebbles.jpg", "Pebbles along the shoreline")]
def _frames():
    return "".join(f'<img src="images/{n}" alt="{a}" width="800" height="600" style="--i:{i}" decoding="async">' for i, (n, a) in enumerate(REEL_FRAMES))
REEL = f'''<figure class="screen-wrap">
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
{product("Discovery Call", "30 minutes · Zoom or phone", "Free", "A first conversation to see if we are a good fit.", "", "Book a time").replace(stripe(""), BOOKING)}
{product("Single Coaching Session", "[Length]", "[$ Price]", "[Description from your current site.]", "SINGLE_SESSION", "Book &amp; pay")}
{product("Coaching Package", "[Number of sessions]", "[$ Price]", "[Description from your current site.]", "COACHING_PACKAGE", "Book &amp; pay")}
    </div>
  </div>
</section>

{wave()}
<section class="section section-sand" id="teaching">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <h2>Spiritual teaching</h2>
      <p>[Teaching copy from your current Products &amp; Programs page: classes, circles, workshops, or retreats.]</p>
    </div>
    <div class="products">
{product("[Program or workshop name]", "[Dates · Location or online]", "[$ Price]", "[Description from your current site.]", "PROGRAM_1", "Register &amp; pay")}
{product("[Program or workshop name]", "[Dates · Location or online]", "[$ Price]", "[Description from your current site.]", "PROGRAM_2", "Register &amp; pay")}
    </div>
    <p class="secure-note">Payments are processed securely by Stripe. You will get a receipt by email.</p>
  </div>
</section>
{CTA}'''

services_schema = {"@context": "https://schema.org", "@type": "Service", "name": "Heart-focused coaching and spiritual teaching",
                   "provider": {"@type": "ProfessionalService", "name": NAME, "url": BASE + "/"},
                   "serviceType": "Life coaching", "areaServed": "Worldwide",
                   "description": "Inner alignment coaching for individual clients, connecting them with peace, fulfillment, joy, clarity, and abundance."}

projects = f'''<section class="page-hero">
  <div class="wrap stack measure">
    <p class="eyebrow">Projects</p>
    <h1>The Hearts of Mauna Kea</h1>
    <p class="lede">This book pairs photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split">
    {img("coral-heart-in-hand.jpg", "The Hearts of Mauna Kea: a heart-shaped piece of coral held on a sandy beach")}
    <div class="stack">
      <p class="eyebrow">Book one of The Hearts of… series</p>
      <h2>About the book</h2>
      <p>[Book description from your current site.]</p>
      <dl class="field-note">
        <dt>Format</dt><dd>[Hardcover · pages]</dd>
        <dt>Price</dt><dd>[$ Price] plus shipping</dd>
        <dt>Place</dt><dd>Mauna Kea, Hawai‘i Island, 13,803 ft</dd>
      </dl>
      <div class="actions">
        <a class="btn" href="{stripe("BOOK_HEARTS_OF_MAUNA_KEA")}">Buy the book</a>
      </div>
      <p class="secure-note">Payments are processed securely by Stripe.</p>
    </div>
  </div>
</section>

{MKB}
<section class="section section-sand">
  <div class="wrap cta">
    <div>
      <p class="eyebrow">Inside the book</p>
      <h2>Turn the pages</h2>
      <p>Step through the book one spread at a time. The preview is password protected.</p>
    </div>
    <a class="btn btn-ghost" href="book-preview.html">Look inside the book</a>
  </div>
</section>
{wave("wave-flip")}

<section class="section" id="hearts-of-hendrys">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Projects</p>
      <h2 class="h1-size">Hearts of Hendry's</h2>
      <p class="lede">Listening from the Beach. [A sentence or two introducing the book.]</p>
    </div>
    <div class="split">
      {img("hearts-of-hendrys-cover.jpg", "Hearts of Hendry's, Listening from the Beach: book cover showing a heart-shaped stone held up against a sunset over the ocean", "book-cover")}
      <div class="stack">
        <p class="eyebrow">Book two of The Hearts of… series</p>
        <h3 class="h2-size">About the book</h3>
        <p>[Book description.]</p>
        <dl class="field-note">
          <dt>Format</dt><dd>[Hardcover · pages]</dd>
          <dt>Price</dt><dd>[$ Price] plus shipping</dd>
          <dt>Place</dt><dd>Hendry's Beach, Santa Barbara, California</dd>
        </dl>
        <div class="actions">
          <a class="btn" href="{stripe("BOOK_HEARTS_OF_HENDRYS")}">Buy the book</a>
        </div>
        <p class="secure-note">Payments are processed securely by Stripe.</p>
      </div>
    </div>
  </div>
</section>
{HENDRY}

<section class="section">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Artistic projects</p>
      <h2>More creative work</h2>
      <p>[Other projects you produce or create: films, photography, prints, events.]</p>
    </div>
    <div class="products">
{product("[Print or product name]", "[Size or format]", "[$ Price]", "[Description from your current site.]", "PRODUCT_1", "Buy now", "sand")}
{product("[Print or product name]", "[Size or format]", "[$ Price]", "[Description from your current site.]", "PRODUCT_2", "Buy now", "")}
{product("[Project name]", "[Type · Year]", "Coming soon", "[One or two sentences about the project.]", "PRODUCT_3", "Learn more", "basalt")}
    </div>
  </div>
</section>
{CTA}'''

book_schema = {"@context": "https://schema.org", "@type": "Book", "name": "The Hearts of Mauna Kea",
               "author": {"@type": "Person", "name": "Pamela"}, "url": BASE + "/projects.html",
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
    ("Roberto Benigni on the Ten Commandments", "[A line or two on why this clip moves you.]", "https://youtu.be/EatwzkvOWf4"),
    ("[Film title and scene]", "[A line or two on what this scene teaches.]", ""),
]
def film(title, note, url):
    import re
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})", url or "")
    if m:
        frame = f'<iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" title="{title}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
    else:
        frame = '<p class="film-soon">Clip coming soon</p>'
    return f'''      <article class="film">
        <div class="film-frame">{frame}</div>
        <h3>{title}</h3>
        <p>{note}</p>
      </article>'''

def teaching(text, place):
    return f'''      <div class="teaching">
        <blockquote>{text}</blockquote>
        <p class="meta muted" style="font-size:.8rem;letter-spacing:.14em;text-transform:uppercase">{place}</p>
      </div>'''

inspirations = f'''<section class="page-hero">
  <div class="wrap stack measure">
    <p class="eyebrow">Inspirations</p>
    <h1>Inspirations for <em>a soul-aligned life</em></h1>
    <p class="lede">Heart rocks, wisdom teachings, film, and reflections gathered along the way. Take what speaks to your heart.</p>
  </div>
</section>

{HENDRY}

<section class="section">
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
      <p class="eyebrow">Wisdom teachings</p>
      <h2>Words to carry with you</h2>
    </div>
    <div class="split">
{teaching("[A wisdom teaching or inspiring quote.]", "[Place or source]")}
{teaching("[A wisdom teaching or inspiring quote.]", "[Place or source]")}
    </div>
  </div>
</section>

<section class="section" id="film">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Film</p>
      <h2>Film as <em>a teacher of life</em></h2>
      <p>A great film can show us ourselves in two hours: what we love, what we fear, and what we are capable of. Storytelling is one of the oldest ways the heart has learned, and it is an art worth preserving. These are scenes I return to.</p>
    </div>
    <div class="films">
{chr(10).join(film(*f) for f in FILMS)}
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap stack-lg">
    <div class="stack measure">
      <p class="eyebrow">Reflections</p>
      <h2>Notes from the heart</h2>
      <p>[Short reflections, meditations, or journal entries. Each can become its own page later.]</p>
    </div>
    <div class="offers">
      <div class="offer"><p class="meta">[Month Year]</p><h3>[Reflection title]</h3><p>[A two-sentence preview.]</p></div>
      <div class="offer"><p class="meta">[Month Year]</p><h3>[Reflection title]</h3><p>[A two-sentence preview.]</p></div>
    </div>
  </div>
</section>
{CTA}'''

book_preview = f'''<section class="section book">
  <div class="wrap stack-lg">
    <div class="stack measure"><p class="eyebrow">Book preview</p><h1>The Hearts of Mauna Kea</h1></div>
    <article class="spread" id="p1">
      {img("coral-heart-in-hand.jpg", "The Hearts of Mauna Kea: a heart-shaped piece of coral held on a sandy beach")}
      <div class="stack"><p class="lede">Photographs and sentiments from a special place and time, where the heart-shaped rocks that arrived carried a depth of heartfulness and meaning.</p><nav class="book-nav" aria-label="Book pages"><span></span><span class="book-count">1 / 7</span><a class="btn btn-small" href="#p2">Next page</a></nav></div>
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
        <div class="actions"><a class="btn" href="{stripe("BOOK_HEARTS_OF_MAUNA_KEA")}">Buy the book</a></div>
        <nav class="book-nav" aria-label="Book pages"><a class="btn btn-ghost btn-small" href="#p6">Previous</a><span class="book-count">7 / 7</span><a class="btn btn-small" href="projects.html">Back to Projects</a></nav>
      </div>
    </article>
  </div>
</section>'''

pages = [
    ("index.html", "The Power of Heart | Heart-Focused Coaching & Spiritual Teaching",
     "Heart-focused alignment coaching and spiritual teaching for peace, fulfillment, joy, clarity, and abundance. Home of The Hearts of Mauna Kea book.", home, ORG),
    ("about.html", "About Pamela | The Power of Heart",
     "Meet Pamela: heart-focused coach drawing on leadership training, Women's Energetics, 1,000+ hours of yoga certification, and the Meisner Technique.", about, None),
    ("services.html", "Coaching & Spiritual Teaching Services | The Power of Heart",
     "Inner alignment coaching sessions, packages, and spiritual teaching programs. Book a free discovery call or pay securely online.", services, services_schema),
    ("projects.html", "The Hearts of Mauna Kea Book & Creative Projects | The Power of Heart",
     "The Hearts of Mauna Kea pairs photographs and sentiments from a special place and time, with heart-shaped rocks that carry a depth of heartfulness and meaning. Order your copy.", projects, book_schema),
    ("inspirations.html", "Inspirations: Heart Rocks & Wisdom Teachings | The Power of Heart",
     "Heart rocks found in nature, wisdom teachings, and reflections from Mauna Kea and Hendry's Beach in Santa Barbara.", inspirations, None),
    ("contact.html", "Book a Free Discovery Call | The Power of Heart",
     "Book a free 30-minute discovery call for heart-focused coaching, or get in touch with The Power of Heart.", contact, None),
]

for f in ["coaching.html", "creative.html", "books.html", "book-a-call.html", "site.js"]:
    p = os.path.join(OUT, f)
    if os.path.exists(p): os.remove(p)

for slug, t, d, b, s in pages:
    open(os.path.join(OUT, slug), "w").write(page(slug, t, d, b, s))
# Private book preview: not in the menu, sitemap, or search results.
bp = page("book-preview.html", "Book Preview | The Power of Heart", "A page-by-page preview of The Hearts of Mauna Kea.", book_preview)
bp = bp.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, nofollow">')
open(os.path.join(OUT, "book-preview.html"), "w").write(bp)

urls = "\n".join(f"  <url><loc>{BASE}/{'' if s == 'index.html' else s}</loc><lastmod>2026-10-30</lastmod></url>" for s, *_ in pages)
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /book-preview.html\n\nSitemap: {BASE}/sitemap.xml\n")
print("built")
