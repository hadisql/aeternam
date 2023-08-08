/** @type {import('tailwindcss').Config} */
module.exports = {
content: ["../**/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require('@tailwindcss/aspect-ratio'), require("daisyui"),
   require("@tailwindcss/forms")({
    strategy: 'class', // only generate classes
  }),],
  daisyui: {
    themes: [
      "light",
      "dark",
      // "cupcake",
      // "bumblebee",
      // "emerald",
      // "corporate",
      // "synthwave",
      // "retro",
      // "cyberpunk",
      // "valentine",
      // "halloween",
      // "garden",
      // "forest",
      // "aqua",
      // "lofi",
      // "pastel",
      // "fantasy",
      // "wireframe",
      // "black",
      // "luxury",
      // "dracula",
      // "cmyk",
      // "autumn",
      // "business",
      // "acid",
      // "lemonade",
      // "night",
      // "coffee",
      // "winter",
    ],
  },
}
