/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",  
    "./templates/dashboard/*.html",  
    "./templates/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

