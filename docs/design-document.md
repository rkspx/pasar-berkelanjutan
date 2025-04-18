**Design Document: Pasar Berkelanjutan Jakarta**

---

### 🌱 Project Overview

**Pasar Berkelanjutan Jakarta** is a community-driven sustainable marketplace platform connecting local sellers and buyers within Jakarta. The platform is designed to be accessible, clean, and centered around a simple user experience. It empowers small businesses and eco-conscious users with easy navigation, meaningful visuals, and an inclusive design system.

---

### ✨ Design Principles

1. **Clarity First**: Prioritize readability, clear labeling, and natural information flow.
2. **Visual Hierarchy**: Use consistent type scales and spacing to lead user attention.
3. **Minimalism with Warmth**: Clean UI with purposeful use of color and soft visuals.
4. **Consistency**: Repeat familiar visual patterns for user confidence.
5. **Local Relevance**: Use illustrations, language, and tone that resonate with Jakarta communities.

---

### 🎨 Color Palette

- **Primary Green**: `#335633` — For primary buttons, highlights
- **Terracotta**: `#D97D54` — Accent color (badges, alerts)
- **Off-White / Cream**: `#F5F5F5` — Backgrounds and sections

---

### ✏️ Typography

- **Font Family**: Plus Jakarta Sans or Manrope
- **Heading**: Bold, 32–48px
- **Body Text**: Regular, 16–18px
- **Caption**: Regular, 12–14px

---

### 🖊️ Core UI Elements

- **Buttons**:
  - Rounded corners (8px)
  - Primary = filled green, white text
  - Secondary = outline or soft fill
- **Inputs**:
  - Border: 1px subtle gray, rounded
  - Label outside input field
- **Cards**:
  - Borderless or light border/shadow
  - Compact, minimal text blocks
- **Icons**:
  - Feather / Lucide style
  - Light outline, consistent sizing

---

### 🏛️ Key Screens & Layouts

#### 1. Landing Page

- Hero with search bar by *kelurahan*
- Carousel of featured products or markets
- Section: Produk Terbaru (Latest Products)

#### 2. Market Discovery Page

- Split view: Left filter sidebar, right interactive Jakarta map
- Filter by category, delivery method, distance, and payment options
- List of results with cards

#### 3. Product Detail Page

- Image gallery, description, seller badge
- Price, stock, quantity selector
- Delivery & payment options
- Seller widget and related products

#### 4. Cart & Checkout Flow

- Cart Review: List items, quantity control, promo code, order summary
- Checkout:
  - Alamat & Pickup method (Pasar, Kurir Lokal, COD)
  - Payment selection (GoPay, OVO, Bank Transfer)
  - Order recap

#### 5. Authentication Screens

- Sign In: Email + Password, followed by OTP
- Sign Up: Name, Email, Phone, Password + Terms
- Forgot Password: Email/Phone + OTP reset

#### 6. System Feedback Screens

- Empty Cart: "Keranjang Anda Kosong"
- No Results: "Tidak ada pasar ditemukan"
- 404 Page: Local illustration + search + return links
- Order Confirmation:
  - Summary, order number, pickup slot or delivery estimate
  - CTA to view order status or return to homepage

---

### 📊 Interaction Guidelines

- **Animations**: Use Framer Motion for smooth transitions (e.g. cart open, filter toggle)
- **Responsive Behavior**:
  - Cards collapse into list view
  - Filter becomes modal
  - Fixed bottom CTAs on mobile
- **Accessibility**:
  - All buttons have labels
  - Color contrast AA+ compliant
  - Focus rings and screen-reader support

---

### ✉️ Next Steps

- Apply design system to final high-fidelity UI mockups
- Create mobile variants for key screens
- Build a reusable component library (Figma or Storybook)
- Prepare assets for frontend implementation

---

End of document.
