# AI Sales Assistant (Public Widget)

FastAPI backend (`app.py`) serving a public embeddable AI Sales Assistant widget (`/widget.js`).

## Stripe Checkout (Starter / Pro)

Plans:
- Starter — $39/month (`STRIPE_PRICE_STARTER`)
- Pro — $99/month (`STRIPE_PRICE_PRO`)
- Custom / Enterprise — contact sales (no Stripe checkout)

### Required Environment Variables (Render)

- `STRIPE_SECRET_KEY` (must start with `sk_test_` or `sk_live_`)
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_STARTER` (must start with `price_`)
- `STRIPE_PRICE_PRO` (must start with `price_`)
- `APP_PUBLIC_URL` (must start with `https://`, example: `https://repository-name-ai-sales-public.onrender.com`)

### Webhook Setup (Stripe)

Add a webhook endpoint pointing to:

`https://<your-render-domain>/api/stripe/webhook`

Subscribe at least to:
- `checkout.session.completed`

Notes:
- The app does not trust the frontend success URL for access. It marks payments as paid only via Stripe webhooks.
- Payment records are stored in PostgreSQL table `v2_payments`.

### Test Payment

1. Use Stripe test mode keys and prices.
2. Open a page with the widget embedded (or open the demo site) and click **Pay Starter** or **Pay Pro**.
3. Complete Checkout.
4. Confirm webhook events are received in Stripe and the payment is recorded in DB.

