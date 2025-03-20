const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    [process.env.REACT_APP_URL_PREFIX],
    createProxyMiddleware({
      //target: 'https://engineering.arm.gov',
      target: 'http://localhost:8000',
      changeOrigin: true,
    })
  );
};
