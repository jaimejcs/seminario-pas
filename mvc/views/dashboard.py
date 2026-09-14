"""Serialização para a View web comum (frontend/app.js)."""
def present(models, traces):
    return {'roads': models, 'traces': traces}
