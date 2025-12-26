
/**
 * Safe storage wrapper to handle cases where localStorage is restricted
 * (e.g., sandboxed iframes, strict privacy settings).
 */
export const safeStorage = {
    getItem: (key: string): string | null => {
        try {
            if (typeof window !== "undefined" && window.localStorage) {
                return window.localStorage.getItem(key);
            }
        } catch (e) {
            // console.warn("localStorage access denied:", e);
        }
        return null;
    },

    setItem: (key: string, value: string): void => {
        try {
            if (typeof window !== "undefined" && window.localStorage) {
                window.localStorage.setItem(key, value);
            }
        } catch (e) {
            // console.warn("localStorage access denied:", e);
        }
    },

    removeItem: (key: string): void => {
        try {
            if (typeof window !== "undefined" && window.localStorage) {
                window.localStorage.removeItem(key);
            }
        } catch (e) {
            // console.warn("localStorage access denied:", e);
        }
    },
};
