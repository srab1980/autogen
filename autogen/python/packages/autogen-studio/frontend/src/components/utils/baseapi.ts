import { getServerUrl } from "./utils";
import { safeStorage } from "./safe-storage";

// baseApi.ts
export abstract class BaseAPI {
  protected getBaseUrl(): string {
    return getServerUrl();
  }

  protected getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };
    if (typeof window !== "undefined") {
      const token = safeStorage.getItem("token");
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }
    return headers;
  }

  // Other common methods
}
