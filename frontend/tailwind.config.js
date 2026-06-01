/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0b0d12",
        panel: "#11141b",
        panel2: "#161a23",
        border: "#1f2433",
        accent: "#6ee7b7",
        accent2: "#60a5fa",
        muted: "#8a93a6",
      },
    },
  },
  plugins: [],
};
