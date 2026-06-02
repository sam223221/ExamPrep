// Intentionally minimal: the renderer needs no privileged APIs, so nothing is
// exposed over the context bridge. Keeping this empty preserves the security
// boundary (contextIsolation + sandbox) with zero attack surface.
export {};
