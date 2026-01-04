# GranblueParty: Monetization & Revenue Analysis

## Summary

**YES** - This codebase includes ad services and revenue generation mechanisms.

---

## Revenue Streams Identified

### 1. **Google AdSense** ✓ Active

- **Type:** Display advertising network
- **Location:** `Frontend/src/ads.txt`
- **Publisher ID:** `pub-2769716391947040`
- **Implementation:** Loaded in `Frontend/src/index.template.html`
  ```html
  <script
    async
    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2769716391947040"
    crossorigin="anonymous"
  ></script>
  ```
- **How It Works:** Google automatically displays contextual ads on the website pages. Revenue is generated per impression and per click.
- **Revenue Potential:** Typically $0.25 - $10 per 1000 impressions (CPM), depending on traffic quality and geographic location

### 2. **Quantcast (GDPR/TCF Consent Management)** ✓ Active

- **Type:** Consent management platform + analytics
- **Location:** `Frontend/src/index.template.html` (lines ~43-60)
- **Quantcast ID:** `pyeNsBYmDqcpe`
- **Purpose:** Manages user consent for cookie tracking and GDPR compliance
- **Function:** Integrates with Quantcast's ad network and other third-party trackers
- **Revenue:** Quantcast enables better targeting for advertisers, which increases ad rates

```javascript
// From index.template.html
<script type="text/javascript" async=true>
  (function() {
    var host = 'granblue.party';
    var element = document.createElement('script');
    var firstScript = document.getElementsByTagName('script')[0];
    var url = 'https://cmp.inmobi.com'
      .concat('/choice/', 'pyeNsBYmDqcpe', '/', host, '/choice.js?tag_version=V2');
    // ... initializes consent manager
  })();
</script>
```

### 3. **Privacy Policy & Tracking Disclosures** ✓ Present

- **Location:** `Frontend/src/pages/Privacy.vue`
- **Sections About Tracking:**
  - "6. DO WE USE COOKIES AND OTHER TRACKING TECHNOLOGIES?"
  - "11. CONTROLS FOR DO-NOT-TRACK FEATURES"
- **Content:** Discloses that cookies and tracking technologies may be used for data collection

### 4. **User Accounts & Collection Tracking** ✓ Premium Feature Ready

- **Location:** `Frontend/src/store/modules/collection-tracker.js`
- **API Routes:** `/tracker/charas/:userId`, `/tracker/summons/:userId`
- **Purpose:** Users can create accounts and track their collection progress
- **Monetization Potential:** Could enable:
  - Premium account features (remove ads)
  - Battle pass / season pass cosmetics
  - Subscription for ad-free experience

---

## Monetization Infrastructure

### What's Already In Place

1. **User Authentication System** (`API/src/models/admin.js`, `passport-providers.js`)

   - JWT tokens
   - Password reset capability
   - Account management ready

2. **Collection Tracker Backend** (`API/src/models/tracker.js`)

   - Tracks character and summon collections per user
   - Database support for user data persistence

3. **Cookies & Consent System**
   - Quantcast integration for GDPR compliance
   - Ready for additional trackers (Google Analytics, Facebook Pixel, etc.)

### What Could Be Added for Additional Revenue

1. **Subscription Model**

   ```javascript
   // Could add premium tier to config
   {
     premium: {
       remove_ads: true,
       ad_free_mode: true,
       stats_tracking: true,
      price_monthly: 4.99
    }
   }
   ```

2. **Google Analytics** (for traffic data)

   ```html
   <!-- Currently NOT implemented -->
   <script
     async
     src="https://www.googletagmanager.com/gtag/js?id=GA_ID"
   ></script>
   ```

3. **Stripe/PayPal Integration** (for premium payments)
   ```javascript
   // Routes for payment processing
   // POST /api/payments/checkout
   // Could process premium subscriptions
   ```

---

## Current Ad Configuration

### File: `Frontend/src/ads.txt`

```
google.com, pub-2769716391947040, DIRECT, f08c47fec0942fa0
```

This is a **public file** that tells Google Ad Exchange and other ad networks that this publisher is authorized to sell ads for this domain. It's a requirement for AdSense to work properly.

### Ad Display Locations (Expected)

Google AdSense auto-places ads in:

- Between content sections
- Sidebars
- Footer areas
- Native ad placements

The actual ad placement code (like `<ins class="adsbygoogle">` tags) is likely dynamically injected by the AdSense script or could be added in Vue components.

---

## Privacy & Compliance

### Privacy Policy Status

- ✓ Present and comprehensive (`Frontend/src/pages/Privacy.vue`)
- ✓ Mentions tracking technologies
- ✓ Mentions cookies
- ✓ References GDPR compliance

### GDPR/CCPA Compliance

- ✓ Quantcast consent manager active
- ✓ Cookie consent required before tracking

### How to Verify in Production

Open any page and look for:

1. Cookie consent banner (Quantcast pop-up)
2. AdSense ads displayed on the page
3. Console: Check for Google AdSense script loading

---

## Revenue Estimation (For Reference)

Based on typical GranblueFantasy fan site metrics:

| Metric              | Conservative | Moderate | Optimistic |
| ------------------- | ------------ | -------- | ---------- |
| Monthly Visitors    | 5,000        | 25,000   | 100,000    |
| Monthly Page Views  | 15,000       | 100,000  | 500,000    |
| CPM Rate            | $0.50        | $2.00    | $5.00      |
| **Monthly Revenue** | **$7.50**    | **$200** | **$2,500** |

Note: Actual revenue depends heavily on:

- Traffic source geography (US/EU = higher CPM)
- Content quality and relevance
- User engagement time
- Ad block usage rates
- Ad frequency

---

## What's NOT Implemented

These common monetization methods are **NOT** in the current codebase:

- ❌ Google Analytics tracking
- ❌ Facebook Pixel / Meta tracking
- ❌ Stripe/PayPal payments
- ❌ Subscription management
- ❌ Premium tier system
- ❌ Affiliate links
- ❌ Amazon Associates
- ❌ Blockchain/crypto monetization

---

## For Production Deployment

When deploying to production, you should:

1. **Verify AdSense Account is Active**

   - Log in to Google AdSense
   - Ensure publisher ID `pub-2769716391947040` is approved
   - Check for policy violations

2. **Configure Ad Placements**

   - Add `<ins class="adsbygoogle">` elements in Vue components
   - Wrap with AdSense initialization code
   - Test ad display in different pages

3. **Enable Analytics**
   Consider adding Google Analytics to track:

   ```html
   <script
     async
     src="https://www.googletagmanager.com/gtag/js?id=GA_XXXX"
   ></script>
   ```

4. **Verify Consent Manager**

   - Test Quantcast consent banner appears
   - Ensure it complies with GDPR/CCPA
   - Monitor consent rates

5. **Monitor Revenue**
   - Check AdSense dashboard weekly
   - Monitor CPM trends
   - Check traffic sources

---

## Summary for Your Situation

**Current State:**

- AdSense is configured and ready to serve ads
- Consent management is in place
- Privacy policy covers tracking
- No ads are actively displayed in the current UI (could be added to Vue templates)

**To Activate:**

- Ensure AdSense publisher account is active
- Add AdSense placement codes to Vue components
- Deploy to production
- Ads will serve automatically

**Additional Revenue Opportunities:**

- Premium ad-free subscription ($4.99/month)
- Premium collection tracker features
- Cosmetic/battle pass items
- Affiliate partnerships with GBF retailers

---

**Last Updated:** January 2, 2026  
**Status:** Production-ready monetization infrastructure in place
