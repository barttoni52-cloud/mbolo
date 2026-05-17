const CACHE_NAME = 'mbolo-v1';
const URLS_TO_CACHE = [
  '/mbolo/',
  '/mbolo/index.html',
  '/mbolo/manifest.json'
];

// Installation — mise en cache des fichiers essentiels
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activation — suppression des anciens caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(name) {
          return name !== CACHE_NAME;
        }).map(function(name) {
          return caches.delete(name);
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch — réseau en priorité, cache en fallback
self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request)
      .then(function(response) {
        // Mettre à jour le cache si la requête réussit
        if (response && response.status === 200) {
          var responseClone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(function() {
        // Fallback sur le cache si pas de réseau
        return caches.match(event.request).then(function(cached) {
          return cached || caches.match('/mbolo/index.html');
        });
      })
  );
});
