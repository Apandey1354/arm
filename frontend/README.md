# FindMe – Missing Person Search Platform

A compassionate, production-ready Next.js platform to help find missing persons through AI-powered matching and community support.

## Features

- 🏠 **Home Page**: Beautiful landing page with hero section, how it works, and why it matters sections
- 📤 **Upload Page**: Comprehensive form with validation for reporting missing persons
- 💬 **Consultation Page**: Support resources and callback request form
- 🎨 **Modern UI**: Built with TailwindCSS, ShadCN UI, and Framer Motion
- 📱 **Fully Responsive**: Mobile-first design that works on all devices
- 🌙 **Dark Mode**: Full dark mode support
- ✅ **Form Validation**: React Hook Form + Zod validation
- 🖼️ **Image Upload**: Image preview with upload functionality

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **TailwindCSS**
- **ShadCN UI Components**
- **Framer Motion** (Animations)
- **React Hook Form** + **Zod** (Form Validation)
- **Lucide Icons**

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
├── app/
│   ├── layout.tsx          # Root layout with Navbar
│   ├── page.tsx            # Home page
│   ├── upload/
│   │   └── page.tsx        # Upload form page
│   ├── consultation/
│   │   └── page.tsx        # Consultation page
│   └── globals.css         # Global styles
├── components/
│   ├── Navbar.tsx          # Navigation component
│   └── ui/                 # ShadCN UI components
└── lib/
    └── utils.ts            # Utility functions
```

## Pages

### Home Page (/)
- Hero section with CTA
- How it works (3 steps)
- Why this matters section
- Footer with links

### Upload Page (/upload)
- Form with validation for:
  - Full Name
  - Age
  - City Last Seen
  - Date Last Seen
  - Contact Phone
  - Additional Description
  - Image Upload with preview

### Consultation Page (/consultation)
- Contact information for support services
- Request callback form
- Additional resources section

## Build for Production

```bash
npm run build
npm start
```

## License

This project is created for the FindMe platform.


