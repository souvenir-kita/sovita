/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,ts,jsx,tsx}', // Adjust the path based on your project structure
    './templates/**/*.html', // For Django projects, include templates folder
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
