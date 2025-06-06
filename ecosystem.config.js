module.exports = {
  apps: [
    {
      name: 'alimento-solidario',
      script: 'index.js',
      watch: false,
      env: {
        NODE_ENV: 'production',
      }
    }
  ]
};
