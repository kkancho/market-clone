import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

export default {
  preprocess: vitePreprocess(),
  compilerOptions: {
    compatibility: {
      componentApi: 4, // Svelte 4 방식과 호환
    },
  },
};
