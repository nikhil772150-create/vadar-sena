/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff7ed',
          100: '#ffedd5',
          500: '#f97316',
          600: '#ea580c',
          700: '#c2410c',
          900: '#7c2d12',
        },
        sena: {
          saffron: '#FF9933',
          green: '#138808',
          navy: '#000080',
          dark: '#1F2937'
        }
      }
    },
  },
  plugins: [],
}
