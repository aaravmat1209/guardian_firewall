# Guardian AI

A React-based child safety monitoring system for gaming chats, featuring advanced AI-powered threat detection and real-time content filtering.

## Design System

This application follows the design patterns inspired by [Quantra Security](https://quantra-security.webflow.io/) with our custom Guardian AI color scheme and branding.

### Key Features

- **Quantra-Inspired Design**: Modern, professional aesthetic with smooth animations
- **Custom Color Scheme**: Red accent colors (#DC2626) on dark backgrounds
- **Space Grotesk Typography**: Clean, geometric font matching Quantra's style
- **Responsive Design**: Mobile-first approach with smooth transitions
- **Advanced Animations**: Fade-in effects, hover states, and scroll-triggered animations

### Color Palette

```css
--color-black: #000000;
--color-dark: #0a0a0a;
--color-red: #DC2626;
--color-red-bright: #FF0000;
--color-white: #FFFFFF;
--color-gray: #E5E5E5;
--color-red-glow: rgba(220, 38, 38, 0.5);
--color-red-dim: rgba(220, 38, 38, 0.2);
```

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Removes the single build dependency

## Project Structure

```
src/
├── components/
│   ├── Navbar.jsx
│   └── Hero.jsx
├── styles/
│   ├── globals.css
│   ├── Navbar.css
│   └── Hero.css
├── App.jsx
└── index.js
```

## Components

### Navbar
- Fixed navigation with blur background
- Guardian AI branding with red accent
- Smooth hover animations
- Mobile-responsive hamburger menu

### Hero
- Full viewport height with animated content
- Quantra-style fade-up animations
- Interactive mouse-tracking glow effect
- Statistics display and call-to-action buttons

## Design Implementation

The design closely follows Quantra's aesthetic while maintaining Guardian AI's unique identity:

- **Typography**: Space Grotesk font with uppercase headings and proper letter spacing
- **Animations**: Smooth fade-in effects with staggered timing
- **Layout**: Clean grid system with consistent spacing
- **Interactive Elements**: Hover effects with glow and transform animations
- **Color Usage**: Strategic use of red accents on dark backgrounds

## Future Development

This is the foundation for a comprehensive child safety monitoring platform. Future features will include:

- Real-time chat monitoring dashboard
- AI threat detection analytics
- Content filtering controls
- Safety reporting system
- Parent/guardian notification center

## License

Private project for Guardian AI development.
