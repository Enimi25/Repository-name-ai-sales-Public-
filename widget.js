<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Sales Assistant — AI продавец для сайта</title>
  <meta name="description" content="AI Sales Assistant отвечает посетителям сайта, собирает лиды, записывает клиентов и помогает закрывать оплаты автоматически." />

  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: Arial, sans-serif;
      background: #050507;
      color: #ffffff;
      line-height: 1.6;
      overflow-x: hidden;
    }

    body::before {
      content: "";
      position: fixed;
      inset: -20%;
      background:
        radial-gradient(circle at 20% 20%, rgba(124, 58, 237, 0.38), transparent 32%),
        radial-gradient(circle at 80% 10%, rgba(99, 102, 241, 0.22), transparent 28%),
        radial-gradient(circle at 70% 80%, rgba(168, 85, 247, 0.18), transparent 32%);
      filter: blur(60px);
      z-index: -2;
    }

    body::after {
      content: "";
      position: fixed;
      inset: 0;
      background:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
      background-size: 64px 64px;
      mask-image: linear-gradient(to bottom, black, transparent 75%);
      z-index: -1;
      pointer-events: none;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    .container {
      width: min(1180px, 92%);
      margin: 0 auto;
    }

    header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: rgba(5,5,7,0.78);
      backdrop-filter: blur(18px);
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .nav {
      min-height: 86px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 900;
      letter-spacing: -0.5px;
      font-size: 22px;
    }

    .brand-icon {
      width: 38px;
      height: 38px;
      border-radius: 12px;
      display: grid;
      place-items: center;
      background: linear-gradient(135deg, #8b5cf6, #4f46e5);
      box-shadow: 0 0 35px rgba(139,92,246,.55);
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 28px;
      color: #b9b9c8;
      font-size: 15px;
    }

    .nav-links a:hover {
      color: white;
    }

    .nav-actions {
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      border-radius: 14px;
      padding: 14px 22px;
      font-weight: 800;
      cursor: pointer;
      transition: 0.2s ease;
      border: 1px solid transparent;
      white-space: nowrap;
    }

    .btn-primary {
      background: linear-gradient(135deg, #a855f7, #5b5ff7);
      color: white;
      box-shadow: 0 18px 50px rgba(124,58,237,.35);
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 24px 70px rgba(124,58,237,.48);
    }

    .btn-secondary {
      background: rgba(255,255,255,0.06);
      color: white;
      border-color: rgba(255,255,255,0.12);
    }

    .btn-secondary:hover {
      background: rgba(255,255,255,0.1);
      transform: translateY(-2px);
    }

    .btn-light {
      background: white;
      color: #050507;
    }

    .hero {
      padding: 94px 0 70px;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 56px;
      align-items: center;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 13px;
      border-radius: 999px;
      background: rgba(124,58,237,0.12);
      color: #d8c7ff;
      border: 1px solid rgba(168,85,247,0.32);
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 24px;
    }

    h1 {
      font-size: clamp(52px, 7vw, 88px);
      line-height: 0.94;
      letter-spacing: -4px;
      margin-bottom: 28px;
    }

    .gradient-text {
      background: linear-gradient(90deg, #ffffff, #a855f7 52%, #6366f1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      color: #c4c4d2;
      font-size: 21px;
      max-width: 650px;
      margin-bottom: 34px;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 34px;
    }

    .proof-row {
      display: grid;
      grid-template-columns: repeat(4, auto);
      gap: 16px;
      color: #a7a7b8;
      font-size: 14px;
    }

    .proof-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .check {
      width: 20px;
      height: 20px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      background: rgba(124,255,189,0.14);
      color: #7cffbd;
      font-size: 12px;
      border: 1px solid rgba(124,255,189,0.22);
    }

    .dashboard {
      position: relative;
      padding: 26px;
      border-radius: 32px;
      background:
        radial-gradient(circle at 70% 15%, rgba(168,85,247,.25), transparent 38%),
        linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,.035));
      border: 1px solid rgba(255,255,255,.12);
      box-shadow:
        0 40px 120px rgba(0,0,0,.55),
        0 0 100px rgba(124,58,237,.18);
      overflow: hidden;
    }

    .dashboard::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(120deg, transparent, rgba(255,255,255,.08), transparent);
      transform: translateX(-100%);
      animation: shine 6s infinite;
      pointer-events: none;
    }

    @keyframes shine {
      0% { transform: translateX(-120%); }
      45%, 100% { transform: translateX(120%); }
    }

    .dashboard-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 22px;
      position: relative;
      z-index: 1;
    }

    .dashboard-top h3 {
      font-size: 23px;
      letter-spacing: -0.6px;
    }

    .select-pill {
      color: #b9b9c8;
      font-size: 13px;
      padding: 8px 11px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,.12);
      background: rgba(0,0,0,.25);
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
      margin-bottom: 22px;
      position: relative;
      z-index: 1;
    }

    .stat {
      background: rgba(0,0,0,.25);
      border: 1px solid rgba(255,255,255,.08);
      border-radius: 20px;
      padding: 18px;
    }

    .stat span {
      color: #a8a8b8;
      font-size: 13px;
      display: block;
      margin-bottom: 8px;
    }

    .stat strong {
      font-size: 27px;
      letter-spacing: -1px;
    }

    .up {
      color: #7cffbd;
      font-size: 13px;
      margin-left: 6px;
    }

    .chart-card {
      height: 245px;
      border-radius: 22px;
      background:
        linear-gradient(to bottom, rgba(255,255,255,.04), rgba(255,255,255,.015)),
        repeating-linear-gradient(to bottom, transparent, transparent 47px, rgba(255,255,255,.055) 48px);
      border: 1px solid rgba(255,255,255,.08);
      padding: 16px;
      position: relative;
      overflow: hidden;
      z-index: 1;
    }

    .chart-card svg {
      width: 100%;
      height: 100%;
    }

    .logos {
      padding: 34px 0 20px;
      border-top: 1px solid rgba(255,255,255,.06);
      border-bottom: 1px solid rgba(255,255,255,.06);
    }

    .logos-title {
      text-align: center;
      color: #77778a;
      font-size: 12px;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 24px;
    }

    .logos-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 18px;
      color: #8d8da0;
      text-align: center;
      font-weight: 800;
      opacity: .8;
    }

    section {
      padding: 88px 0;
    }

    .section-head {
      max-width: 780px;
      margin-bottom: 42px;
    }

    .section-kicker {
      color: #a855f7;
      font-weight: 900;
      margin-bottom: 12px;
      text-transform: uppercase;
      font-size: 13px;
      letter-spacing: 1.5px;
    }

    .section-title {
      font-size: clamp(36px, 5vw, 58px);
      line-height: 1.02;
      letter-spacing: -2.5px;
      margin-bottom: 18px;
    }

    .section-subtitle {
      color: #b9b9c8;
      font-size: 19px;
    }

    .cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }

    .card {
      min-height: 240px;
      background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,.035));
      border: 1px solid rgba(255,255,255,.1);
      border-radius: 28px;
      padding: 28px;
      box-shadow: 0 24px 80px rgba(0,0,0,.25);
    }

    .card-icon {
      width: 46px;
      height: 46px;
      border-radius: 16px;
      display: grid;
      place-items: center;
      background: rgba(124,58,237,.16);
      color: #d8c7ff;
      margin-bottom: 22px;
      box-shadow: inset 0 0 20px rgba(124,58,237,.15);
    }

    .card h3 {
      font-size: 23px;
      margin-bottom: 12px;
      letter-spacing: -0.7px;
    }

    .card p {
      color: #b7b7c8;
      font-size: 16px;
    }

    .steps {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .step {
      background: rgba(255,255,255,.045);
      border: 1px solid rgba(255,255,255,.1);
      border-radius: 26px;
      padding: 24px;
      min-height: 210px;
    }

    .step-num {
      width: 42px;
      height: 42px;
      border-radius: 14px;
      display: grid;
      place-items: center;
      background: white;
      color: #050507;
      font-weight: 900;
      margin-bottom: 18px;
    }

    .step h3 {
      margin-bottom: 10px;
      font-size: 20px;
    }

    .step p {
      color: #b7b7c8;
      font-size: 15px;
    }

    .pricing-section {
      padding-top: 98px;
    }

    .pricing-note {
      max-width: 900px;
      padding: 26px;
      border-radius: 28px;
      background:
        radial-gradient(circle at 80% 10%, rgba(124,58,237,.22), transparent 35%),
        rgba(255,255,255,.055);
      border: 1px solid rgba(255,255,255,.1);
      margin-bottom: 26px;
      color: #d8d8e6;
      font-size: 18px;
    }

    .pricing-note strong {
      color: white;
    }

    .pricing-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-top: 34px;
    }

    .price-card {
      position: relative;
      padding: 30px;
      border-radius: 30px;
      background: linear-gradient(180deg, rgba(255,255,255,.075), rgba(255,255,255,.035));
      border: 1px solid rgba(255,255,255,.11);
      box-shadow: 0 30px 90px rgba(0,0,0,.28);
      overflow: hidden;
    }

    .price-card.featured {
      border-color: rgba(168,85,247,.55);
      box-shadow:
        0 30px 100px rgba(0,0,0,.35),
        0 0 80px rgba(124,58,237,.22);
      transform: translateY(-10px);
    }

    .popular {
      position: absolute;
      top: 18px;
      right: 18px;
      padding: 7px 11px;
      border-radius: 999px;
      background: rgba(124,58,237,.24);
      border: 1px solid rgba(168,85,247,.45);
      color: #e7d8ff;
      font-size: 12px;
      font-weight: 900;
    }

    .price-card h3 {
      font-size: 25px;
      margin-bottom: 8px;
    }

    .price-card .desc {
      color: #aaaabe;
      min-height: 52px;
      margin-bottom: 20px;
    }

    .monthly {
      font-size: 46px;
      font-weight: 900;
      letter-spacing: -2px;
      margin-bottom: 4px;
    }

    .monthly span {
      font-size: 16px;
      color: #aaaabe;
      letter-spacing: 0;
    }

    .success-fee {
      color: #7cffbd;
      font-weight: 900;
      margin-bottom: 22px;
    }

    .price-list {
      display: grid;
      gap: 12px;
      margin: 24px 0 28px;
      color: #d4d4e2;
      font-size: 15px;
    }

    .price-list div {
      display: flex;
      gap: 10px;
      align-items: flex-start;
    }

    .pricing-explainer {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 30px;
    }

    .explainer-box {
      padding: 24px;
      border-radius: 26px;
      background: rgba(255,255,255,.045);
      border: 1px solid rgba(255,255,255,.1);
    }

    .explainer-box h3 {
      font-size: 22px;
      margin-bottom: 10px;
    }

    .explainer-box p {
      color: #b9b9c8;
    }

    .final-cta {
      position: relative;
      overflow: hidden;
      border-radius: 34px;
      padding: 46px;
      background:
        radial-gradient(circle at 80% 20%, rgba(124,58,237,.26), transparent 35%),
        linear-gradient(135deg, #ffffff, #e9ddff);
      color: #09090d;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 30px;
      align-items: center;
    }

    .final-cta h2 {
      font-size: clamp(34px, 4.5vw, 54px);
      line-height: 1;
      letter-spacing: -2px;
      margin-bottom: 14px;
    }

    .final-cta p {
      color: #33333d;
      font-size: 18px;
      max-width: 660px;
    }

    .final-cta-box {
      text-align: right;
    }

    .final-price {
      font-size: 52px;
      font-weight: 900;
      letter-spacing: -3px;
      margin-bottom: 14px;
    }

    footer {
      padding: 42px 0;
      color: #79798c;
      border-top: 1px solid rgba(255,255,255,.08);
    }

    @media (max-width: 920px) {
      .hero-grid,
      .final-cta,
      .pricing-explainer {
        grid-template-columns: 1fr;
      }

      .final-cta-box {
        text-align: left;
      }

      .cards,
      .steps,
      .logos-row,
      .stats-grid,
      .pricing-grid {
        grid-template-columns: 1fr;
      }

      .price-card.featured {
        transform: none;
      }

      h1 {
        letter-spacing: -2px;
      }

      .nav-links {
        display: none;
      }

      .hero {
        padding-top: 62px;
      }

      .proof-row {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>

<body>
  <header>
    <div class="container nav">
      <a class="brand" href="#">
        <span class="brand-icon">🤖</span>
        <span>AI Sales Assistant</span>
      </a>

      <nav class="nav-links">
        <a href="#features">Features</a>
        <a href="#how">How it works</a>
        <a href="#pricing">Pricing</a>
      </nav>

      <div class="nav-actions">
        <a class="btn btn-secondary" href="#demo">Demo</a>
        <a class="btn btn-primary" href="#pricing">Get Started</a>
      </div>
    </div>
  </header>

  <main>
    <section class="hero" id="demo">
      <div class="container hero-grid">
        <div>
          <div class="badge">⚡ AI-powered sales automation</div>

          <h1>
            Close More Deals
            <span class="gradient-text">with AI</span>
          </h1>

          <p class="hero-subtitle">
            A smart website assistant that qualifies visitors, answers questions,
            collects leads, books appointments, and helps customers pay faster.
          </p>

          <div class="hero-actions">
            <a class="btn btn-primary" href="#pricing">Get Started Free →</a>
            <a class="btn btn-secondary" href="#how">Watch Demo</a>
          </div>

          <div class="proof-row">
            <div class="proof-item"><span class="check">✓</span> 24/7 available</div>
            <div class="proof-item"><span class="check">✓</span> Lead capture</div>
            <div class="proof-item"><span class="check">✓</span> Payment ready</div>
            <div class="proof-item"><span class="check">✓</span> Easy install</div>
          </div>
        </div>

        <div class="dashboard">
          <div class="dashboard-top">
            <h3>Live Overview</h3>
            <div class="select-pill">This Week</div>
          </div>

          <div class="stats-grid">
            <div class="stat">
              <span>Total Leads</span>
              <strong>247 <small class="up">↑ 23%</small></strong>
            </div>
            <div class="stat">
              <span>Deals Closed</span>
              <strong>39 <small class="up">↑ 18%</small></strong>
            </div>
            <div class="stat">
              <span>Revenue</span>
              <strong>$12,450 <small class="up">↑ 32%</small></strong>
            </div>
            <div class="stat">
              <span>Conversion</span>
              <strong>15.8% <small class="up">↑ 12%</small></strong>
            </div>
          </div>

          <div class="chart-card">
            <svg viewBox="0 0 520 240" preserveAspectRatio="none">
              <defs>
                <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#8b5cf6" stop-opacity=".55"/>
                  <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
                </linearGradient>
                <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#7c3aed"/>
                  <stop offset="100%" stop-color="#a855f7"/>
                </linearGradient>
              </defs>

              <path d="M20 190 L90 145 L160 112 L230 92 L300 62 L365 126 L440 85 L505 42 L505 240 L20 240 Z" fill="url(#area)"/>
              <polyline points="20,190 90,145 160,112 230,92 300,62 365,126 440,85 505,42"
                fill="none" stroke="url(#line)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

              <g fill="#a855f7">
                <circle cx="20" cy="190" r="5"/>
                <circle cx="90" cy="145" r="5"/>
                <circle cx="160" cy="112" r="5"/>
                <circle cx="230" cy="92" r="5"/>
                <circle cx="300" cy="62" r="5"/>
                <circle cx="365" cy="126" r="5"/>
                <circle cx="440" cy="85" r="5"/>
                <circle cx="505" cy="42" r="5"/>
              </g>
            </svg>
          </div>
        </div>
      </div>
    </section>

    <div class="logos">
      <div class="container">
        <div class="logos-title">Trusted by growing businesses</div>
        <div class="logos-row">
          <div>AlphaLab</div>
          <div>CloudFlow</div>
          <div>NextGen</div>
          <div>Visionary</div>
          <div>TechNova</div>
        </div>
      </div>
    </div>

    <section id="features">
      <div class="container">
        <div class="section-head">
          <div class="section-kicker">Features</div>
          <h2 class="section-title">Everything your website needs to convert visitors</h2>
          <p class="section-subtitle">
            Not just a chat bubble. A sales assistant that guides people toward price,
            appointment, payment, and lead capture.
          </p>
        </div>

        <div class="cards">
          <div class="card">
            <div class="card-icon">💬</div>
            <h3>AI Lead Capture</h3>
            <p>Engages visitors instantly and collects qualified leads while they are hot.</p>
          </div>

          <div class="card">
            <div class="card-icon">🎯</div>
            <h3>Smart Qualification</h3>
            <p>Asks the right questions and helps the customer choose the next step.</p>
          </div>

          <div class="card">
            <div class="card-icon">💳</div>
            <h3>Payment Links</h3>
            <p>Sends a secure payment link when the customer is ready to buy.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="how">
      <div class="container">
        <div class="section-head">
          <div class="section-kicker">How it works</div>
          <h2 class="section-title">Install once. Let the assistant sell 24/7.</h2>
          <p class="section-subtitle">
            Add one script to your website and the assistant appears as a small chat bubble.
          </p>
        </div>

        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <h3>Visitor asks</h3>
            <p>They ask about price, booking, product, or payment.</p>
          </div>

          <div class="step">
            <div class="step-num">2</div>
            <h3>AI answers</h3>
            <p>The assistant responds instantly and keeps the conversation moving.</p>
          </div>

          <div class="step">
            <div class="step-num">3</div>
            <h3>Lead is captured</h3>
            <p>Email, phone, and intent are saved for the business owner.</p>
          </div>

          <div class="step">
            <div class="step-num">4</div>
            <h3>Deal closes</h3>
            <p>The customer books an appointment or receives a payment link.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="pricing" class="pricing-section">
      <div class="container">
        <div class="section-head">
          <div class="section-kicker">Hybrid pricing model</div>
          <h2 class="section-title">Pay a simple monthly fee, then share only when AI brings real revenue</h2>
          <p class="section-subtitle">
            Our model is built around results. You get the stability of a SaaS subscription,
            plus a small success fee only from deals closed by the assistant.
          </p>
        </div>

        <div class="pricing-note">
          <strong>Why hybrid?</strong> A flat subscription keeps the assistant running 24/7.
          The success fee keeps us aligned with your business: we earn more only when the AI helps you earn more.
        </div>

        <div class="pricing-grid">
          <div class="price-card">
            <h3>Starter</h3>
            <p class="desc">For small businesses that want to start collecting leads and bookings.</p>

            <div class="monthly">$39 <span>/ month</span></div>
            <div class="success-fee">+ 10% success fee</div>

            <div class="price-list">
              <div><span class="check">✓</span> Website AI chat widget</div>
              <div><span class="check">✓</span> Price, booking, payment answers</div>
              <div><span class="check">✓</span> Lead capture</div>
              <div><span class="check">✓</span> Multilingual AI assistant</div>
            </div>

            <a class="btn btn-secondary" href="#demo">Start Starter</a>
          </div>

          <div class="price-card featured">
            <div class="popular">Most popular</div>

            <h3>Pro</h3>
            <p class="desc">For growing businesses that want AI to close more appointments and payments.</p>

            <div class="monthly">$99 <span>/ month</span></div>
            <div class="success-fee">+ 5% success fee</div>

            <div class="price-list">
              <div><span class="check">✓</span> Everything in Starter</div>
              <div><span class="check">✓</span> Stronger sales prompts</div>
              <div><span class="check">✓</span> Google Sheets leads</div>
              <div><span class="check">✓</span> Stripe payment link support</div>
              <div><span class="check">✓</span> Priority setup help</div>
            </div>

            <a class="btn btn-primary" href="#demo">Start Pro →</a>
          </div>

          <div class="price-card">
            <h3>Business</h3>
            <p class="desc">For teams that want calendar booking, CRM flow, and custom automation.</p>

            <div class="monthly">$299 <span>/ month</span></div>
            <div class="success-fee">+ 3% success fee</div>

            <div class="price-list">
              <div><span class="check">✓</span> Everything in Pro</div>
              <div><span class="check">✓</span> Google Calendar booking</div>
              <div><span class="check">✓</span> Multi-company setup</div>
              <div><span class="check">✓</span> Custom sales script</div>
              <div><span class="check">✓</span> Advanced integrations</div>
            </div>

            <a class="btn btn-secondary" href="#demo">Talk to Sales</a>
          </div>
        </div>

        <div class="pricing-explainer">
          <div class="explainer-box">
            <h3>What is a success fee?</h3>
            <p>
              A small percentage only from payments, bookings, or deals that were generated through the AI assistant.
              If the assistant does not help close the deal, there is no success fee.
            </p>
          </div>

          <div class="explainer-box">
            <h3>Why clients like this model</h3>
            <p>
              Businesses do not pay huge upfront costs. They get a working AI salesperson quickly,
              and the pricing grows only when the assistant creates value.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="final-cta">
          <div>
            <h2>Start with AI sales today</h2>
            <p>
              Launch your assistant, capture more leads, book more appointments,
              and only share upside when the AI helps close real business.
            </p>
          </div>

          <div class="final-cta-box">
            <div class="final-price">$99/mo</div>
            <a class="btn btn-light" href="https://buy.stripe.com/test_your_payment_link">Start Now</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      © 2026 AI Sales Assistant. Built to turn visitors into customers.
    </div>
  </footer>

  <script src="/widget.js"></script>
</body>
</html>
