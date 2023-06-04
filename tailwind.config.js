module.exports = {
    content: [
        "./src/templates/**/*.html",
        "./src/static/src/**/*.js",
        "./src/api/presenters/**/*.py",
        "./src/knobs/**/*.py"
    ],
    theme: {
        extend: {},
        fontFamily: {
            sans: ['"Montserrat"', 'sans-serif'],
        },
        screens: {
            'sm': '640px',
            'md': '960px',
            'lg': '1200px'
        }
    },
    plugins: [],
}
