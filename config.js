

export default {
  config: {
    port: 5000,
  },
  paths: {
    root: './',
    src: {
      base: "./static",
      css: "./static/css",
      js: "./static/js",
      img: "./static/img",
    },
    dist: {
      base: "./static/dist",
      css: "./static/dist/css",
      js: "./static/dist/js",
      img: "./static/dist/img",
    },
    build: {
      base: "./static/build",
      css: "./static/build/css",
      js: "./static/build/js",
      img: "./static/build/img",
    },
  },
};
