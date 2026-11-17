/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/index.html", "./public/app.js"],
  theme: {
    extend: {
      colors: {
        puna: { 50: "#f6f3ee", 100: "#ebe4d8", 700: "#2a3442", 800: "#1b2430", 900: "#121922", 950: "#0b1017" },
        arcilla: { 300: "#f3b48a", 400: "#ec9560", 500: "#e2733a", 600: "#c95a26" },
        abierto: "#1b7f3b",
        cerrado: "#c0262d",
        telegram: "#2481cc",
      },
      fontFamily: {
        sans: ["system-ui", "-apple-system", "Segoe UI", "Roboto", "Helvetica Neue", "Arial", "sans-serif"],
      },
    },
  },
};
