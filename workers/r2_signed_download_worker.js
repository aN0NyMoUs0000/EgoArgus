const encoder = new TextEncoder();

async function hmacHex(secret, message) {
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(message));
  return [...new Uint8Array(signature)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

function timingSafeEqualHex(left, right) {
  if (!left || !right || left.length !== right.length) {
    return false;
  }
  let diff = 0;
  for (let index = 0; index < left.length; index += 1) {
    diff |= left.charCodeAt(index) ^ right.charCodeAt(index);
  }
  return diff === 0;
}

function responseHeaders(object) {
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("etag", object.httpEtag);
  headers.set("cache-control", "private, max-age=3600");
  return headers;
}

export default {
  async fetch(request, env) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405 });
    }
    if (!env.EGOARGUS_BUCKET || !env.URL_SIGNING_SECRET) {
      return new Response("Worker is not configured", { status: 500 });
    }

    const url = new URL(request.url);
    const exp = url.searchParams.get("exp");
    const sig = url.searchParams.get("sig");
    const expiresAt = Number.parseInt(exp || "", 10);
    if (!Number.isFinite(expiresAt) || expiresAt < Math.floor(Date.now() / 1000)) {
      return new Response("Expired link", { status: 403 });
    }

    const canonicalMethod = request.method === "HEAD" ? "GET" : request.method;
    const expected = await hmacHex(
      env.URL_SIGNING_SECRET,
      `${canonicalMethod}\n${url.pathname}\n${expiresAt}`,
    );
    if (!timingSafeEqualHex(sig, expected)) {
      return new Response("Invalid signature", { status: 403 });
    }

    const objectKey = decodeURIComponent(url.pathname.slice(1));
    if (!objectKey) {
      return new Response("Missing object key", { status: 400 });
    }

    const object = await env.EGOARGUS_BUCKET.get(objectKey, {
      onlyIf: request.headers,
    });
    if (!object) {
      return new Response("Not found", { status: 404 });
    }
    if (object.body === null) {
      return new Response(null, { status: 304, headers: responseHeaders(object) });
    }

    return new Response(request.method === "HEAD" ? null : object.body, {
      headers: responseHeaders(object),
    });
  },
};
