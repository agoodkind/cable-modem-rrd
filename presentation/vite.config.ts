import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react-swc";
import { defineConfig } from "vite";
import wasm from "vite-plugin-wasm";

// https://vite.dev/config/
export default defineConfig({
	plugins: [react(), tailwindcss(), wasm()],
	build: {
		sourcemap: true,
	},
	server: {
		proxy: {
			"/api": {
				target: "http://localhost:8000",
				changeOrigin: true,
				secure: false,
			},
		},
	},
});
