self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('chooza-v1').then(cache => cache.addAll([
      '/',
      '/static/css/app.css',
      '/static/js/app.js',
      '/pwa/manifest.webmanifest'
    ]))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
