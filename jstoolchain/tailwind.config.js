/** @type {import('tailwindcss').Config} */
module.exports = {
content: ["../**/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require('@tailwindcss/aspect-ratio'),
    require("daisyui"),
    require("@tailwindcss/forms")({
      strategy: 'class', // only generate classes
    }),
  ],
  daisyui: {
    themes: [
      "light",
      "dark",
    ],
  },
  safelist: [
    'absolute',
    'w-24',
    'h-full',
    'duration-300',
    'ease-linear',
    'bg-neutral-900',
    'relative', 'w-full', 'h-3', 'overflow-hidden', 'rounded-full', 'bg-neutral-100'
  ]
}
