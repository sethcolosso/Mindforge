(function () {
  function getToken() {
    return localStorage.getItem('access_token');
  }

  async function postBySlug(url, slug, extraPayload) {
    const token = getToken();
    if (!token || !slug) return false;

    const payload = Object.assign({ slug: slug }, extraPayload || {});

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify(payload),
        keepalive: true,
      });
      return res.ok;
    } catch (err) {
      console.error('Exercise tracking error:', err);
      return false;
    }
  }

  window.MindForgeExerciseTracking = {
    trackOpenBySlug: function (slug) {
      return postBySlug('/api/exercises/open-by-slug/', slug);
    },
    completeBySlug: function (slug, durationSeconds, notes) {
      return postBySlug('/api/exercises/complete-by-slug/', slug, {
        duration_seconds: durationSeconds,
        notes: notes || '',
      });
    },
  };
})();
