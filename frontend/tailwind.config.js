/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#F0F4F8',
          100: '#D9E2EC',
          800: '#102A43',
          900: '#0B1B2B',
        },
        civic: {
          offwhite: '#F8FAFC',
          card: '#FFFFFF',
          border: '#E2E8F0',
          navy: '#0F172A',
          teal: '#0D9488',
          emerald: '#059669',
          amber: '#D97706',
          rose: '#E11D48',
        }
      }
    },
  },
  plugins: [],
}
