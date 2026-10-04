import { defineConfig, triggers } from "cf/config";
import * as entrypoint from "./src/index.ts" with { type: "cf-worker" };

// Static site: everything under public/ is served as an asset. The files live in
// public/games/flymetothemoon/ so their URLs match the route on mpts.ie.
export default defineConfig({
	worker: {
		name: "flymetothemoon",
		compatibilityDate: "2026-10-04",
		entrypoint,
		assets: {
			htmlHandling: "auto-trailing-slash",
			notFoundHandling: "none",
		},
		triggers: [triggers.fetch({ pattern: "mpts.ie/games/flymetothemoon*", zone: "mpts.ie" })],
	},
});
